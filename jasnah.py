#!/usr/bin/env python
import argparse
import readline
import sys

"""
Mathematical Anti-Telharsic Harfatum Septomin
"""


def apply_op(op, x, y):
    if op == '+':
        return x + y
    if op == '-':
        return x - y
    if op == '/':
        return x/(y*1.0)
    if op == '*':
        return x * y
    print("{} is not currently a supported operator :(.".format(op))


def apply_op_identity(op, x):
    if op == '+':
        return apply_op(op, x, 0)
    if op == '-':
        return apply_op(op, 0, x)
    if op == '/':
        return apply_op(op, 1, x)
    if op == '*':
        return apply_op(op, x, 1)


def resolve_list(L):
    op = L[0]
    args = L[1:]
    if len(args) == 1:
        return apply_op_identity(op, args[0])
    while len(args) > 1:
        x = args.pop(0)
        y = args.pop(0)
        args.insert(0, apply_op(op, x, y))
    return args[0]


def list_is_nested(L):
    for item in L:
        if isinstance(item, list):
            return True
    return False


def resolve_left_innermost(L, inner=None):
    """
    Given a nested list L:
        * Find the left-innermost nested list
        * Resolve it to a numeric value by applying resolve_list
        * Replace the nested list with the resolved value
        * Return L
    """
    if inner is None:
        inner = L

    for idx, item in enumerate(inner):
        """
        If we found a flat list, we know we've bottomed out.

        Replace the list with the resolved, numeric value
        and pass the modified containing list back to the caller.
        """
        if isinstance(item, list) and not list_is_nested(item):
            inner[idx] = resolve_list(item)
            return L
        if isinstance(item, list):
            return resolve_left_innermost(L, item)


def jasnah_eval(L, trace=False):
    """
    Given a list L where:
        * L[0] is an operator
        * L[> 0] will either be of type:
            * int _or_
            * float _or_
            * a list that also follows these rules

    If L is flat:
        apply resolve_list
    Else:
        Successively apply resolve_left_innermost until L is a flat list

    Examples:
    ========
    # Flat lists are immediately resolved
    L = ['+', 1, 2, 3]
    resolve_list(L)
    >> 6

    # List is nested -- apply resolve_left_innermost
    L = ['+', 1, 2, 3, ['-', 4, 5, 6], ['*', 7, 8]]
    resolve_left_innermost(L)
    >> ['+', 1, 2, 3, -7, ['*', 7, 8]]
    # List is nested -- apply resolve_left_innermost
    L = ['+', 1, 2, 3, -7, ['*', 7, 8]]
    resolve_left_innermost(L)
    >> ['+', 1, 2, 3, -7, 56]
    # Flat lists are resolved
    L = ['+', 1, 2, 3, -7, 56]
    resolve_list(L)
    >> 55
    """
    if trace:
        print('# TRACE: {}'.format(L))
    if list_is_nested(L):
        return jasnah_eval(resolve_left_innermost(L), trace=trace)
    else:
        return resolve_list(L)


def tokenize(chars):
    '''
    Convert a string of characters into a list of tokens.
    Source: http://www.norvig.com/lispy.html
    '''
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens):
    '''
    Read an expression from a sequence of tokens.
    Source: http://www.norvig.com/lispy.html
    '''
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        try:
            return int(token)
        except:
            try:
                return float(token)
            except:
                return token


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="LISPy math REPL")
    parser.add_argument('--trace', required=False, action="store_true")
    args = parser.parse_args()

    while True:
        try:
            val = raw_input('jasnah=> ').lstrip().rstrip()
            if val is not None:
                print(jasnah_eval(read_from_tokens(tokenize(val)), trace=args.trace))
        except KeyboardInterrupt:
            print('')
        except EOFError:
            print("Be on your way now.")
            sys.exit(0)
