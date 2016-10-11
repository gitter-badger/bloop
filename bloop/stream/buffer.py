from datetime import datetime
import heapq
from typing import Tuple, List, Iterable, Mapping, Any
from .shard import Shard


def heap_item(
        clock: int,
        record: Mapping[str, Any],
        shard: Shard) -> Tuple[Tuple[datetime, str, int], Tuple[Mapping[str, Any], Shard]]:
    # Primary ordering is by event creation time.
    # However, creation time is *approximate* and has whole-second resolution.
    # This means two events in the same shard within one second can't be ordered.
    ordering = record["meta"]["created_at"]
    # From testing, SequenceNumber isn't a guaranteed ordering either.  However,
    # it is guaranteed to be unique within a shard.  This will be tie-breaker
    # for multiple records within the same shard, within the same second.
    second_ordering = record["meta"]["sequence_number"]
    # It's possible though unlikely, that sequence numbers will collide across
    # multiple shards, within the same second.  The final tie-breaker is
    # a monotonically increasing integer from the buffer.
    return (ordering, second_ordering, clock), (record, shard)


class RecordBuffer:
    def __init__(self):
        # (total_ordering, (record, shard))
        #  ^--sort          ^--data ^--src
        self._heap = []

        # Used by the total ordering clock
        self.__monotonic_integer = 0

    def push(self, record: Mapping[str, Any], shard: Shard) -> None:
        heapq.heappush(self._heap, heap_item(self.clock, record, shard))

    def push_all(self, record_shard_pairs: Iterable[Tuple[Mapping[str, Any], Shard]]) -> None:
        # Faster than inserting one at a time;
        # the heap is sorted once after all inserts.
        for pair in record_shard_pairs:
            self._heap.append(heap_item(self.clock, *pair))
        heapq.heapify(self._heap)

    def pop(self) -> Tuple[Mapping[str, Any], Shard]:
        return heapq.heappop(self._heap)[1]

    def peek(self) -> Tuple[Mapping[str, Any], Shard]:
        return self._heap[0][1]

    def clear(self) -> None:
        self._heap.clear()

    @property
    def heap(self) -> List[Tuple[Tuple[datetime, str, int], Tuple[Mapping[str, Any], Shard]]]:
        return self._heap

    def __len__(self) -> int:
        return len(self._heap)

    @property
    def clock(self) -> int:
        """A monotonically increasing integer."""
        # The return value is in between previous and new, so that __monotonic_integer
        # is never set to a tie-breaking value.  This tries to avoid collisions when
        # someone directly manipulates the underlying int.
        self.__monotonic_integer += 2
        return self.__monotonic_integer - 1
