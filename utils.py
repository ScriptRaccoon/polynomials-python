def remove_spaces(txt: str) -> str:
    """
    Removes all spaces inside of a string

    Arguments:
        txt: any string

    Returns:
        a string without spaces
    """
    return txt.replace(" ", "")


def parse_by_operators(
    txt: str, operators: list[str], default: str | None = None
) -> dict:
    """
    Parses a string by a list of unary operators.
    For example, the string "- x + y - z with the operators "+","-"
    returns the dictionary {"+": ["y"], "-": ["x", "z"]}.

    When a default operator is given, it is added to the start
    (when no other operator is present there). For example,
    "x + y - z" is processed in the same way as "+ x + y - z"
    when "+" is the default operator.

    Arguments:
        txt: any string
        operators: any list of string-encoded operators

    Returns:
        A dictionary whose keys are the operators and whose value
        at an operator is the list of substrings to which this operator
        has been applied in the given string
    """
    txt = remove_spaces(txt)
    if default:
        txt = add_default_operator(txt, operators, default)
    res: dict = {operator: [] for operator in operators}
    current = ""
    operator = None
    for index in range(len(txt)):
        char = txt[index]
        if char in operators:
            if operator:
                res[operator].append(current)
                current = ""
            operator = char
        else:
            current += char
    if operator:
        res[operator].append(current)
        current = ""
    return res


def add_default_operator(txt: str, operators: list[str], default: str) -> str:
    """
    Adds a default operator in front of a string, in case no operator is present there.

    For example, when + is the default operator, the other one being -,
    then x + y is transformed to + x + y, but + x + y and - x + y stay the same.

    Arguments:
        txt: any string
        operators: a list of operators
        default: a default operator

    Returns:
        the transformed string
    """
    if any([txt.lstrip().startswith(operator) for operator in operators]):
        return txt
    else:
        return default + txt
