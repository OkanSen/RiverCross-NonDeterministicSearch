"""
This program solves the river crossing problem of the cannibals and missionaries using NDS.
The homework consists of 6 missionaries, 6 cannibals, and a boat of 5 seats.
"""
import random

class Node(object):
    "our node class. used for nds search and to show the parent"

    def __init__(self, parent, state, depth):
        self.parent = parent
        self.state = state
        self.depth = depth

    "by using the new_states function, yields new child nodes with parent as self"

    def child_node(self):
        for state in self.state.new_states():
            yield Node(parent=self, state=state, depth=self.depth + 1)

    "used to obtain the solution. Adds nodes starting from the goal state and reverses the list at the end for the solution."

    def get_solution(self):
        solution = []
        node = self
        solution.append(node)
        while node.parent is not None:
            solution.append(node.parent)
            node = node.parent
        solution.reverse()
        return solution

    "checks for the state in the state_list"

class State(object):
    """
    Left side of the river is set to state '0' and right side of the river is set to state '1'
    """
    "constructor"

    def __init__(self, total_m, total_c, boat_size, missionary_num, cannibal_num, boat_place, move):
        self.total_missionaries = total_m
        self.total_cannibals = total_c
        self.boat_size = boat_size
        self.missionary_num = missionary_num
        self.cannibal_num = cannibal_num
        self.boat_place = boat_place
        self.move = move

    "prints the state"

    def __str__(self):
        return "{:s}, {:d} {:d} {:d}".format(self.move, self.missionary_num, self.cannibal_num, self.boat_place)

    "checks if the state is valid"

    def is_state_valid(self):
        if self.missionary_num < 0 or self.missionary_num > self.total_missionaries:
            return False
        if self.cannibal_num < 0 or self.cannibal_num > self.total_cannibals:
            return False
        if self.boat_place < 0 or self.boat_place > 1:
            return False
        if self.missionary_num < self.cannibal_num and self.missionary_num > 0:
            return False
        if self.missionary_num > self.cannibal_num and self.missionary_num < self.total_missionaries:
            return False
        else:
            return True

    "returns true if goal state is met, i.e. 0 0 1"

    def goal(self):
        return self.missionary_num == 0 and self.cannibal_num == 0 and self.boat_place == 1

    "yields new states by iterating on possible m and c values. moves the boat to the other side and checks for validity too"

    def new_states(self):
        if self.boat_place > 1 or self.boat_place < 0:
            print("""Boat is somewhere it cant be.
                  """)
        elif self.boat_place == 0:
            movement = "from left to right"
            boat_place = 1
            op = -1
        elif self.boat_place == 1:
            movement = "from right to left"
            boat_place = 0
            op = 1
        for x in range(self.total_missionaries):
            for y in range(self.total_cannibals):
                move = "Moved {:d} missionaries and {:d} cannibals {:s}".format(x, y, movement)
                new_state = State(self.total_missionaries, self.total_cannibals, self.boat_size,
                                  self.missionary_num + op * x, self.cannibal_num + op * y, boat_place, move)
                if x + y >= 1 and x + y <= self.boat_size and new_state.is_state_valid():
                    yield new_state

    "checks if two states are equal"

    def is_states_equal(self, state):
        if self.missionary_num == state.missionary_num:
            if self.cannibal_num == state.cannibal_num:
                if self.boat_place == state.boat_place:
                    return True
        return False


def does_state_exists(state_list, state_two):
    for state in state_list:
        if state.is_states_equal(state_two):
            return True
    return False
    "the nds search function. adds the node to queue randomly. then pops it and adds its child nodes."
    "If goal state is found get_solution is called"


def NDS(root_node):
    queue = []
    queue.append(root_node)
    iteration_check_list = []
    while True:
        if not len(queue):
            return None
        node = queue.pop(0)

        if does_state_exists(iteration_check_list, node.state):
            continue
        iteration_check_list.append(node.state)

        if node.state.goal():
            return (node.get_solution())

        for child_node in node.child_node():
            queue.insert(random.randint(0,len(queue)),child_node)

"checks for the solution of 6 each and boat capacity 5"
print()
begin_state = State(6, 6, 5, 6, 6, 0, "Initial State")
root_node = Node(parent=None, state=begin_state, depth=0)
sol = NDS(root_node)
for element in sol:
    print(str(element.state))

    """Output can vary depending on the random node selection
    due to the behaviour of """