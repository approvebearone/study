import importlib
import sys

import study_test


def test_greet_returns_hi():
    assert study_test.greet() == "hi"


def test_no_print_on_import(capsys):
    module_name = 'study_test'
    if module_name in sys.modules:
        del sys.modules[module_name]
    importlib.import_module(module_name)
    captured = capsys.readouterr()
    assert captured.out == ""
