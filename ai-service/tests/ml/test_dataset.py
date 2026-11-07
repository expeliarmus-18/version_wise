
import pytest

from app.ml.dataset import (
    DatasetValidationError,
    normalize_record,
    validate_records,
)


def make_record(**overrides):
    record = {
        "record_id": "record-1",
        "ecosystem": "MAVEN",
        "group_id": "org.example",
        "artifact_id": "sample",
        "current_version": "1.0.0",
        "target_version": "1.1.0",
        "upgrade_type": "MINOR",
        "project_id": "project-1",
        "observation_timestamp": "2025-01-01T00:00:00Z",
        "label": "TEST_FAILURE",
        "label_evidence": "Observed test failure",
        "label_confidence": "0.9",
        "data_source": "example-dataset",
        "source_license": "MIT",
        "split_group": "project-1",
    }

    record.update(overrides)
    return record


def test_normalize_record_preserves_source_label():
    record = normalize_record(
        make_record(label=" test_failure ")
    )

    assert record.label == "TEST_FAILURE"
    assert record.source_label == "test_failure"


def test_missing_required_field_is_rejected():
    source = make_record()
    source["project_id"] = ""

    with pytest.raises(DatasetValidationError):
        normalize_record(source)


def test_unknown_label_is_not_guessed():
    with pytest.raises(DatasetValidationError):
        normalize_record(
            make_record(label="MAYBE_FAILURE")
        )


@pytest.mark.parametrize(
    "confidence",
    ["invalid", "-0.1", "1.1"],
)
def test_invalid_confidence_is_rejected(confidence):
    with pytest.raises(DatasetValidationError):
        normalize_record(
            make_record(label_confidence=confidence)
        )


def test_duplicate_upgrade_is_removed():
    records, summary = validate_records(
        [
            make_record(record_id="record-1"),
            make_record(record_id="record-2"),
        ]
    )

    assert len(records) == 1
    assert summary.input_records == 2
    assert summary.valid_records == 1
    assert summary.duplicate_records == 1


def test_label_counts_are_calculated():
    records, summary = validate_records(
        [
            make_record(record_id="record-1"),
            make_record(
                record_id="record-2",
                artifact_id="another-artifact",
                label="COMPILATION_FAILURE",
            ),
        ]
    )

    assert len(records) == 2
    assert summary.label_counts == {
        "COMPILATION_FAILURE": 1,
        "TEST_FAILURE": 1,
    }
