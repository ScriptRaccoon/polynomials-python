"""
Tests for utils.py
"""
# pylint: disable=missing-function-docstring

from utils import remove_spaces, add_default_operator, parse_by_operators


def test_remove_spaces():
    assert remove_spaces("a b cd ") == "abcd"
    assert remove_spaces("") == ""


def test_add_operator():
    ops = ["+", "-"]
    assert add_default_operator("x", ops, "+") == "+x"
    assert add_default_operator("x + y", ops, "+") == "+x + y"
    assert add_default_operator("+ x + y", ops, "+") == "+ x + y"
    assert add_default_operator("- x + y", ops, "+") == "- x + y"


def test_parse_by_operators():
    ops = ["+", "-"]
    assert not parse_by_operators(" ", ops)
    assert parse_by_operators("+ x", ops) == [("+", "x")]
    assert parse_by_operators("x", ops, "+") == [("+", "x")]
    assert parse_by_operators("- x", ops) == [("-", "x")]
    assert parse_by_operators("- x", ops, "+") == [("-", "x")]
    assert parse_by_operators("+ x + y + z", ops) == [
        ("+", "x"),
        ("+", "y"),
        ("+", "z"),
    ]
    assert parse_by_operators("x + y + z", ops, "+") == [
        ("+", "x"),
        ("+", "y"),
        ("+", "z"),
    ]
    assert parse_by_operators("+ x - y - z", ops, "+") == [
        ("+", "x"),
        ("-", "y"),
        ("-", "z"),
    ]
    assert parse_by_operators("- x + y - z", ops, "+") == [
        ("-", "x"),
        ("+", "y"),
        ("-", "z"),
    ]
