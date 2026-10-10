import subprocess
import time

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
    assert "ClinicGuard synthetic EHR" in result.stdout


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


def run_in_service(service: str, *command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "exec", "-T", service, *command],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def test_gateway_forwarding_is_enabled():
    result = run_in_service("gateway", "cat", "/proc/sys/net/ipv4/ip_forward")
    assert result.returncode == 0
    assert result.stdout.strip() == "1"


def test_gateway_forward_chain_is_default_deny():
    result = run_in_service("gateway", "nft", "list", "chain", "inet", "clinicguard", "forward")
    assert result.returncode == 0, result.stderr
    assert "policy drop" in result.stdout


def test_suricata_is_running_on_gateway_namespace():
    result = subprocess.run(
        ["docker", "compose", "ps", "--status", "running", "-q", "suricata"],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip()


def test_attack_simulation_generates_suricata_alert():
    attack = run_in_service("attacker", "/attack/attack.sh")
    assert attack.returncode == 0, attack.stderr

    deadline = time.time() + 10
    while time.time() < deadline:
        alerts = run_in_service(
            "suricata",
            "sh",
            "-c",
            "grep '\"signature_id\":1000002' /var/log/suricata/eve.json",
        )
        if alerts.returncode == 0 and alerts.stdout.strip():
            return
        time.sleep(1)
    pytest.fail("attack simulation did not produce a Suricata alert")
