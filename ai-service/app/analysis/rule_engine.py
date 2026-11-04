from app.analysis.version_comparator import Comparison, compare_versions
from app.models.risk import UpgradeAnalysisRequest, UpgradeAnalysisResponse, RiskFactor


def _category(score: int) -> str:
    if score < 20:
        return "LOW"
    if score < 40:
        return "MODERATE"
    if score < 70:
        return "HIGH"
    return "CRITICAL"


def analyze_upgrade(request: UpgradeAnalysisRequest) -> UpgradeAnalysisResponse:
    compared = compare_versions(request.current_version, request.target_version)
    factors: list[RiskFactor] = []
    warnings: list[str] = []
    recommendations: list[str] = []
    score = 0

    def add(rule_id, name, points, explanation):
        nonlocal score
        score += points
        factors.append(RiskFactor(
            ruleId=rule_id, name=name, contribution=points,
            explanation=explanation, currentVersion=request.current_version,
            targetVersion=request.target_version, evidenceSource=None,
        ))

    if compared.result == Comparison.UNKNOWN:
        add("VERSION_UNCERTAIN", "Version comparison uncertain", 20, compared.explanation)
        warnings.append("Version ordering could not be established reliably; risk assessment is incomplete.")
        recommendations.append("Perform a manual version and compatibility assessment.")
    elif compared.result == Comparison.DOWNGRADE:
        add("DOWNGRADE", "Dependency downgrade", 30,
            "The target version is older than the current version under the supported comparison.")
        recommendations.extend(["Review the reason for the downgrade.", "Run unit and integration tests."])
    elif compared.result == Comparison.EQUAL:
        warnings.append("Current and target versions compare as equivalent; this is not a version upgrade.")
    else:
        current_parts = compared.current_parts or ()
        target_parts = compared.target_parts or ()
        # Magnitude is assigned once, at the highest changed numeric position.
        if current_parts and target_parts:
            width = max(len(current_parts), len(target_parts))
            a = current_parts + (0,) * (width - len(current_parts))
            b = target_parts + (0,) * (width - len(target_parts))
            changed = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), None)
            if changed == 0:
                add("MAJOR_CHANGE", "Major version change", 40,
                    "The leading numeric version component changed.")
                recommendations.extend(["Review release notes and migration guides.", "Review API and runtime compatibility.", "Run unit and integration tests."])
            elif changed == 1:
                add("MINOR_CHANGE", "Minor version change", 15,
                    "The second numeric version component changed while the leading component remained stable.")
                recommendations.extend(["Review release notes for behavior changes.", "Run unit and integration tests."])
            elif changed is not None:
                add("PATCH_CHANGE", "Patch-level version change", 5,
                    "Only a later numeric version component changed.")
                recommendations.append("Run the project's unit tests.")
        else:
            warnings.append("Version comparison succeeded, but numeric upgrade magnitude could not be classified.")
            add("MAGNITUDE_UNCERTAIN", "Upgrade magnitude uncertain", 10,
                "The version ordering is known, but numeric components are insufficient for magnitude classification.")
            recommendations.append("Review the release notes and validate compatibility manually.")

    target_lower = request.target_version.lower()
    if any(q in target_lower for q in ("snapshot", "-rc", "-cr", "-alpha", "-beta", "-milestone", "-m")):
        add("PRERELEASE_TARGET", "Prerelease or snapshot target", 20,
            "The target version appears to be a prerelease, milestone, or snapshot.")
        warnings.append("Prerelease stability and compatibility have not been independently verified.")
        recommendations.append("Confirm that a prerelease dependency is appropriate for the target environment.")

    if request.version_resolution in ("unresolved", "missing"):
        add("VERSION_METADATA_UNRESOLVED", "Version metadata unresolved", 20,
            "The request indicates the current dependency version was unresolved or missing in the POM.")
        warnings.append("The parser cannot resolve full Maven inheritance or dependency-management context.")
        recommendations.append("Resolve the effective Maven version using the project's Maven build context.")

    if request.metadata_available is False:
        add("DEPENDENCY_METADATA_MISSING", "Dependency metadata unavailable", 5,
            "No additional dependency metadata was supplied for this assessment.")
        warnings.append("No release-note, compatibility, or vulnerability evidence was provided.")
    elif request.metadata_available is None:
        warnings.append("Dependency metadata availability was not specified; no metadata score was added.")

    score = min(100, max(0, score))
    # Deduplicate recommendations while preserving deterministic order.
    recommendations = list(dict.fromkeys(recommendations))
    return UpgradeAnalysisResponse(
        groupId=request.group_id, artifactId=request.artifact_id,
        currentVersion=request.current_version, targetVersion=request.target_version,
        comparison=compared.result.value, riskScore=score, riskCategory=_category(score),
        factors=factors, warnings=warnings, recommendations=recommendations,
        scoreIsProbability=False,
    )
