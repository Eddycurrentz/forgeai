from forgeai_api.core.db import Base
from forgeai_api.models import Approval, Job, Repository, Run


def test_phase_two_models_define_expected_tables() -> None:
    expected_tables = {"repositories", "runs", "jobs", "approvals"}

    assert expected_tables <= set(Base.metadata.tables)
    mapped_classes = {mapper.class_ for mapper in Base.registry.mappers}
    assert {Repository, Run, Job, Approval} <= mapped_classes


def test_phase_two_tables_have_timestamps_and_foreign_keys() -> None:
    for table_name in ("repositories", "runs", "jobs", "approvals"):
        table = Base.metadata.tables[table_name]
        assert {"created_at", "updated_at"} <= set(table.c.keys())

    assert {"repository_id"} <= set(Base.metadata.tables["runs"].c.keys())
    assert {"run_id"} <= set(Base.metadata.tables["jobs"].c.keys())
    assert {"run_id"} <= set(Base.metadata.tables["approvals"].c.keys())

    foreign_keys = {
        (foreign_key.parent.table.name, foreign_key.target_fullname)
        for table in Base.metadata.tables.values()
        for foreign_key in table.foreign_keys
    }
    assert ("runs", "repositories.id") in foreign_keys
    assert ("jobs", "runs.id") in foreign_keys
    assert ("approvals", "runs.id") in foreign_keys
