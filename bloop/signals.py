from .util import signal

before_create_table = signal("before_create_table")
before_create_table.__doc__ = """:class:`~blinker.base.Signal` sent before a model's backing table is created.

Basic Usage:

.. code-block:: python

    # Nonce table names to avoid testing collisions
    @before_create_table.connect
    def apply_table_nonce(_, model, **__):
        nonce = arrow.now().isoformat()
        model.Meta.table_name += "-test-{}".format(nonce)

:param engine: :class:`~bloop.engine.Engine` creating the model's table.
:param model: The :class:`~bloop.models.BaseModel` class to create a table for.
"""

table_validated = signal("table_validated")
table_validated.__doc__ = """:class:`~blinker.base.Signal` sent after a model's expected table is validated.

This signal is sent before :data:`~bloop.signals.model_validated` and :data:`~bloop.signals.model_bound`.

:param model: The :class:`~bloop.models.BaseModel` class that was validated.
:param actual_description: (dict) Sanitized description from DynamoDB.
:param expected_description: (dict) May be a subset of ``actual_description``.
"""

object_loaded = signal("object_loaded")
object_loaded.__doc__ = """:class:`~blinker.base.Signal` sent after an object is loaded from DynamoDB.


Basic Usage:

.. code-block:: python

    # Track objects "checked out" locally
    local_objects = {}

    def key(obj):
        meta = obj.__class__.Meta
        return (getattr(obj, k.model_name) for k in meta.keys)

    @object_loaded.connect
    def on_loaded(_, obj, **__):
        local_objects[key(obj)] = obj

:param engine: The :class:`~bloop.engine.Engine` that loaded the object.
:param obj: The :class:`~bloop.models.BaseModel` loaded from DynamoDB.
"""

object_saved = signal("object_saved")
object_saved.__doc__ = """:class:`~blinker.base.Signal` sent after an object is saved to DynamoDB.

Basic Usage:

.. code-block:: python

    # Track objects "checked out" locally
    local_objects = {}

    def key(obj):
        meta = obj.__class__.Meta
        return (getattr(obj, k.model_name) for k in meta.keys)

    @object_saved.connect
    def on_saved(_, obj, **__):
        local_objects.pop(key(obj))

:param engine: The :class:`~bloop.engine.Engine` that saved the object.
:param obj: The :class:`~bloop.models.BaseModel` saved to DynamoDB.
"""

object_deleted = signal("object_deleted")
object_deleted.__doc__ = """:class:`~blinker.base.Signal` sent after an object is deleted from DynamoDB.

Basic Usage:

.. code-block:: python

    # Track objects "checked out" locally
    local_objects = {}

    def key(obj):
        meta = obj.__class__.Meta
        return (getattr(obj, k.model_name) for k in meta.keys)

    @object_deleted.connect
    def on_deleted(_, obj, **__):
        local_objects.pop(key(obj))

:param engine: The :class:`~bloop.engine.Engine` that deleted the object.
:param obj: The :class:`~bloop.models.BaseModel` deleted from DynamoDB.
"""

object_modified = signal("object_modified")
object_modified.__doc__ = """:class:`~blinker.base.Signal` sent after an object's attribute is set or deleted.

* Always sent on ``__del__``, regardless of exceptions.
* Only sent on ``__set__`` if an exception isn't raised.

Basic Usage:

.. code-block:: python

    # Account balance can't be less than 0

    @object_modified.connect
    def enforce_positive_balance(_, obj, column, value, **__):
        if column is Account.balance and value < 0:
            # Danger: careful around infinite loops!
            setattr(obj, column.model_name, 0)

:param column: The :class:`~bloop.models.Column` that corresponds to the modified attribute.
:param obj: The :class:`~bloop.models.BaseModel` that was modified.
:param value: The new value of the attribute.
"""


model_bound = signal("model_bound")
model_bound.__doc__ = """:class:`~blinker.base.Signal` sent after a model has been bound to an
:class:`~bloop.engine.Engine`.

This signal is sent after :data:`~bloop.signals.table_validated` and :data:`~bloop.signals.model_validated`.

:param engine: The :class:`~bloop.engine.Engine` that the model was bound to.
:param model: The :class:`~bloop.models.BaseModel` class that was bound.
"""


model_created = signal("model_created")
model_created.__doc__ = """:class:`~blinker.base.Signal` sent after a new model is defined.

While this signal is sent when the :class:`~bloop.models.BaseModel` is created, the BaseModel is created so
early in Bloop's import order that no handlers will be connected when it occurs.

You can manually send the BaseModel through your handler with:

.. code-block:: python

    model_created.send(model=BaseModel)

:param model: The subclass of :class:`~bloop.models.BaseModel` that was created.
"""

model_validated = signal("model_validated")
model_validated.__doc__ = """:class:`~blinker.base.Signal` sent after a model is validated.

This signal is sent after :data:`~bloop.signals.table_validated` and before :data:`~bloop.signals.model_bound`.

:param engine: The :class:`~bloop.engine.Engine` that validated the model.
:param model: The :class:`~bloop.models.BaseModel` class that was validated.
"""
