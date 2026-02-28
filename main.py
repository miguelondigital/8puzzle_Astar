import random
import sys
import heapq
import time

#define goal state
GOAL = [[0,1,2],[3,4,5],[6,7,8]]

#define node for A* search
class Node:
    def __init__(self, board, heuristic, parent = None, action= None):
        self.parent = parent
        self.action = action
        self.board = board
        self.heuristic = heuristic
        #define g(n) as cost so far
        if( self.parent != None):
            self.g = parent.g + 1
        else:
            self.g = 0

    #determine h according to appropriate heuristic
    def h(self):
        if(self.heuristic == 1):
            h_val = num_misplaced(self.board)
        else:
            h_val = manhattan_distance(self.board)
        return h_val
     
    #calculate f(n) = g(n) + h(n)
    def f(self):
        return self.g + self.h()

#function to calculate heuristic 1
def num_misplaced(board):
    total = 0
    for i in range(3):
        for j in range(3):
            current = board[i][j]
            if current != GOAL[i][j] and current!= 0:
                total += 1
    return total

#function to calculate heuristic 2
def manhattan_distance(board):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = board[i][j]
            if val != 0:
                goal_row = val // 3
                goal_col = val % 3
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance


#function to handle manual input
#enables us to read manual boards in the multi line format
# press enter followed by command d or contorl d to conclude input
def manual_input():
    msg = sys.stdin.readlines()
    #create new board to append values to
    new_board = [[0]*3 for i in range (3)]
    row = 0
    for line in msg:
        col = 0
        line = line.split()
        for num in line:
            num = int(num)
            new_board [row][col] = num
            col += 1
        row += 1
    return new_board

#function to print board
def display_board(board):
    for i in range (3):
        printable = ""
        for j in range(3):
            printable += str(board[i][j])
            printable += " "
        print(printable)

#function to locate the index of the empty slot in puzzle
def find_blank(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return (i, j)
            else:
                continue

def find_moves(blank_index):
    # blank_index = find_blank(board)
    valid_moves = []
    #check up, down, left, right as valid moves
    if (blank_index[0] - 1 >= 0):
        valid_moves.append("up")
    if(blank_index[0] + 1 <= 2):
        valid_moves.append("down")

    if(blank_index[1] - 1 >= 0):
        valid_moves.append("left")
    if(blank_index[1] + 1 <= 2):
        valid_moves.append("right")

    return(valid_moves)

#function to generate all possible children given a set of valid moves
def spawn_children(board, moves, empty_index):
    children = []
    for item in moves:
        new_board = [[0]*3 for i in range (3)]
        for i in range(3):
            for j in range(3):
                new_board[i][j] = board[i][j]
        if item == "left":
            swap_placeholder = board[empty_index[0]][empty_index[1]-1]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]][empty_index[1]-1] = 0
        
        if item == "right":
            swap_placeholder = board[empty_index[0]][empty_index[1]+1]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]][empty_index[1]+1] = 0

        if item == "up":
            swap_placeholder = board[empty_index[0]-1][empty_index[1]]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]-1][empty_index[1]] = 0
        
        if item == "down":
            swap_placeholder = board[empty_index[0]+1][empty_index[1]]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]+1][empty_index[1]] = 0

        children.append((item, new_board))
    return children

#convert 2D array representation of board into a hashable element and return
def hash_board(board):
    #convert array into tuple of tuples (hashable)
    tuple_board = tuple(map(tuple,board))
    hash_board = hash(tuple_board)
    return hash_board

#returns solution path from goal node back to beginning
def get_path(node):
    path = []
    while node.parent is not None:
        path.append(node.board)
        node = node.parent
    path.reverse()
    return path

