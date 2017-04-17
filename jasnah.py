#!/usr/bin/env python
import readline

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
    raise ValueError("{} is not a supported operator :(.".format(op))


def apply_op_identity(op, x):
    if op in ('+', '-'):
        return apply_op(op, x, 0)
    if op == '/':
        return apply_op(op, 1, x)
    if op == '*':
        return apply_op(op, x, 1)


def process_list(l):
    op = l[0]
    args = l[1:]
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


def innermost(L):
    if not list_is_nested(L):
        return L
    else:
        for idx, item in enumerate(L):
            if isinstance(item, list):
                return innermost(L[idx])


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
            return token


def e(code_as_str):
    return process_list(read_from_tokens(tokenize(code_as_str)))

if __name__ == '__main__':
    "A prompt-read-eval-print loop."
    while True:
        val = raw_input('jasnah=> ').lstrip().rstrip()
        if val is not None:
            print(e(val))
