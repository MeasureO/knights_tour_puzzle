import sys
def print_board():
    print(' ' * len(str(dim[1])) + (dim[0] * (len(place_holder) + 1) + 3) * '-')
    for i in range(dim[1] - 1, -1, -1):
        print(' ' * (len(str(dim[1])) - len(str(i + 1))), i + 1, '| ', sep='', end='')
        for j in range(dim[0]):
            print(board[i][j], end=' ')
        print('|')
    print(' ' * len(str(dim[1])) + (dim[0] * (len(place_holder) + 1) + 3) * '-')
    print(f"{' ' * len(str(dim[1]))}  ", end='')
    for i in range(1, dim[0] + 1):
        print(f"{' ' * (len(place_holder) - len(str(i)))}{i} ", end='')
    print('  ')

def input_dimension():
    while True:
        dimensions = input("Enter your board dimensions: ")
        try:
            dimensions = dimensions.split()
            X = int(dimensions[0])
            Y = int(dimensions[1])
            assert X > 0 and Y > 0
            return X, Y
        except Exception:
            print("Invalid dimensions!")
            continue
def input_starting_position():
    global x, y
    while True:
        position = input("Enter the knight's starting position: ")
        try:
            position = position.split()
            x = int(position[0]) - 1
            y = int(position[1]) - 1
            assert 1 <= len(position) <= 2 and 0 <= x <= dim[0] - 1 and 0 <= y <= dim[1] - 1
            break
        except Exception:
            print("Invalid position!")
            continue
    visited_squares.append((x, y))
    board[y][x] = ' ' * len(place_holder[:-1]) + 'X'

def input_next_position():
    global x, y
    last_x = x
    last_y = y
    while True:
        position = input("Enter your next move: ")
        try:
            position = position.split()
            x = int(position[0]) - 1
            y = int(position[1]) - 1
            assert 1 <= len(position) <= 2 and 0 <= x <= dim[0] - 1 and 0 <= y <= dim[1] - 1
            assert (abs(x - last_x) == 1 and abs(y - last_y)) or (abs(x - last_x) == 2 and abs(y - last_y) == 1)
            assert (x, y) not in visited_squares
            break
        except Exception:
            print("Invalid position!", end='')
            continue
    visited_squares.append((x, y))

    board[y][x] = ' ' * len(place_holder[:-1]) + 'X'
    print("Here are the possible moves:")
    knight_moves(x, y)
    board[y][x] = ' ' * len(place_holder[:-1]) + '*'

def is_possible(x, y):
    count = -1
    for i in [-2, -1, 1, 2]:
        for j in [-2, -1, 1, 2]:
            if 0 <= x + i <= dim[0] - 1 and 0 <= y + j <= dim[1] - 1:
                if (abs(i) == 2 and abs(j) == 1) or (abs(i) == 1 and abs(j) == 2):
                    count += 1
    return count
def knight_moves(x, y):
    for i in [-2, -1, 1, 2]:
        for j in [-2, -1, 1, 2]:
            if 0 <= x + i <= dim[0] - 1 and 0 <= y + j <= dim[1] - 1:
                if (abs(i) == 2 and abs(j) == 1) or (abs(i) == 1 and abs(j) == 2):
                    if (x + i,  y + j) not in visited_squares:
                        board[y + j][x + i] = ' ' * len(place_holder[:-1]) + str(is_possible(x + i, y + j))

    print_board()
    for i in [-2, -1, 1, 2]:
        for j in [-2, -1, 1, 2]:
            if 0 <= x + i <= dim[0] - 1 and 0 <= y + j <= dim[1] - 1:
                if (abs(i) == 2 and abs(j) == 1) or (abs(i) == 1 and abs(j) == 2):
                    if (x + i,  y + j) not in visited_squares:
                        board[y + j][x + i] = place_holder

def no_moves():
    moves = []
    for i in [-2, -1, 1, 2]:
        for j in [-2, -1, 1, 2]:
            if (abs(i) == 2 and abs(j) == 1) or (abs(i) == 1 and abs(j) == 2):
                if 0 <= x + i <= dim[0] - 1 and 0 <= y + j <= dim[1] - 1:
                    if (x + i, y + j) not in visited_squares:
                        moves.append((x + i, y + j))
    return not bool(len(moves))

def possible_moves(x, y, visited):
    possible_moves = []
    for i in [-2, -1, 1, 2]:
        for j in [-2, -1, 1, 2]:
            if 0 <= x + i <= dim[0] - 1 and 0 <= y + j <= dim[1] - 1:
                if (abs(i) == 2 and abs(j) == 1) or (abs(i) == 1 and abs(j) == 2):
                    if (x + i,  y + j) not in visited:
                        possible_moves.append((x + i, y + j))
    return possible_moves

def rec_solver(x, y, visited):
    if len(visited) == dim[0] * dim[1]:
        for i in range(dim[0] * dim[1]):
            cell = visited[i]
            board[cell[1]][cell[0]] = f"{' ' * (len(place_holder) - len(str(i + 1)))}{i + 1}"
        print_board()
        exit(0)
    possible = possible_moves(x, y, visited)

    for move in possible:
        visited.append(move)
        if not rec_solver(move[0], move[1], visited):
            del visited[visited.index(move):]
            continue
    return False

def rec_solver_check(x, y, visited):

    if len(visited) == dim[0] * dim[1]:
        return visited
    possible = possible_moves(x, y, visited)

    for move in possible:
        a = rec_solver_check(move[0], move[1], visited + [move])
        if a:
            return a
    return False

if __name__  == "__main__":
    solution = []
    flag = False
    sys.setrecursionlimit(100)
    visited_squares = []
    dim = input_dimension()
    place_holder = '_' * len(str(dim[0] * dim[1]))
    board = [[place_holder for j in range(dim[0])] for i in range(dim[1])]
    input_starting_position()
    while True:
        answer = input("Do you want to try the puzzle? (y/n): ")
        if answer == "y":
            answer = rec_solver_check(x, y, [(x, y)])
            if answer:
                #print("Here are the possible moves:")
                knight_moves(x, y)
                board[y][x] = ' ' * len(place_holder[:-1]) + '*'
                while True:
                    #print(visited_squares)
                    if no_moves():
                        if len(visited_squares) == dim[0] * dim[1]:
                            print("What a great tour! Congratulations!")
                            break
                        else:
                            print("\nNo more possible moves!")
                            print(f"Your knight visited {len(visited_squares)} squares!")
                            break
                    input_next_position()
            else:
                print("No solution exists!")
            break
        elif answer == "n":
            if rec_solver_check(x, y, [(x, y)]):
                print()
                print("Here's the solution!")
                rec_solver(x, y, [(x, y)])
            else:
                print("No solution exists!")
            break
        else:
            print("Invalid input!")
            continue