#main A* method for informed search
def a_star(node):
    search_cost = 0
    #counter will serve as a tiebraker in the event of an equivalent f() for two nodes
    counter = 0
    frontier = []
    explored_set = set()

    #pass in parent node into frontier
    heapq.heappush(frontier,(node.f(), counter, node))
    counter += 1

    #begin A* loop
    while (len(frontier) != 0):
        ntuple = heapq.heappop(frontier)
        current_node = ntuple[2]
        current_board = current_node.board
        board_id = hash_board(current_board)

        #skip board if already in explored
        if board_id in explored_set:
            continue

        #mark as explored and add to search cost
        explored_set.add(board_id)
        search_cost += 1

        #check if this board is a success before proceeding
        if current_board == GOAL:
            return(current_node, search_cost)
        
        #expand children
        blank = find_blank(current_board)
        moves = find_moves(blank)
        children = spawn_children(current_board, moves ,blank)

        for child in children:
            child_move = child[0]
            child_board = child[1]
            #check if child in explored set
            child_id = hash_board(child_board)

            if child_id not in explored_set:
                child_node = Node(child_board, current_node.heuristic, current_node, child_move)
                heapq.heappush(frontier,(child_node.f(), counter, child_node))
                counter += 1
    
    #reach this point if no solution is found
    print("no solution found")
    return None

#function to determine whether or not board can be solved
def is_solveable(board):
    flat_board = []
    for i in range(3):
        for j in range(3):
            if (board[i][j] != 0):
                flat_board.append(board[i][j])
    inversions = 0
    for i in range(len(flat_board)):
        for j in range(i+1,len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1
    
    return inversions % 2 == 0

#function to randomize board:
def randomizer():
    while True:
        tiles = list(range(9))
        random.shuffle(tiles)
        board = [[0]*3 for i in range(3)]
        index = 0
        for i in range(3):
            for j in range(3):
                board[i][j] = tiles[index]
                index += 1
        if is_solveable(board):
            return board

#function to select heuristic and display results
def menu_print(board):
    selected_h = int(input("Select H Function: \n[1] H1\n[2] H2\n"))
    if selected_h == 1:
        node = Node(board,1)
    else:
        node = Node(board,2)

    result = a_star(node)
    if result:
        path = get_path(result[0])
        cost = result[1]
        print(f'Search cost: {cost}')
        print(f'Solution depth:{len(path)}')
        print("Path:")
        step_index = 1
        for item in path:
            print(f'Step {step_index}:')
            display_board(item)
            print("\n")
            step_index += 1
    else:
        print("Board is not solveable")

def main():
    # main entry point of the script
    print('CS 4200 Project 1\n')
    active = True

    while active:
        print("Select Input Method:")
        print("[1] - Random Board")
        print("[2] - Manual input")
        print("[3] - 100 Case Statistical test")
        print("[4] - Exit")

        selection = int(input())
        if selection == 1:
            random_b = randomizer()
            print("Random Board Selected: ")
            display_board(random_b)
            menu_print(random_b)
            

        elif selection == 2:
            print("Input Board: ")
            unsolved = manual_input()
            if is_solveable(unsolved):
                menu_print(unsolved)
            else:
                print("This Board is not solveable")       
        
        elif selection == 3:
            total_cost1 = 0
            total_cost2 = 0
            print("# | H1 Cost | H2 Cost | H1 Time | H2 Time")
            for i in range(100):
                random_board = randomizer()
                h1_node = Node(random_board,1)
                h2_node = Node(random_board,2)

                t1_start = time.time()
                sol1 = a_star(h1_node)
                t1_end = time.time()
                t1 = t1_end - t1_start

                t2_start = time.time()
                sol2 = a_star(h2_node)
                t2_end = time.time()
                t2 = t2_end - t2_start

                cost1 = sol1[1]
                cost2 = sol2[1]

                print(f'{i+1} | {cost1} | {cost2} | {t1:.4f}s | {t2:.4f}s ')
                total_cost1 += cost1
                total_cost2 += cost2

            print(f'Average H1 Cost: {total_cost1 / 100}')
            print(f'Average H2 Cost: {total_cost2 / 100}')


        elif selection == 4:
            print("Terminating")
            active = False

        else:
            print("Improper input, please try again: ")

if __name__ == "__main__":
    main()


