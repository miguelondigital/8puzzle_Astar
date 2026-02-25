import random

#define node for A* search
class Node:
    def __init__(self, puzzle, board, heuristic, parent = None, action= None):
        self.puzzle = puzzle
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
            return self.puzzle.misplaced
        else:
            return self.puzzle.manhattan
        
    #calculate f(n) = g(n) + h(n)
    def f(self):
        return self.g + self.h


        


# class board



#function to calculate heuristic 1
def num_misplaced():
    print('placeholder')

#function to calculate heuristic 2
def manhattan_distance():
    sum = 0

def main():
    # main entry point of the script
    print('CS 4200 Project 1\n')
    active = True

    while active:
        print("Select Input Method:")
        print("[1] - Random Board")
        print("[2] - Manual input")
        print("[3] - Exit")

        selection = int(input())

        if selection == 1:
            print("randomizing")
        elif selection == 2:
            print("Input Board: ")
        elif selection == 3:
            print("Terminating")
            active = False
        else:
            print("Improper input, please try again: ")



if __name__ == "__main__":
    main()
    




