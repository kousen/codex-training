"""Distribution-level smoke tests for the built wheel and console entry point."""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUCCESS_EXIT_CODE = 0


def test_built_wheel_installs_and_exposes_cli(tmp_path: Path) -> None:
    """A wheel works outside the source tree and provides its declared command."""
    wheel_directory = tmp_path / "wheel"
    installed_site = tmp_path / "site"

    build_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--wheel",
            "--outdir",
            str(wheel_directory),
            str(PROJECT_ROOT),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert build_result.returncode == SUCCESS_EXIT_CODE, build_result.stderr

    wheels = list(wheel_directory.glob("*.whl"))
    assert len(wheels) == 1
    install_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--target",
            str(installed_site),
            str(wheels[0]),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert install_result.returncode == SUCCESS_EXIT_CODE, install_result.stderr

    command = installed_site / "bin" / "legacy-processor"
    environment = {**os.environ, "PYTHONPATH": str(installed_site)}
    cli_result = subprocess.run(
        [str(command), "--help"],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert cli_result.returncode == SUCCESS_EXIT_CODE
    assert "Filter, transform, and validate records" in cli_result.stdout
