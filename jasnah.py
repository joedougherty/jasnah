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
    if inner is None:
        inner = L

    for idx, item in enumerate(inner):
        if isinstance(item, list) and not list_is_nested(item):
            inner[idx] = resolve_list(item)
            return L
        if isinstance(item, list):
            return resolve_left_innermost(L, item)


def jasnah_eval(L, trace=False):
    if trace:
        print('# TRACE: {}'.format(L))
    if list_is_nested(L):
        L = resolve_left_innermost(L)
        return jasnah_eval(L, trace=trace)
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
    "A prompt-read-eval-print loop."

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
