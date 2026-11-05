# VersionWise — Day 8: ML Dataset and Feasibility Research

**Status:** Research completed; implementation and training deferred to Day 9
**Project:** VersionWise
**Focus:** Historical Java/Maven dependency-upgrade data and ML feasibility

## 1. Objective

Evaluate whether VersionWise can move from deterministic dependency-upgrade risk analysis to a machine-learning-assisted approach using historical dependency-upgrade data.

The research covers:

- Dataset suitability and availability
- Label quality and evidence
- Data licensing and provenance
- Candidate model features
- Evaluation methodology
- Training constraints based on the development laptop

No model training is performed on Day 8.

## 2. Development Hardware and Constraints

The development laptop has:

- AMD Ryzen 7 4800H CPU
- 16 GB RAM
- NVIDIA RTX 3050 GPU with 4 GB VRAM
- Approximately 200 GB free SSD storage

The initial ML approach must be practical on this hardware.

The project will prioritize compact structured datasets and classical ML models. GPU training is not required for the first experiments.

The full BUMP Docker archive and large transformer fine-tuning are out of scope for the initial local training phase.

## 3. BUMP Dataset Research

BUMP is a benchmark of reproducible breaking dependency updates.

The published benchmark contains 571 breaking dependency updates across 153 Java projects.

BUMP is useful for studying failure modes associated with dependency upgrades. Its records include dependency identity, old and new versions, update type, project context, build reproduction information, and failure categories.

However, BUMP focuses on breaking updates. It is not automatically representative of all ordinary dependency upgrades encountered by VersionWise.

### Storage Considerations

The full archived dataset is approximately 150 GB. The Docker-based reproduction workflow can require approximately 250 GB of disk space.

The available laptop storage is approximately 200 GB.

Therefore:

- Do not download the complete archive.
- Do not reproduce the full Docker environment locally.
- Prefer compact metadata and selected records.
- Retain dataset provenance and license information.
- Avoid unnecessary raw source and build-artifact storage.

### License and Provenance

The repository license and the licenses of underlying projects and archived artifacts must be considered separately.

Before redistributing or incorporating dataset material, verify the applicable dataset and source-project terms.

Preserve source attribution and provenance for any selected records.

## 4. Successful Upgrade Data

A general dependency-upgrade risk model requires evidence of both unsuccessful and successful upgrades.

A merged pull request, approved update, or completed version change is not by itself conclusive evidence that the resulting dependency upgrade built successfully or remained compatible at runtime.

Candidate success records must be labeled according to the evidence available.

Examples:

- A merged PR without build evidence: weak success evidence
- A successful post-upgrade build: stronger build evidence
- A successful build and test run: stronger evidence, but not proof of runtime compatibility
- Missing or ambiguous build evidence: unknown

The model must not imply causation or runtime compatibility when the available evidence does not support those conclusions.

## 5. Candidate Labels

The initial label vocabulary is:

- `COMPILATION_FAILURE`
- `TEST_FAILURE`
- `DEPENDENCY_RESOLUTION_FAILURE`
- `OTHER_BUILD_FAILURE`
- `SUCCESSFUL_BUILD`
- `UNKNOWN`

The original source label and supporting evidence must be preserved.

A reproducible failure with a passing baseline is stronger evidence than a CI failure without a known baseline.

Labels should include an evidence category and confidence indicator where possible. Label confidence must not be confused with a model's predicted probability.

## 6. Candidate Features

Potential features include:

### Dependency Information

- Dependency group and artifact identifiers
- Current and target versions
- Upgrade type
- Dependency scope
- Direct or transitive status

### Maven Context

- Dependency-management source
- Whether a version is supplied through a property
- Relevant project and build configuration
- Missing metadata indicators
- Version-comparison confidence

### Historical Context

- Previous dependency outcomes, when available before prediction time
- Project history, when legally and reliably available
- Dependency history, when available before the prediction timestamp

### Leakage Prevention

Features that reveal the outcome of the upgrade must not be used to predict that same outcome.

Examples of potential leakage include:

- Post-upgrade build status
- Failure traces from the evaluated update
- Revert information
- CI results produced after the prediction timestamp
- Any target label derived directly from a feature

## 7. Proposed Dataset Schema

The normalized dataset should retain:

- `record_id`
- `ecosystem`
- `group_id`
- `artifact_id`
- `current_version`
- `target_version`
- `upgrade_type`
- `project_id`
- `observation_timestamp`
- `label`
- `label_evidence`
- `label_confidence`
- `feature_values`
- `data_source`
- `source_license`
- `split_group`
- `notes`

Raw source data, normalized records, model features, label evidence, and provenance should remain logically separated.

Do not include secrets, private repository content, or unnecessary personal information.

## 8. Evaluation Methodology

Evaluation must account for class imbalance and data leakage.

The proposed process is:

1. Deduplicate records and identify related upgrades.
2. Use time-aware evaluation where timestamps permit.
3. Keep related records from the same project together where practical.
4. Compare against a simple majority-class baseline.
5. Compare against the Day 7 deterministic engine only when both methods are evaluated on the same target and evidence.
6. Report precision, recall, F1, macro-F1, and a confusion matrix.
7. For binary failure prediction, consider PR-AUC and failure-class precision and recall.
8. Avoid relying on accuracy alone.

A model should proceed toward integration only if it demonstrates useful held-out performance and improves on the deterministic baseline for the intended use case.

## 9. Laptop-Aware Training Plan

The initial training plan is designed to avoid unnecessarily long training runs.

### Initial Experiment Limits

- Start with a representative sample of up to 10,000 records, if suitable data is available.
- Keep the initial feature set compact.
- Begin with Logistic Regression, Random Forest, and Gradient Boosting.
- Use a small sample to validate the pipeline before a larger run.
- Set short per-model time budgets.
- Avoid parallel memory-heavy training jobs.
- Do not use GPU training unless a later experiment demonstrates a clear need.

These are initial planning limits, not guarantees of exact runtime.

If the data is unsuitable or training is unexpectedly slow, stop and reassess rather than leave the laptop training for hours.

## 10. Day 8 Conclusion

Dataset research establishes that BUMP may support failure-category research, but it does not by itself establish the feasibility of a representative general-purpose dependency-upgrade risk model.

The availability and quality of successful-upgrade labels remain important unresolved requirements.

Day 8 is complete when the research, label strategy, feature considerations, evaluation plan, and hardware constraints are documented.

Day 9 training should begin only after the data and label feasibility criteria are met. Otherwise, Day 9 should focus on improving data collection and labeling rather than training a weak or misleading model.

## References

- BUMP repository: https://github.com/chains-project/bump
- BUMP research paper: https://arxiv.org/abs/2401.09906
- BUMP Zenodo archive: https://zenodo.org/records/10041883

References must be reviewed for applicable dataset, source-project, and redistribution terms before using or redistributing data.
