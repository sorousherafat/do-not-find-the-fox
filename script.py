from collections import defaultdict


# Reference: https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/more.html#distinct_permutations
def distinct_permutations(iterable):
    """Yield successive distinct permutations of the elements in *iterable*.

    Equivalent to yielding from ``set(permutations(iterable))``, except
    duplicates are not generated and thrown away. For larger input sequences
    this is much more efficient.

    Duplicate permutations arise when there are duplicated elements in the
    input iterable. The number of items returned is
    `n! / (x_1! * x_2! * ... * x_n!)`, where `n` is the total number of
    items input, and each `x_i` is the count of a distinct item in the input
    sequence.

    *iterable* need not be sortable, but note that using equal (``x == y``)
    but non-identical (``id(x) != id(y)``) elements may produce surprising
    behavior. For example, ``1`` and ``True`` are equal but non-identical:
    """

    # Algorithm: https://w.wiki/Qai
    items = list(iterable)
    size = len(items)
    items.sort()
    while True:
        # Yield the permutation we have
        yield tuple(items)

        # Find the largest index i such that items[i] < items[i + 1]
        for i in range(size - 2, -1, -1):
            if items[i] < items[i + 1]:
                break
        #  If no such index exists, this permutation is the last one
        else:
            return

        # Find the largest index j greater than j such that items[i] < items[j]
        for j in range(size - 1, i, -1):
            if items[i] < items[j]:
                break

        # Swap the value of items[i] with that of items[j], then reverse the
        # sequence from items[i + 1] to form the new permutation
        items[i], items[j] = items[j], items[i]
        items[i + 1 :] = items[: i - size : -1]  # items[i + 1:][::-1]


target = {"fox", "xof"}


def is_fox(board, one, two, three):
    return (
        1
        if f"{board[one[0]][one[1]]}{board[two[0]][two[1]]}{board[three[0]][three[1]]}"
        in target
        else 0
    )


def get_indices():
    for i in range(4):
        yield (i, 0), (i, 1), (i, 2)
        yield (i, 1), (i, 2), (i, 3)
        yield (0, i), (1, i), (2, i)
        yield (1, i), (2, i), (3, i)
    for i in range(2):
        for j in range(2):
            yield (i, j), (i + 1, j + 1), (i + 2, j + 2)
            yield (i, 3 - j), (i + 1, 2 - j), (i + 2, 1 - j)


def count_fox(board):
    return sum(is_fox(board, one, two, three) for (one, two, three) in indices)


def get_board_from_string(string):
    return [string[start : start + 4] for start in range(0, 16, 4)]


def get_boards():
    yield from (
        get_board_from_string(string)
        for string in (
            "".join(permutation)
            for permutation in distinct_permutations(f"{5 * 'f'}{6 * 'o'}{5 * 'x'}")
        )
    )


def print_result(result):
    total = sum(count for count in result.values())
    for count in sorted(result):
        print(f"probability of seeing fox {count} times: {result[count] / total}")


indices = list(get_indices())
result = defaultdict(lambda: 0)
for board in get_boards():
    result[count_fox(board)] += 1

print_result(result)
