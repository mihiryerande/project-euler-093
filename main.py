# Problem 93:
#     Arithmetic Expressions
#
# Description:
#     By using each of the digits from the set, {1, 2, 3, 4}, exactly once,
#       and making use of the four arithmetic operations (+, −, *, /) and brackets/parentheses,
#       it is possible to form different positive integer targets.
#
#     For example,
#          8 = (4 * (1 + 3)) / 2
#         14 = 4 * (3 + 1 / 2)
#         19 = 4 * (2 + 3) − 1
#         36 = 3 * 4 * (2 + 1)
#
#     Note that concatenations of the digits, like 12 + 34, are not allowed.
#
#     Using the set, {1, 2, 3, 4},
#       it is possible to obtain thirty-one different target numbers of which 36 is the maximum,
#       and each of the numbers 1 to 28 can be obtained before encountering the first non-expressible number.
#
#     Find the set of four distinct digits, a < b < c < d,
#       for which the longest set of consecutive positive integers, 1 to n, can be obtained,
#       giving your answer as a string: abcd.

from itertools import combinations, permutations, product
from operator import add, mul, sub, truediv
from typing import List, Tuple


def main() -> Tuple[Tuple[int, int, int, int], int, List[str]]:
    """
    Determines the set of 4 distinct digits (from 1 to 9)
      which allows for the formation of the longest set of consecutive positive integers, 1 to `n`,
      using arithmetic operations (+,-,*,/) and brackets/parentheses.
    Also returns the value of `n` itself, as well as
      the arithmetic expressions (as readable strings) producing each consecutive target.

    Returns:
        (Tuple[Tuple[int, int, int, int], int, List[str]]):
            Tuple of ...
              * 4-tuple of the distinct digits a,b,c,d (in order)
              * Greatest consecutive integer target `n` reached by those digits
              * List of arithmetic expressions (as readable strings) producing each target.
    """

    # Strategy:
    #     Brute-force through all possible choices of digits, operations, and parentheses.
    #     Simply need to do this in a systematic way ...
    #       * Consider all combinations set of 4 of the 9 digits
    #         * Construct all possible arithmetic expressions
    #         * Compute values and keep track of positive integer results,
    #             as well as expressions producing them
    #         * Determine the greatest consecutive target `n` that was produced
    #       * Return the combination which produced the greatest `n`

    # Idea 1:
    #     There are 9 total digits to choose from (1 through 9).
    #     The number of ways to select a combination of 4 digits from them is:
    #         (9 choose 4) = 126

    # Idea 2:
    #     As all the possible arithmetic operations (+,-,*,/) are binary operations,
    #       which each input two operands and produce one (decrease operand count by 1),
    #       then any arithmetic expression will use 3 operators.
    #     There are 4 possible operators,
    #       so the number of combinations of 3 of these (allowing for replacement) is:
    #         4 ^ 3 = 64

    # Idea 3a:
    #     Consider some arithmetic expression lacking parentheses,
    #       which would look like:
    #         a # b # c # d     ('#' represents any of the binary operations)
    #
    #     Adding parentheses is akin to choosing the order in which the operations get used,
    #       for example op2 -> op1 -> op3.
    #     There are then 3! = 6 such orders of operation
    #     However, 2 of these, both resulting in the expression ((a # b) # (c # d)), are equivalent.
    #     So there are actually 5 different orders of operation.

    # Idea 3b:
    #    Another way to consider parentheses in the expression would be to instead use
    #      Polish notation [https://en.wikipedia.org/wiki/Polish_notation].
    #
    #    The possible valid orderings of tokens would then still produce 5 possibilities:
    #
    #        [ #, #, #, a, b, c, d ]
    #        [ #, #, a, #, b, c, d ]
    #        [ #, #, a, b, #, c, d ]
    #        [ #, a, #, #, b, c, d ]
    #        [ #, a, #, b, #, c, d ]
    #
    #    Since there are only 5 different expressions that can be formed once the digits and operations are fixed,
    #      we will simply hardcode them as described in Idea 3b.

    # Idea 4:
    #     Counting up all the previous numbers:
    #       -> Digit combinations       = (9 choose 4) = 126
    #       -> Permutations of digits   = 4!           =  24
    #       -> Operation combinations   = 4 ^ 3        =  64
    #       -> Parentheses combinations = 3! - 1       =   5
    #
    #     Overall number of expressions that can be formed is:
    #         126 * 24 * 64 * 5 = 967,680
    #
    #     Not terrible!

    digits_all = [i+1 for i in range(9)]
    ops_all = [add, mul, sub, truediv]
    op_strs = {
        add: '+',
        mul: '*',
        sub: '-',
        truediv: '/',
    }

    # Best seen so far
    digits_best = (0, 0, 0, 0)
    t_best = 0
    expressions_best = []

    for digit_set in combinations(digits_all, 4):
        # Keep track of positive integer targets,
        #   as well as one of the expressions which produced it
        targets_by_expression = dict()

        # Run through all possible arithmetic expressions with these digits
        for a, b, c, d in permutations(digit_set):
            for op1, op2, op3 in product(ops_all, repeat=3):
                # Hardcode the 5 possible parentheses orderings
                # Won't be pretty but whatever ...

                # (((a . b) . c) . d)
                # op1 -> op2 -> op3
                try:
                    target = op3(op2(op1(a, b), c), d)
                    if target not in targets_by_expression and int(target) == target and target > 0:
                        targets_by_expression[int(target)] =\
                            '(({a} {op1} {b}) {op2} {c}) {op3} {d}'.format(
                                a=a, b=b, c=c, d=d, op1=op_strs[op1], op2=op_strs[op2], op3=op_strs[op3])
                    else:
                        pass
                except ZeroDivisionError:
                    pass

                # ((a . b) . (c . d))
                # op1 -> op3 -> op2
                # op3 -> op1 -> op2
                try:
                    target = op2(op1(a, b), op3(c, d))
                    if target not in targets_by_expression and int(target) == target and target > 0:
                        targets_by_expression[int(target)] = \
                            '({a} {op1} {b}) {op2} ({c} {op3} {d})'.format(
                                a=a, b=b, c=c, d=d, op1=op_strs[op1], op2=op_strs[op2], op3=op_strs[op3])
                    else:
                        pass
                except ZeroDivisionError:
                    pass

                # ((a . (b . c)) . d)
                # op2 -> op1 -> op3
                try:
                    target = op3(op1(a, op2(b, c)), d)
                    if target not in targets_by_expression and int(target) == target and target > 0:
                        targets_by_expression[int(target)] = \
                            '({a} {op1} ({b} {op2} {c})) {op3} {d}'.format(
                                a=a, b=b, c=c, d=d, op1=op_strs[op1], op2=op_strs[op2], op3=op_strs[op3])
                    else:
                        pass
                except ZeroDivisionError:
                    pass

                # (a . ((b . c) . d))
                # op2 -> op3 -> op1
                try:
                    target = op1(a, op3(op2(b, c), d))
                    if target not in targets_by_expression and int(target) == target and target > 0:
                        targets_by_expression[int(target)] = \
                            '{a} {op1} (({b} {op2} {c}) {op3} {d})'.format(
                                a=a, b=b, c=c, d=d, op1=op_strs[op1], op2=op_strs[op2], op3=op_strs[op3])
                    else:
                        pass
                except ZeroDivisionError:
                    pass

                # (a . (b . (c . d)))
                # op3 -> op2 -> op1
                try:
                    target = op1(a, op2(b, op3(c, d)))
                    if target not in targets_by_expression and int(target) == target and target > 0:
                        targets_by_expression[int(target)] = \
                            '{a} {op1} ({b} {op2} ({c} {op3} {d}))'.format(
                                a=a, b=b, c=c, d=d, op1=op_strs[op1], op2=op_strs[op2], op3=op_strs[op3])
                    else:
                        pass
                except ZeroDivisionError:
                    pass

        # Get length of consecutive target chain
        t = 1
        while t in targets_by_expression:
            t += 1
        t -= 1

        # Update best
        if t > t_best:
            digits_best = digit_set
            t_best = t
            expressions_best = [targets_by_expression[i+1] for i in range(t)]
        else:
            continue

    return digits_best, t_best, expressions_best


if __name__ == '__main__':
    digit_choosing, greatest_consecutive_target, arithmetic_expressions = main()
    print('Set of 4 digits producing longest consecutive chain of arithmetic expressions targets:')
    print('  digits = {}'.format(' < '.join(map(str, digit_choosing))))
    print('Greatest consecutive value reached (1 to `n`):')
    print('  n = {}'.format(greatest_consecutive_target))
    print('Expressions producing targets:')
    for expression_target, arithmetic_expression in enumerate(arithmetic_expressions):
        print('  {:2d} = {}'.format(expression_target+1, arithmetic_expression))
