from pycsp3 import *


def varArr_2_arrTup(x:VarArray):
    matrix = values(x)
    new_arr_tup = []
    n = len(matrix) 
    for i in range (n):
        new_arr = []
        for j in range (n):
            new_arr += [(matrix[i][j][0],matrix[i][j][1])]
        new_arr_tup += [new_arr]
    return new_arr_tup

def solve_tapestry(clues: list[list[(int, int)]]) -> list[list[(int, int)]]:
    print("clues are \n")
    for element in clues:
        print(element)
    row_size = len(clues)
    column_size = len(clues[0])
    n = row_size
    
    x = VarArray(size=[row_size, column_size, 2] , dom=range(1,column_size+1))    
    
    satisfy(
        # Constraint 1 - Row are different
        [AllDifferent(x[i,:,0]) for i in range(row_size)],
        [AllDifferent(x[i,:,1]) for i in range(row_size)],
        # Constraint 2 - Columun are different
        [AllDifferent(x[:,j,0]) for j in range(row_size)],
        [AllDifferent(x[:,j,1]) for j in range(row_size)],
        # Constraint 3 - in coming
        [x[i][j] != x[k][l] for i in range(n) for j in range(n) for k in range(n) for l in range(n) if (i!=k and j!=l)],
        # Constraint 4
        [x[i][j][0] == clues[i][j][0] for i in range(row_size) for j in range(column_size) if clues and clues[i][j][0] > 0],
        [x[i][j][1] == clues[i][j][1] for i in range(row_size) for j in range(column_size) if clues and clues[i][j][1] > 0]
    )

    if solve(solver=CHOCO) is SAT:
        print("SATISFIABLE")
        
        print("x is \n".format(values(x)))
        solution = varArr_2_arrTup(x)
        print("solution is :\n")
        for element in solution:
            print(element)
        return solution
         
    else:
        print("UNSATISFIABLE")
        return None


def verify_format(solution: list[list[(int, int)]], n: int):
    validity = True
    if (len(solution) != n):
        validity = False
        print("The number of rows in the solution is not equal to n")
    for i in range(len(solution)):
        if len(solution[i]) != n:
            validity = False
            print(f"Row {i} does not contain the right number of cells\n")
        for j in range(len(solution[i])):
            if (not isinstance(solution[i][j], tuple)):
                validity = False
                print(f"Cell in row {i} and column {j} is not a tuple\n")
            elif len(solution[i][j]) != 2:
                validity = False
                print(f"Cell in row {i} and column {j} does not contain the right number of values\n")
    return validity

def parse_instance(input_file: str) -> list[list[(int, int)]]:
    with open(input_file) as input:
        lines = input.readlines()
    n = int(lines[0].strip())
    clues = [[(0, 0) for i in range(n)] for j in range(n)]
    for line in lines[1:]:
        i, j, s, c = line.strip().split(" ")
        clues[int(i)][int(j)] = (int(s), int(c))
    return n, clues


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 tapestry.py instance_path")
        sys.exit(1)

    n, clues = parse_instance(sys.argv[1])
    
    solution = solve_tapestry(clues)
    if solution is not None:
        if (verify_format(solution, n)):
            print("Solution format is valid")
        else:
            print("Solution format is invalid")
    else:
        print("No solution found")

