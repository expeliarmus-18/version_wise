
from app.ml.dataset import normalize_record
from app.ml.split import split_by_group


def make_record(record_id: str, split_group: str) -> dict[str, str]:
    return {
        "record_id": record_id,
        "ecosystem": "maven",
        "group_id": "org.example",
        "artifact_id": "library",
        "current_version": "1.0.0",
        "target_version": "2.0.0",
        "upgrade_type": "MAJOR",
        "project_id": f"project-{split_group}",
        "observation_timestamp": "2025-01-01T00:00:00Z",
        "label": "TEST_FAILURE",
        "label_evidence": "Build test failure",
        "data_source": "test-fixture",
        "source_license": "MIT",
        "split_group": split_group,
    }


def build_records() -> list:
    return [
        normalize_record(make_record(f"record-{group}", str(group)))
        for group in range(10)
    ]


def test_split_preserves_all_records():
    records = build_records()

    result = split_by_group(records)

    combined = result.train + result.validation + result.test

    assert len(combined) == len(records)
    assert {record.record_id for record in combined} == {
        record.record_id for record in records
    }


def test_split_groups_do_not_leak():
    result = split_by_group(build_records())

    train_groups = {record.split_group for record in result.train}
    validation_groups = {record.split_group for record in result.validation}
    test_groups = {record.split_group for record in result.test}

    assert train_groups.isdisjoint(validation_groups)
    assert train_groups.isdisjoint(test_groups)
    assert validation_groups.isdisjoint(test_groups)


def test_split_is_deterministic():
    records = build_records()

    first = split_by_group(records, random_seed=42)
    second = split_by_group(records, random_seed=42)

    assert [record.record_id for record in first.train] == [
        record.record_id for record in second.train
    ]
    assert [record.record_id for record in first.validation] == [
        record.record_id for record in second.validation
    ]
    assert [record.record_id for record in first.test] == [
        record.record_id for record in second.test
    ]


def test_split_rejects_fewer_than_three_groups():
    records = [
        normalize_record(make_record("record-1", "group-1")),
        normalize_record(make_record("record-2", "group-2")),
    ]

    try:
        split_by_group(records)
    except ValueError as exc:
        assert "At least 3 distinct split groups" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_split_rejects_invalid_ratios():
    records = build_records()

    try:
        split_by_group(
            records,
            train_ratio=0.7,
            validation_ratio=0.2,
            test_ratio=0.2,
        )
    except ValueError as exc:
        assert "sum to 1.0" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
