import sys
import copy
from copy import deepcopy


# Domain is int 1-9, variables are the box and constraint is that all numbers must be different from the line and box
class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        puzzle = ""
        answer = []

        #Changing the puzzle into a string
        for i in range(0,9):
            for j in range(0,9):
                puzzle = puzzle + str(self.ans[i][j])
                j += 1
                if j == 9:
                    i += 1
                    j = 0
        
        sudoku = csp(grid=puzzle)
        solved = backtrackSearch(sudoku)
        answer = write(solved)
        answerlist = [[0 for i in range(9)] for j in range(9)]
        i,j = 0, 0

        #Changing the answer into the proper form to be printed to output.txt
        for number in answer:
            answerlist[i][j] = number
            j += 1
            if j == 9:
                i += 1
                j = 0
    
        return answerlist

class csp:   
    #Initialise the csp format
    def __init__ (self, domain = "123456789", grid = ""):
        digits =  cols = "123456789"
        rows = "ABCDEFGHI"
        squares = cross(rows,cols)
        self.variables = squares
        self.domain = self.getDict(grid)
        self.values = self.getDict(grid)        
        self.unitlist = ([cross(rows, c) for c in cols] +
                         [cross(r, cols) for r in rows] +
                         [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

        self.units = dict((s, [u for u in self.unitlist if s in u]) for s in squares)
        self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in squares)
        self.constraints = {(variable, peer) for variable in self.variables for peer in self.peers[variable]}

    #setting up the arc consistency
    def getDict(self, grid=""):
        digits =  cols = "123456789"
        rows = "ABCDEFGHI"
        i = 0
        values = dict()
        for cell in self.variables:
            if grid[i]!='0':
                values[cell] = grid[i]
            else:
                values[cell] = digits
            i = i + 1
        return values

def backtrackSearch(csp):
        return backtrack({}, csp)

#Formats the output
def write(values):
    digits =  cols = "123456789"
    rows = "ABCDEFGHI"
    squares = cross(rows,cols)
    output = ""
    for variable in squares:
        output = output + values[variable]
    return output

def cross(A, B):
    return [a + b for a in A for b in B]

def backtrack(assignment, csp):
        digits =  cols = "123456789"
        rows = "ABCDEFGHI"
        squares = cross(rows,cols)
        #checks if the puzzle is solved
        if set(assignment.keys())==set(squares):
            return assignment

        domain = deepcopy(csp.values)
        #get the next minimum remaining values possible variable
        unassigned_variables = dict((squares, len(csp.values[squares])) for squares in csp.values if squares not in assignment.keys())
        nextBestVariable = min(unassigned_variables, key=unassigned_variables.get)

        #assigning values from each variable domains
        for value in csp.values[nextBestVariable]:
            if checkPuzzle(nextBestVariable, value, assignment, csp):
                assignment[nextBestVariable] = value
                inferences = {}
                # Check for the inference, forwarch checking that will prune subsequent search branches
                inferences = Inference(assignment, inferences, csp, nextBestVariable, value)
                if inferences!= False:
                    result = backtrack(assignment, csp)
                    if result!=False:
                        return result

                #removing the value from the domain
                del assignment[nextBestVariable]
                csp.values.update(domain)
        return False

#Forward checking/constriant propogation
def Inference(assignment, inferences, csp, nextBestVariable, value):
    inferences[nextBestVariable] = value

    for neighbor in csp.peers[nextBestVariable]:
        if neighbor not in assignment and value in csp.values[neighbor]:
            if len(csp.values[neighbor])==1:
                return False

            remaining = csp.values[neighbor] = csp.values[neighbor].replace(value, "")

            if len(remaining)==1:
                flag = Inference(assignment, inferences, csp, neighbor, remaining)
                if flag==False:
                    return False

    return inferences
        
#Checks for the validity of the current state of the sudoku
def checkPuzzle(nextBestVariable, value, assignment, csp):
    for neighbor in csp.peers[nextBestVariable]:
        if neighbor in assignment.keys() and assignment[neighbor]==value:
            return False
    return True

def AC3(csp):
    q = queue.Queue()

    for arc in csp.constraints:
        q.put(arc)

    i = 0
    while not q.empty():
        (Xi, Xj) = q.get()

        i = i + 1 

        if Revise(csp, Xi, Xj):
            if len(csp.values[Xi]) == 0:
                return False

            for Xk in (csp.peers[Xi] - set(Xj)):
                q.put((Xk, Xi))

    #display(csp.values)
    return True 

#helper function
def cross(A, B):
    digits =  cols = "123456789"
    rows = "ABCDEFGHI"
    return [a + b for a in A for b in B]


if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python sudoku_A2_xx.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")
