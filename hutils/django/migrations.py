from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.operations.base import Operation
from django.db.migrations.state import ProjectState
from django.db.models import NOT_PROVIDED


class AlterDefault(Operation):
    """ AlterDefault value to database. (which will persist default value to database layer)

    Examples::

        operations = [
            AlterDefault(model_name='model', name='field'),
        ]
    """

    # Can this migration be represented as SQL? (things like RunPython cannot)
    reduces_to_sql = True

    # Should this operation be considered safe to elide and optimize across?
    elidable = True

    def __init__(self, model_name: str, name: str):
        self.model_name = model_name
        self.name = name

    def deconstruct(self):
        return (
            self.__class__.__name__,
            [],
            {
                'model_name': self.model_name,
                'name': self.name,
            },
        )

    def state_forwards(self, app_label, state):
        """ do nothing for Django State """

    def database_forwards(self, app_label, schema_editor: BaseDatabaseSchemaEditor, from_state, to_state: ProjectState):
        to_model = to_state.apps.get_model(app_label, self.model_name)
        meta = to_model._meta
        to_field = meta.get_field(self.name)
        if to_field.default != NOT_PROVIDED:
            table_name = schema_editor.quote_name(meta.db_table)
            column = schema_editor.quote_name(to_field.column)
            default = schema_editor.quote_value(to_field.default)
            schema_editor.execute(f'ALTER TABLE {table_name} ALTER COLUMN {column} SET DEFAULT {default}')

    def database_backwards(self, app_label, schema_editor: BaseDatabaseSchemaEditor, from_state, to_state):
        self.database_forwards(app_label, schema_editor, from_state, to_state)

    def describe(self):
        return f'Altering default value for {self.model_name}.{self.name}'
