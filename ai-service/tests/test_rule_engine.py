from app.analysis.rule_engine import analyze_upgrade
from app.models.risk import UpgradeAnalysisRequest


def request(current, target, **extra):
    return UpgradeAnalysisRequest(
        groupId="org.example", artifactId="demo",
        currentVersion=current, targetVersion=target, **extra
    )


def test_patch_upgrade_score_and_explanation():
    result = analyze_upgrade(request("1.2.3", "1.2.4", metadataAvailable=True))
    assert result.risk_score == 5
    assert result.risk_category == "LOW"
    assert result.factors[0].rule_id == "PATCH_CHANGE"
    assert result.factors[0].contribution == 5


def test_minor_upgrade_score():
    result = analyze_upgrade(request("1.2.3", "1.3.0", metadataAvailable=True))
    assert result.risk_score == 15
    assert result.risk_category == "LOW"


def test_major_upgrade_score():
    result = analyze_upgrade(request("1.2.3", "2.0.0", metadataAvailable=True))
    assert result.risk_score == 40
    assert result.risk_category == "HIGH"


def test_downgrade_score():
    result = analyze_upgrade(request("2.0.0", "1.0.0", metadataAvailable=True))
    assert result.risk_score == 30
    assert result.comparison == "downgrade"


def test_prerelease_target_adds_factor():
    result = analyze_upgrade(request("1.0.0", "2.0.0-RC1", metadataAvailable=True))
    assert result.risk_score == 60
    assert {f.rule_id for f in result.factors} == {"MAJOR_CHANGE", "PRERELEASE_TARGET"}


def test_unknown_comparison_is_not_upgrade():
    result = analyze_upgrade(request("1.0.0-custom", "1.0.1", metadataAvailable=True))
    assert result.comparison == "unknown"
    assert result.risk_score == 20
    assert result.warnings


def test_unresolved_metadata_is_visible():
    result = analyze_upgrade(request("1.0.0", "1.1.0", versionResolution="unresolved"))
    assert "VERSION_METADATA_UNRESOLVED" in {f.rule_id for f in result.factors}
    assert result.warnings


def test_deterministic_output():
    req = request("1.2.3", "2.0.0", metadataAvailable=False)
    assert analyze_upgrade(req).model_dump() == analyze_upgrade(req).model_dump()
