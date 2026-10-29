from sqlalchemy import (
    BIGINT,
    Column,
    LargeBinary,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB

from src.domain.entities.task import Task
from src.infrastructure.models.base import mapper_registry, timestamp_columns

task = Table(
    "task",
    mapper_registry.metadata,
    Column("id", BIGINT, primary_key=True, autoincrement=True),
    Column("status", String(32), nullable=False),
    Column("column", String(255), nullable=False),
    Column("data", LargeBinary, nullable=False),
    Column("result", JSONB()),
    Column("error", Text),
    *timestamp_columns(),
)

def mapped_task_table():
    mapper_registry.map_imperatively(Task, task)
