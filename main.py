import random
import sys
import heapq

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
        move = ""
        if item == "left":
            move = "left"
            swap_placeholder = board[empty_index[0]][empty_index[1]-1]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]][empty_index[1]-1] = 0
        
        if item == "right":
            move = "right"
            swap_placeholder = board[empty_index[0]][empty_index[1]+1]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]][empty_index[1]+1] = 0

        if item == "up":
            move = "up"
            swap_placeholder = board[empty_index[0]-1][empty_index[1]]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]-1][empty_index[1]] = 0
        
        if item == "down":
            move = "down"
            swap_placeholder = board[empty_index[0]+1][empty_index[1]]
            new_board[empty_index[0]][empty_index[1]] = swap_placeholder
            new_board[empty_index[0]+1][empty_index[1]] = 0
        move_pair = (move, new_board)
        children.append(move_pair)
    
    return children

#convert 2D array representation of board into a hashable element and return
def hash_board(board):
    #convert array into tuple of tuples (hashable)
    tuple_board = tuple(map(tuple,board))
    hash_board = hash(tuple_board)
    return hash_board

#main A* method for informed search
def a_star(node):
    current_board = node.board 
    search_cost = 0
    frontier = []
    explored_set = set()
    #pass in parent node into frontier
    heapq.heappush(frontier,(node.f(), node))
    search_cost += 1
    #begin A* loop
    while (len(frontier) != 0):
        ntuple = heapq.heappop(frontier)
        h_val = ntuple[0]
        parent_node = ntuple[1]
        parent_board = parent_node.board
        parent_hash = hash_board(parent_board)
        explored_set.add(parent_hash)

        #check if this board is a success before proceeding
        incorrect_placements = num_misplaced(parent_board)
        if incorrect_placements == 0:
            print("succesful")
            return (parent_node, search_cost)

        blank = find_blank(parent_board)
        moves = find_moves(blank)
        children = spawn_children(parent_board,moves,blank)

        for child in children:
            child_board = child[1]
            #check if child in explored set
            child_id = hash_board(child_board)

            if child_id in explored_set:
                continue
            else:
                #heuristic
                search_cost += 1
                hst = parent_node.heuristic
                child_node = Node(child_board,hst,parent_node, child[0])
                heapq.heappush(frontier,(child_node.f(), child_node))
                explored_set.add(child_id)



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
        unsolved = [[0]*3 for i in range (3)]
        if selection == 1:
            print("randomizing")

        elif selection == 2:
            print("Input Board: ")
            unsolved = manual_input() 
            # display_board(unsolved)
            empty = find_blank(unsolved)
            possible_m = find_moves(empty)
            test_list = spawn_children(unsolved,possible_m,empty)
            print(manhattan_distance(unsolved))
        
        elif selection == 3:
            print("will do later")

        elif selection == 4:
            print("Terminating")
            active = False

        else:
            print("Improper input, please try again: ")



if __name__ == "__main__":
    main()


