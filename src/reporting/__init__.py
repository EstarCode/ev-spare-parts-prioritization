# Reporting & Coverage Matrix Subpackage. Generates candidate vehicle selection evidence and the 30-combination coverage matrix.
from .coverage_report import (
    build_vehicle_selection_evidence,
    generate_30_combination_coverage_matrix
)

__all__ = [
    "build_vehicle_selection_evidence",
    "generate_30_combination_coverage_matrix"
]
