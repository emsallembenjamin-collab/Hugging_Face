import pytest

from open_r1.utils.competitive_programming.code_patcher import (
    fix_cpp_includes,
    fix_python3_imports,
    is_patchable,
    patch_code,
)


@pytest.mark.parametrize(
    ("language", "expected"),
    [
        ("python", True),
        ("python3", True),
        ("Python 3", True),
        ("PyPy 3-64", True),
        ("cpp", True),
        ("GNU C++17", True),
        ("rust", False),
    ],
)
def test_is_patchable_recognizes_supported_languages(language, expected):
    assert is_patchable(language) is expected


def test_patch_code_preserves_empty_submissions():
    assert patch_code("", "python") == ""
    assert patch_code(None, "cpp") is None


def test_patch_code_preserves_unknown_languages():
    source = "fn main() { println!(\"hello\"); }"
    assert patch_code(source, "rust") == source


def test_fix_cpp_includes_adds_standard_library_and_namespace():
    patched = fix_cpp_includes("int main() { cout << 1; }")
    assert patched.startswith("#include <bits/stdc++.h>\n")
    assert "using namespace std;" in patched


def test_fix_cpp_includes_avoids_redundant_namespace_for_qualified_code():
    patched = fix_cpp_includes("int main() { std::cout << 1; }")
    assert "using namespace std;" not in patched


def test_fix_python_replaces_legacy_collections_import():
    patched = fix_python3_imports("from collections import Mapping\nprint(Mapping)")
    assert "from collections.abc import Mapping" in patched


def test_fix_python_replaces_deprecated_gcd_import():
    patched = fix_python3_imports("from fractions import gcd\nprint(gcd(6, 4))")
    assert "from math import gcd" in patched
    assert "from fractions import gcd" not in patched


def test_fix_python_disables_integer_string_limit_once():
    patched = fix_python3_imports("print(int(input()))")
    assert patched.count("sys.set_int_max_str_digits(0)") == 1


def test_fix_python_does_not_duplicate_last_import():
    patched = fix_python3_imports("import json\nprint(json.dumps({}))")
    assert patched.count("import json") == 1


def test_fix_python_preserves_first_line_without_imports():
    patched = fix_python3_imports("value = 42\nprint(value)")
    assert patched.count("value = 42") == 1
    assert patched.endswith("value = 42\nprint(value)")


def test_fix_python_does_not_import_gcd_for_unrelated_identifier():
    patched = fix_python3_imports("gcd_result = 'not a function call'")
    assert "from math import gcd" not in patched


def test_fix_python_adds_math_for_qualified_legacy_gcd():
    patched = fix_python3_imports("import fractions\nprint(fractions.gcd(6, 4))")
    assert "import math" in patched
    assert "math.gcd(6, 4)" in patched

