from app.analysis.version_comparator import Comparison, compare_versions


def test_numeric_ordering_1_10_is_newer_than_1_2():
    assert compare_versions("1.2.0", "1.10.0").result == Comparison.UPGRADE


def test_equal_versions():
    assert compare_versions("1.2.3", "1.2.3").result == Comparison.EQUAL


def test_upgrade_and_downgrade():
    assert compare_versions("1.0.0", "2.0.0").result == Comparison.UPGRADE
    assert compare_versions("2.0.0", "1.0.0").result == Comparison.DOWNGRADE


def test_release_candidate_is_before_release():
    assert compare_versions("2.0.0-RC1", "2.0.0").result == Comparison.UPGRADE


def test_snapshot_precedes_release():
    assert compare_versions("2.0.0-SNAPSHOT", "2.0.0").result == Comparison.UPGRADE


def test_milestone_is_before_release_candidate():
    assert compare_versions("2.0.0-M1", "2.0.0-RC1").result == Comparison.UPGRADE


def test_unsupported_qualifier_is_unknown():
    assert compare_versions("1.0.0-custom", "1.0.1").result == Comparison.UNKNOWN
