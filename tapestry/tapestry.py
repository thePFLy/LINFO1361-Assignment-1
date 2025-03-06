from pycsp3 import *


def solve_tapestry(clues: list[list[(int, int)]]) -> list[list[(int, int)]]:
    # Put your code here
    row_size = len(clues)
    column_size = len(clues[0])

    x = VarArray(size=[row_size, column_size], dom=range(1, row_size))

    satisfy(
    # constraints 1
    [AllDifferent(x[i,:][0]) for i in range(row_size)],
    # constraints 2
    [AllDifferent(x[i,:][1]) for i in range(row_size)],
    # constraints 3
    [AllDifferent(x[:, j][0]) for j in range(column_size)],
    # constraints 4
    [AllDifferent(x[:, j][1]) for j in range(column_size)],
    # constraints 5
    [AllDifferent(x[i][j]) for i in range(row_size) for j in range(column_size)],
    # constraints 
    [x[i][j] == clues[i][j] for i in range(row_size) for j in range(column_size) if clues and clues[i] != (0,0) and clues[j] != (0,0)]
    )
    
    print(row_size, column_size)
    print(clues)
    print(x)

    if solve(solver=CHOCO) is SAT:
        print("SATISFIABLE")
        print(values(x))
    else:
        print("UNSATISFIABLE")

    return x

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

