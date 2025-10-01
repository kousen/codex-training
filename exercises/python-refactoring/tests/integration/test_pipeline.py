"""Integration tests covering the processing workflow."""

from __future__ import annotations

from pathlib import Path

from data_processing.service import EmployeeDataService
from data_processing.writers import EmployeeReportWriter


def test_generate_report(employee_service: EmployeeDataService, tmp_path: Path) -> None:
    payload = employee_service.generate_report_payload()
    report_path = tmp_path / "report.txt"
    with EmployeeReportWriter(report_path) as writer:
        writer.write(payload)

    content = report_path.read_text(encoding="utf-8")
    assert "Salary Report" in content
    assert "Average Salary" in content
    assert "John Doe" in content
