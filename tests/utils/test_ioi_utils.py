from unittest.mock import patch

import pytest

from open_r1.utils.competitive_programming.ioi_utils import (
    add_includes,
    load_ioi_tests,
    load_ioi_tests_for_year,
)


def test_add_includes_preserves_empty_code():
    assert add_includes("", "holiday") == ""
    assert add_includes(None, "holiday") is None


def test_add_includes_adds_problem_header_and_namespace():
    patched = add_includes("int solve() { return answer; }", "holiday")
    assert patched.startswith("#include <bits/stdc++.h>\n")
    assert '#include "holiday.h"' in patched
    assert "using namespace std;" in patched


def test_add_includes_does_not_duplicate_problem_header():
    source = '#include "holiday.h"\nint solve() { return 0; }'
    patched = add_includes(source, "holiday")
    assert patched.count('#include "holiday.h"') == 1


def test_add_includes_respects_qualified_standard_library_usage():
    patched = add_includes("std::vector<int> solve();", "holiday")
    assert "using namespace std;" not in patched


@pytest.fixture(autouse=True)
def clear_ioi_dataset_cache():
    load_ioi_tests_for_year.cache_clear()
    yield
    load_ioi_tests_for_year.cache_clear()


def test_load_ioi_tests_groups_cases_by_problem_and_name():
    rows = [
        {"problem_id": "holiday", "test_name": "sample.01", "test_input": "1", "test_output": "2"},
        {"problem_id": "holiday", "test_name": "sample.02", "test_input": "3", "test_output": "4"},
        {"problem_id": "game", "test_name": "sample.01", "test_input": "5", "test_output": "6"},
    ]
    with patch("open_r1.utils.competitive_programming.ioi_utils.load_dataset", return_value=rows) as loader:
        grouped = load_ioi_tests_for_year(2024)

    loader.assert_called_once_with("open-r1/ioi-test-cases", name="2024", split="train")
    assert grouped["holiday"]["sample.02"] == ("3", "4")
    assert grouped["game"]["sample.01"] == ("5", "6")


def test_load_ioi_tests_selects_requested_problem():
    rows = [{"problem_id": "holiday", "test_name": "sample", "test_input": "1", "test_output": "2"}]
    with patch("open_r1.utils.competitive_programming.ioi_utils.load_dataset", return_value=rows):
        assert load_ioi_tests(2024, "holiday") == {"sample": ("1", "2")}


def test_load_ioi_tests_reports_unknown_problem():
    with patch("open_r1.utils.competitive_programming.ioi_utils.load_dataset", return_value=[]):
        with pytest.raises(KeyError):
            load_ioi_tests(2024, "missing")
