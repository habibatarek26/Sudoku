import random
import time


def filter_states(states):
    final_state = states[-1]

    valid_states = []

    for state in states:
        valid = True
        for i in range(len(state)):
            if state[i] != '0' and state[i] != final_state[i]:
                valid = False
                break

        if valid:
            valid_states.append(state)

    return valid_states

class CSP:
    def __init__(self, initial_assignment):
        self.initial_assignment = initial_assignment
        self.assignment = initial_assignment
        self.variables = [f"V{row}{col}" for row in range(1, 10) for col in range(1, 10)]
        self.solution_state = []
        self.current_best_solution = None

        self.solution_state.append(initial_assignment.copy())

        self.domains = {}
        for var in self.variables:
            if var in initial_assignment:
                self.domains[var] = [initial_assignment[var]]
            else:
                self.domains[var] = list(range(1, 10))

        self.neighbors = {}
        for var in self.variables:
            row = int(var[1])
            col = int(var[2])

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

            self.neighbors[var] = list(set(row_neighbors + col_neighbors + subgrid_neighbors))

    def is_final_assignment(self, var, assignment):
        if not self.is_consistent(var, assignment):
            return False

        if len(self.domains[var]) == 1:
            return True

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
        start_time = time.time()
        if self.ac3():
            solution = self.backtracking_search(self.initial_assignment)
            print(f"Time taken: {time.time() - start_time:.2f} seconds")
            if solution:
                self.solution_state = [self.assignment_to_string(state) for state in self.solution_state]
                return filter_states(self.solution_state)
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

        saved_domains = {v: self.domains[v].copy() for v in self.variables}

        if len(var) == 1:

            random.shuffle(self.domains[var[0]])

            for value in self.domains[var[0]]:
                new_assignment = assignment.copy()
                new_assignment[var[0]] = value

                if not self.is_consistent(var[0], new_assignment):
                    continue

                self.domains[var[0]] = [value]

                if self.forward_check(var[0], value) and self.ac3():
                    self.solution_state.append(new_assignment.copy())
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
                self.solution_state.append(new_assignment.copy())
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


