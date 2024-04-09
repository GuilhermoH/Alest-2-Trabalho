from os import system 
from time import sleep


def print_map(map, _row, _col, rows, cols, amount, total):
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

    system('clear')
    for row in range(rows - 1):
        for col in range(cols):
            if row == _row and col == _col:
                print(RED + BOLD + map[row][col] + END, end=' ')
            else:
                print(map[row][col], end=' ')
        print()

    print(f'amount: {amount if amount else "NULL"}')
    print(f'total : {total}')


def get_map(file):
    file = file.read().split('\n')
    rows, cols = file.pop(0).split()
    rows, cols = int(rows), int(cols)
    file.pop(0)

    return file, rows, cols
    

def is_valid_position(row, col, rows, cols):
    return 0 <= row < rows and 0 <= col < cols


def find_start(map, rows, cols):
    for row in range(rows):
        for col in range(cols):
            if map[row][col] == '#': return row, col


def initial_direction(map, row, col):
    right = map[row][col + 1]
    left = map[row][col - 1] 
    above = map[row - 1][col] 
    below =  map[row + 1][col]  

    if right == '-' or right.isnumeric(): return (0, 1)
    if left == '-' or left.isnumeric(): return (0, -1)
    if above == '|' or above.isnumeric(): return (-1, 0)
    if below == '|' or below.isnumeric(): return (1, 0)

def change_direction(direction, turn):
    return {
        (0, 1): { # >
            '/': (-1, 0), # ^
            '\\': (1, 0) # v
        },
        (-1, 0): { # ^
            '/': (0, 1), # >
            '\\': (0, -1) # <
        },
        (0, -1): { # <
            '/': (1, 0), # v
            '\\': (-1, 0) # ^
        }, 
        (1, 0): { # v
            '/': (0, -1), # <
            '\\': (0, 1) # >
        }
    }[direction][turn] 


def count_money(case):
    with open(case, 'r') as file:
        map, rows, cols = get_map(file) 
        row, col = find_start(map, rows, cols)
        direction = initial_direction(map, row, col)
        total = 0
        amount = ''

        while True:
            row += direction[0] 
            col += direction[1]

            # case invalid position
            if not is_valid_position(row, col, rows, cols):
                return total
            
            # print map if print-flag
            if print_flag:
                print_map(map, row, col, rows, cols, amount, total)
                sleep(0.2)
            
            value = map[row][col]

            # case - or |
            if value in ['-', '|'] and amount: 
                total, amount = total + int(amount), '' 

            # case / or \
            if value in ['/', '\\']:
                if amount: total, amount = total + int(amount), ''
                direction = change_direction(direction, value)

            # case [0-9]
            if value.isnumeric():
                amount =  value + amount
                

case_input = input('type the case number (ex: 50) -> ')
print_input = input('do you want to print the path? (y / n) -> ')
print_flag = print_input == 'y'

path = f'casoL{case_input}.txt'
print(f'total: {count_money(path)}')
