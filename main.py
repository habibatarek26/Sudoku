import random

class CSP:
    def __init__(self, initial_assignment):
        self.initial_assignment = initial_assignment
        self.assignment = initial_assignment
        self.variables = [f"V{row}{col}" for row in range(1, 10) for col in range(1, 10)]
        self.solution_state = []  # List to store final states
        self.current_best_solution = None  # Track the best solution found so far

        # Add initial state
        self.solution_state.append(initial_assignment.copy())

        # Initialize domains based on initial assignment
        self.domains = {}
        for var in self.variables:
            if var in initial_assignment:
                self.domains[var] = [initial_assignment[var]]
            else:
                self.domains[var] = list(range(1, 10))

        # Initialize neighbors
        self.neighbors = {}
        for var in self.variables:
            row = int(var[1])
            col = int(var[2])

            # Row neighbors
            row_neighbors = [f"V{row}{c}" for c in range(1, 10) if c != col]

            # Column neighbors
            col_neighbors = [f"V{r}{col}" for r in range(1, 10) if r != row]

            # Subgrid neighbors
            subgrid_row_start = 3 * ((row - 1) // 3) + 1
            subgrid_col_start = 3 * ((col - 1) // 3) + 1
            subgrid_neighbors = [
                f"V{r}{c}"
                for r in range(subgrid_row_start, subgrid_row_start + 3)
                for c in range(subgrid_col_start, subgrid_col_start + 3)
                if (r, c) != (row, col)
            ]

            self.neighbors[var] = list(set(row_neighbors + col_neighbors + subgrid_neighbors))

    def is_final_assignment(self, var, assignment):
        """Check if an assignment is final (won't need to be changed)"""
        # Check if the assignment is consistent
        if not self.is_consistent(var, assignment):
            return False

        # Check if it's the only possible value in the domain
        if len(self.domains[var]) == 1:
            return True

        # Check if it's the only value that works with neighbors
        valid_values = 0
        for value in self.domains[var]:
            temp_assignment = assignment.copy()
            temp_assignment[var] = value
            if self.is_consistent(var, temp_assignment):
                valid_values += 1
                if valid_values > 1:
                    return False
        return valid_values == 1

    def assignment_to_string(self, assignment):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for var, value in assignment.items():
            row = int(var[1]) - 1
            col = int(var[2]) - 1
            board[row][col] = value
        return ''.join(''.join(str(cell) for cell in row) for row in board)

    def Solve(self):
        if self.ac3():
            solution = self.backtracking_search(self.initial_assignment)
            if solution:
                # Convert solution states to string format
                self.solution_state = [self.assignment_to_string(state) for state in self.solution_state]
                return self.solution_state
            return None
        return None

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
                self.domains[xi].remove(x)
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

                # Only add to solution_state if it's a final assignment
                if self.is_final_assignment(var[0], new_assignment):
                    # Store new state only if it's better than current best
                    if (self.current_best_solution is None or
                            len(new_assignment) > len(self.current_best_solution)):
                        self.current_best_solution = new_assignment.copy()
                        self.solution_state.append(new_assignment.copy())

                # Reduce domains based on the new assignment
                self.domains[var[0]] = [value]

                if self.forward_check(var[0], value) and self.ac3():
                    result = self.backtracking_search(new_assignment)
                    if result:
                        return result

                self.domains = {v: saved_domains[v].copy() for v in self.variables}

            return None

        else:
            success = True
            new_assignment = assignment.copy()
            final_assignments = []

            for variable in var:
                value = self.domains[variable][0]
                new_assignment[variable] = value

                if not self.is_consistent(variable, new_assignment):
                    success = False
                    break

                if not self.forward_check(variable, value):
                    success = False
                    break

                if self.is_final_assignment(variable, new_assignment):
                    final_assignments.append(variable)

            if success:
                # Add new state if we found any final assignments
                if final_assignments and (self.current_best_solution is None or
                                          len(new_assignment) > len(self.current_best_solution)):
                    self.current_best_solution = new_assignment.copy()
                    self.solution_state.append(new_assignment.copy())

                if self.ac3():
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
        unassigned_variables = [var for var in self.variables if var not in assignment]

        if not unassigned_variables:
            return None

        single_domain_vars = [var for var in unassigned_variables if len(self.domains[var]) == 1]

        if single_domain_vars:
            return single_domain_vars

        min_var = min(unassigned_variables, key=lambda var: len(self.domains[var]))
        return [min_var]

    def constraints(self, var1, val1, var2, val2):
        if var2 in self.neighbors[var1] and val1 == val2:
            return False
        return True


# Initial board setup
initial_board = [
    [0, 0, 0, 0, 3, 0, 4, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 2, 0],
    [8, 6, 0, 7, 0, 0, 0, 0, 0],
    [0, 4, 0, 0, 8, 0, 7, 0, 0],
    [0, 1, 0, 0, 2, 5, 0, 0, 3],
    [0, 0, 2, 1, 0, 0, 9, 0, 0],
    [9, 7, 0, 8, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0]
]

variables = [f"V{row}{col}" for row in range(1, 10) for col in range(1, 10)]

initial_assignment = {}
for row in range(1, 10):
    for col in range(1, 10):
        var = f"V{row}{col}"
        value = initial_board[row - 1][col - 1]
        if value != 0:
            initial_assignment[var] = value

sud = CSP(initial_assignment)
solution_states = sud.Solve()

print(solution_states)