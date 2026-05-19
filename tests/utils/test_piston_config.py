import pytest

from open_r1.utils.competitive_programming.piston_client import _parse_piston_endpoints, _positive_int_from_env


def test_parse_piston_endpoints_trims_deduplicates_and_sorts():
    endpoints = _parse_piston_endpoints(" https://worker-b/api/ ,http://worker-a/api,http://worker-a/api/ ")
    assert endpoints == ["http://worker-a/api", "https://worker-b/api"]


@pytest.mark.parametrize("value", ["", "  ", ",,,"])
def test_parse_piston_endpoints_rejects_empty_lists(value):
    with pytest.raises(ValueError, match="at least one endpoint"):
        _parse_piston_endpoints(value)


def test_parse_piston_endpoints_rejects_missing_scheme():
    with pytest.raises(ValueError, match="http:// or https://"):
        _parse_piston_endpoints("worker.internal:3223/api/v2")


def test_positive_int_from_env_uses_default(monkeypatch):
    monkeypatch.delenv("PISTON_TEST_LIMIT", raising=False)
    assert _positive_int_from_env("PISTON_TEST_LIMIT", 3) == 3


def test_positive_int_from_env_reads_configured_value(monkeypatch):
    monkeypatch.setenv("PISTON_TEST_LIMIT", "7")
    assert _positive_int_from_env("PISTON_TEST_LIMIT", 3) == 7


@pytest.mark.parametrize("value", ["0", "-1"])
def test_positive_int_from_env_rejects_non_positive_values(monkeypatch, value):
    monkeypatch.setenv("PISTON_TEST_LIMIT", value)
    with pytest.raises(ValueError, match="greater than zero"):
        _positive_int_from_env("PISTON_TEST_LIMIT", 3)


def test_positive_int_from_env_rejects_non_integer_values(monkeypatch):
    monkeypatch.setenv("PISTON_TEST_LIMIT", "many")
    with pytest.raises(ValueError, match="must be an integer"):
        _positive_int_from_env("PISTON_TEST_LIMIT", 3)
