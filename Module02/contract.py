"""Executable data contract for the repaired maintenance schema."""

from datetime import date

from pydantic import BaseModel, Field, ValidationError, field_validator
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    UniqueConstraint,
    create_engine,
)


class Machine(BaseModel):
    machine_id: int = Field(ge=1)
    serial_no: str = Field(min_length=3)
    site: str = Field(min_length=1)
    installed: date

    @field_validator("serial_no")
    @classmethod
    def serial_has_prefix(cls, value: str) -> str:
        if not value.startswith("SN-"):
            raise ValueError("serial number must start with SN-")
        return value


class MaintenanceJob(BaseModel):
    job_id: int = Field(ge=1)
    machine_id: int = Field(ge=1)
    technician: str = Field(min_length=1)
    done_on: date
    part_nos: list[str] = Field(default_factory=list)


metadata = MetaData()

machine_table = Table(
    "machine",
    metadata,
    Column("machine_id", Integer, primary_key=True),
    Column("serial_no", String, nullable=False),
    Column("site", String, nullable=False),
    Column("installed", Date, nullable=False),
    UniqueConstraint("serial_no", name="uq_machine_serial"),
)

part_table = Table(
    "part",
    metadata,
    Column("part_no", String, primary_key=True),
    Column("description", String, nullable=False),
    Column("unit_price", Numeric(9, 2), nullable=False),
)

maintenance_job_table = Table(
    "maintenance_job",
    metadata,
    Column("job_id", Integer, primary_key=True),
    Column(
        "machine_id",
        Integer,
        ForeignKey("machine.machine_id"),
        nullable=False,
    ),
    Column("technician", String, nullable=False),
    Column("done_on", Date, nullable=False),
)

job_part_table = Table(
    "job_part",
    metadata,
    Column(
        "job_id",
        Integer,
        ForeignKey("maintenance_job.job_id"),
        primary_key=True,
    ),
    Column(
        "part_no",
        String,
        ForeignKey("part.part_no"),
        primary_key=True,
    ),
)


if __name__ == "__main__":
    valid_job = MaintenanceJob(
        job_id=1,
        machine_id=1,
        technician="Beier",
        done_on=date(2026, 1, 8),
        part_nos=["P-1001", "P-1002"],
    )
    print(f"Valid job: {valid_job.model_dump()}")

    try:
        Machine(
            machine_id=1,
            serial_no="not-a-serial",
            site="Gütersloh",
            installed="unknown",
        )
    except ValidationError as error:
        print("Invalid machine rejected:")
        print(error.errors()[0]["msg"])

    engine = create_engine("sqlite://")
    metadata.create_all(engine)
    print("Created tables:", ", ".join(metadata.tables))

