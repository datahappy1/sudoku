"""sudoku generator"""
import random

CANDIDATES_ALL = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def get_rand_int_from_set(members_in, members_out):
    """
    get random integers from a given set
    :param members_in:
    :param members_out:
    :return:
    """
    return random.sample(members_in, members_out)


def sudoku_gen():
    """
    sudoku rows generator
    :return:
    """
    row_index = 1
    rows = []
    rows.append(get_rand_int_from_set(CANDIDATES_ALL, 9))
    squares = [[], [], [], [], [], [], [], [], []]
    while row_index < 9:
        row = []
        col_index = 0
        while col_index < 9:
            candidates_left = get_rand_int_from_set(CANDIDATES_ALL, 9)

            if row_index < 3 and col_index < 3:
                squares[0].extend(rows[row_index-1][0:3])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[0]) - set(list(map(list, zip(*rows)))[col_index]))
            elif row_index < 3 and 2 < col_index < 6:
                squares[1].extend(rows[row_index-1][3:6])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[1]) - set(list(map(list, zip(*rows)))[col_index]))
            elif row_index < 3 and 5 < col_index < 9:
                squares[2].extend(rows[row_index-1][6:9])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[2]) - set(list(map(list, zip(*rows)))[col_index]))
            elif row_index == 3:
                candidates_left = list(set(candidates_left) - set(row) - set(list(map(list, zip(*rows)))[col_index]))
            elif 3 < row_index < 6 and col_index < 3:
                squares[3].extend(rows[row_index-1][0:3])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[3]) - set(list(map(list, zip(*rows)))[col_index]))
            elif 3 < row_index < 6 and 2 < col_index < 6:
                squares[4].extend(rows[row_index-1][3:6])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[4]) - set(list(map(list, zip(*rows)))[col_index]))
            elif 3 < row_index < 6 and 5 < col_index < 9:
                squares[5].extend(rows[row_index-1][6:9])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[5]) - set(list(map(list, zip(*rows)))[col_index]))
            elif row_index == 6:
                candidates_left = list(set(candidates_left) - set(row) - set(list(map(list, zip(*rows)))[col_index]))
            elif 6 < row_index < 9 and col_index < 3:
                squares[6].extend(rows[row_index-1][0:3])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[6]) - set(list(map(list, zip(*rows)))[col_index]))
            elif 6 < row_index < 9 and 2 < col_index < 6:
                squares[7].extend(rows[row_index-1][3:6])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[7]) - set(list(map(list, zip(*rows)))[col_index]))
            elif 6 < row_index < 9 and 5 < col_index < 9:
                squares[8].extend(rows[row_index-1][6:9])
                candidates_left = list(set(candidates_left) - set(row) - set(squares[8]) - set(list(map(list, zip(*rows)))[col_index]))

            cell = int(get_rand_int_from_set(candidates_left, 1)[0]) if len(candidates_left) > 0 else 0

            if cell == 0:
                return -1

            row.append(cell)
            col_index = col_index + 1
        rows.append(row)
        row_index = row_index + 1

    return rows


def sudoku_mask(row):
    """
    sudoku row masker
    :param row:
    :return:
    """
    hidden = get_rand_int_from_set(CANDIDATES_ALL, 3)
    for hide in hidden:
        row[row.index(hide)] = '_'
    return row


def __main__():
    """
    the main function
    :return:
    """
    attempts = 1
    max_attempts = 5000
    while attempts <= max_attempts:
        try:
            output = sudoku_gen()
            for out in output:
                #print(*out)
                print(*sudoku_mask(out))
            break
        except TypeError:
            attempts = attempts + 1
            continue
        finally:
            if divmod(attempts, 1000)[1] == 1:
                print(f'attempts # {str(attempts - 1)}')
    else:
        print(f'no sudoku generated before reaching max attempts {max_attempts}')


__main__()
