import random


def print_assignment(assignment):
    for row in range(1, 10):
        row_values = [assignment.get(f"V{row}{col}", 0) for col in range(1, 10)]
        formatted_row = " | ".join(" ".join(map(str, row_values[i:i + 3])) for i in range(0, 9, 3))
        print(formatted_row)
        if row % 3 == 0 and row != 9:
            print("-" * 21)


class CSP:
    def __init__(self, Variables, Domains, Neighbors, assignment):
        self.variables = Variables
        self.domains = Domains
        self.neighbors = Neighbors
        self.assignment = assignment

    def is_consistent(self, Variable, assignment):
        for neighbor in self.neighbors[Variable]:
            if neighbor in assignment and not self.constraints(Variable,
                                                               assignment[Variable],
                                                               neighbor, assignment[neighbor]):
                return False
        return True

    def ac3(self):
        queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]

        while queue:
            (xi, xj) = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        for x in set(self.domains[xi]):
            if not any(self.constraints(xi, x, xj, y) for y in self.domains[xj]):
                print(f"this is i = {xi}, this is j = {xj}")
                print(f"for {xi} this is domain {self.domains[xi]}")
                print(f"for {xj} this is domain {self.domains[xj]}")
                self.domains[xi].remove(x)
                print(f"for {xi} this is domain after Removal of {x} : {self.domains[xi]}")
                revised = True
        return revised

    def backtracking_search(self, assignment=None):
        if assignment is None:
            assignment = {}
        if len(assignment) == len(self.variables):
            return assignment


        var = self.select_unassigned_variable(assignment)

        # Save domains state before assignment
        saved_domains = {v: self.domains[v].copy() for v in self.variables}

        if len(var) == 1:

            random.shuffle(self.domains[var[0]])

            for value in self.domains[var[0]]:
                new_assignment = assignment.copy()
                new_assignment[var[0]] = value

                if not self.is_consistent(var[0], new_assignment):
                    continue

                print(f"Assigning {var[0]} = {value}")
                print_assignment(new_assignment)

                # Reduce domains based on the new assignment
                self.domains[var[0]] = [value]  # Restrict domain to assigned value

                # Apply forward checking by removing the assigned value from neighbors' domains
                if self.forward_check(var[0], value) and self.ac3():
                    result = self.backtracking_search(new_assignment)
                    if result:
                        return result

                self.domains = {v: saved_domains[v].copy() for v in self.variables}

            return None

        else:
            success = True
            new_assignment = assignment.copy()
            for variable in var:
                value = self.domains[variable][0]
                new_assignment[variable] = value

                if not self.is_consistent(variable, new_assignment):
                    success = False
                    break

                if not self.forward_check(variable, value):
                    success = False
                    break

            if success and self.ac3():
                result = self.backtracking_search(new_assignment)
                if result:
                    return result

            self.domains = {v: saved_domains[v].copy() for v in self.variables}

            return None



    def forward_check(self, var, value):
        for neighbor in self.neighbors[var]:
            if neighbor not in self.assignment and value in self.domains[neighbor]:
                self.domains[neighbor].remove(value)
                if len(self.domains[neighbor]) == 0:
                    return False
        return True

    def select_unassigned_variable(self, assignment):
        # Get all unassigned variables
        unassigned_variables = [var for var in self.variables if var not in assignment]

        if not unassigned_variables:
            return None

        # Find variables with domain size 1
        single_domain_vars = [var for var in unassigned_variables if len(self.domains[var]) == 1]

        if single_domain_vars:
            return single_domain_vars

        min_var = min(unassigned_variables, key=lambda var: len(self.domains[var]))
        print(f"Selected variable {min_var} with smallest domain = {self.domains[min_var]}")
        return [min_var]  # Return as list for consistency

    def constraints(self, var1, val1, var2, val2):
        if var2 in self.neighbors[var1] and val1 == val2:
            return False
        return True


# Initial board setup
initial_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 5, 2, 8, 6, 1, 7, 9]
]

variables = [f"V{row}{col}" for row in range(1, 10) for col in range(1, 10)]

initial_assignment = {}
for row in range(1, 10):
    for col in range(1, 10):
        var = f"V{row}{col}"
        value = initial_board[row - 1][col - 1]
        if value != 0:
            initial_assignment[var] = value

domains = {}
for row in range(1, 10):
    for col in range(1, 10):
        var = f"V{row}{col}"
        value = initial_board[row - 1][col - 1]
        if value == 0:
            domains[var] = list(range(1, 10))
        else:
            domains[var] = [value]


neighbors = {}
for row in range(1, 10):
    for col in range(1, 10):
        var = f"V{row}{col}"
        row_neighbors = [f"V{row}{c}" for c in range(1, 10) if c != col]
        col_neighbors = [f"V{r}{col}" for r in range(1, 10) if r != row]
        subgrid_row_start = 3 * ((row - 1) // 3) + 1
        subgrid_col_start = 3 * ((col - 1) // 3) + 1
        subgrid_neighbors = [
            f"V{r}{c}"
            for r in range(subgrid_row_start, subgrid_row_start + 3)
            for c in range(subgrid_col_start, subgrid_col_start + 3)
            if (r, c) != (row, col)
        ]
        neighbors[var] = list(set(row_neighbors + col_neighbors + subgrid_neighbors))

sud = CSP(variables, domains, neighbors, initial_assignment)

if sud.ac3():
    solution = sud.backtracking_search(initial_assignment)
    if solution:
        print("Solution found:")
        print_assignment(solution)
        print(sud.domains)
    else:
        print("No solution found")
else:
    print("No solution found")
