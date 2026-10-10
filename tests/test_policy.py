import subprocess

import pytest


TARGET = {
    "staff-client": "https://10.10.10.254/",
    "guest-client": "https://10.10.20.254/",
    "attacker": "https://10.10.66.254/",
}


def run_from_client(service: str, url: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "docker",
            "compose",
            "exec",
            "-T",
            service,
            "wget",
            "--no-check-certificate",
            "--timeout=3",
            "-qO-",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


@pytest.fixture(scope="session", autouse=True)
def require_running_stack():
    result = subprocess.run(
        ["docker", "compose", "ps", "--status", "running", "-q"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        pytest.skip("start the Compose stack before running integration tests")


def test_staff_can_reach_ehr_proxy():
    result = run_from_client("staff-client", TARGET["staff-client"])
    assert result.returncode == 0, result.stderr
    assert "Directory listing" in result.stdout


@pytest.mark.parametrize(
    ("service", "url"),
    [
        ("guest-client", TARGET["guest-client"]),
        ("attacker", TARGET["attacker"]),
    ],
)
def test_untrusted_zones_cannot_reach_gateway_proxy(service: str, url: str):
    result = run_from_client(service, url)
    assert result.returncode != 0


def test_staff_cannot_bypass_gateway_to_ehr_network():
    result = run_from_client("staff-client", "https://10.10.30.10/")
    assert result.returncode != 0
