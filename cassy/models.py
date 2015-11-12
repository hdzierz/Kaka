# Create your columns here.

import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class ExampleModel(Model):
    read_repair_chance = 0.05 # optional - defaults to 0.1
    example_id      = columns.UUID(primary_key=True, default=uuid.uuid4)
    example_type    = columns.Integer(index=True)
    created_at      = columns.DateTime()
    description     = columns.Text(required=False)


class DataSource(Model):
    id = columns.UUID(primary_key=True, default=uuid.uuid4)

    name = columns.Text()
    tablename = columns.Text()
    owner = columns.Text()
    description = columns.Text()
    classname = columns.Text()
    group = columns.Text()


