def add_explicit_concat(regex):
    """
    Insert explicit concatenation operator '.' between tokens where needed.
    E.g., "ab" -> "a.b", "a*b" -> "a*.b", "(a)(b)" -> "(a).(b)"
    """
    result = []
    operators = set('|*+')
    length = len(regex)

    for i, char in enumerate(regex):
        result.append(char)
        if i + 1 < length:
            curr = char
            nxt = regex[i + 1]

            # Add concat if:
            # curr is not '(' and not '|'
            # next is not ')' and not '|' and not '*' and not '+'
            curr_is_left = (curr not in ('(', '|'))
            nxt_is_right = (nxt not in (')', '|', '*', '+'))

            if curr_is_left and nxt_is_right:
                result.append('.')

    return ''.join(result)


def to_postfix(regex):
    """
    Convert infix regex (with explicit concat '.') to postfix using
    the shunting-yard algorithm.
    """
    precedence = {'|': 1, '.': 2, '*': 3, '+': 3}
    output = []
    stack = []

    for char in regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # remove '('
        elif char in precedence:
            while (stack and stack[-1] != '(' and
                   stack[-1] in precedence and
                   precedence[stack[-1]] >= precedence[char]):
                output.append(stack.pop())
            stack.append(char)
        else:
            output.append(char)  # operand (literal character)

    while stack:
        output.append(stack.pop())

    return ''.join(output)


def parse_regex(regex):
    """
    Full pipeline: raw regex -> explicit concat -> postfix.
    Returns postfix string ready for Thompson's construction.
    """
    with_concat = add_explicit_concat(regex)
    postfix = to_postfix(with_concat)
    return postfix
