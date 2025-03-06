from pycsp3 import *


def varArr_2_arrTup(x1:VarArray, x2:VarArray):
    matrix1 = values(x1)
    matrix2 = values(x2)
    new_arr_tup = []
    n = len(matrix1) 
    for i in range (n):
        new_arr = []
        for j in range (n):
            new_arr += [(matrix1[i][j],matrix2[i][j])]
        new_arr_tup += [new_arr]
    return new_arr_tup


def solve_tapestry(clues: list[list[(int, int)]]) -> list[list[(int, int)]]:
    print(clues)
    
    row_size = len(clues)
    column_size = len(clues[0])


    x1  = VarArray(size=[row_size, column_size], dom=range(0,column_size+1))
    x2 = VarArray(size=[row_size, column_size], dom=range(0,column_size+1))
    
    
    satisfy(
    # constraints 1 -  Unique on row
    [AllDifferent(x1[i,:]) for i in range(row_size)],
    [AllDifferent(x2[i,:]) for i in range(row_size)],
    
    # constraints 2 - Unique on column
    [AllDifferent(x1[:,j]) for j in range(row_size)],
    [AllDifferent(x2[:,j]) for j in range(row_size)],
    
    # constraints 3 - Tuples unique 
    # J'ai pas encore la contriante 
    #[AllDifferent(x1[i][j], x2[i][j]) for i in range(row_size) for j in range(column_size)],
    
    # constraints 4 - respect clue
    [x1[i][j] == clues[i][j][0] for i in range(row_size) for j in range(column_size) if clues and clues[i][j][0] > 0],
    [x2[i][j] == clues[i][j][1] for i in range(row_size) for j in range(column_size) if clues and clues[i][j][1] > 0],    
    )
    
    
    if solve(solver=CHOCO) is SAT:
        print("SATISFIABLE")
        print(values(x1))
        print(values(x2))
        solution = varArr_2_arrTup(x1,x2)
        print(solution)
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


'''
def solve_tapestry_bis(clues: list[list[(int, int)]]) -> list[list[(int, int)]]:
    row_size = len(clues)
    column_size = len(clues[0])


    x = VarArray(size=[row_size, column_size], dom=lambda i, j: [(a, b) for a in range(1, column_size+1) for b in range(1, column_size+1)])
    
    satisfy(
    # constraints 1
    [AllDifferent(x[i,:][0]) for i in range(row_size)],
    # constraints 2
    [AllDifferent(x[i,:]) for i in range(row_size)],
    # constraints 3
    [AllDifferent(x[:, j]) for j in range(column_size)],
    # constraints 4
    [AllDifferent(x[:, j]) for j in range(column_size)],
    # constraints 5
    [AllDifferent(x[i][j]) for i in range(row_size) for j in range(column_size)],
    AllDifferent(x),
    # constraints 6
    [x[i][j] == clues[i][j] for i in range(row_size) for j in range(column_size) if clues and clues[i][j] != (0,0)]
    )


    if solve(solver=CHOCO) is SAT:
        print("SATISFIABLE")
        print(values(x))
    else:
        print("UNSATISFIABLE")
    
    return None
'''



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

