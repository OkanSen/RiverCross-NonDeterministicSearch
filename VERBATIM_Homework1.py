"""
Created on Sat Feb 8 2021 - 13:28

Mastan Abdulkhaligli (CONTACT)
Okan Sen  21202377
Asadullah Farooqi
Nurlan Farzaliyev 21503756
Utku Baris Yuksek  21602412



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
        self.tot_num_missionaries = total_m
        self.tot_num_cannibals = total_c
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
        if self.cannibal_num < 0 or self.cannibal_num > self.tot_num_cannibals:
            return False
        if self.missionary_num > self.tot_num_missionaries or self.missionary_num < 0:
            return False
        if self.boat_place < 0 or self.boat_place > 1:
            return False
        if self.missionary_num < self.cannibal_num and self.missionary_num > 0:
            return False
        if self.missionary_num > self.cannibal_num and self.missionary_num < self.tot_num_missionaries:
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
            movement = "from the LEFT side to the RIGHT"
            boat_place = 1
            multiplier = -1
        elif self.boat_place == 1:
            movement = "from the RIGHT side to the LEFT"
            boat_place = 0
            multiplier = 1
        for x in range(self.tot_num_missionaries):
            for y in range(self.tot_num_cannibals):
                move = "Moved {:d} missionaries and {:d} cannibals {:s}".format(x, y, movement)
                new_state = State(self.tot_num_missionaries, self.tot_num_cannibals, self.boat_size,
                                  self.missionary_num + multiplier * x, self.cannibal_num + multiplier * y, boat_place, move)
                if x + y >= 1 and x + y <= self.boat_size and new_state.is_state_valid():
                    yield new_state

    "checks if two states are equal"

    def is_states_equal(self, state):
        if self.missionary_num == state.missionary_num and self.cannibal_num == state.cannibal_num and self.boat_place == state.boat_place:
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
    NDS_queue = []
    NDS_queue.append(root_node)
    traverse_checks = []
    while True:
        if not len(NDS_queue):
            return None
        node = NDS_queue.pop(0)

        if does_state_exists(traverse_checks, node.state):
            continue
        traverse_checks.append(node.state)

        if node.state.goal():
            return (node.get_solution())

        for child_node in node.child_node():
            NDS_queue.insert(random.randint(0,len(NDS_queue)),child_node)

"starts checking for a solution for the current problem "
"which consists of 6 cannbals and 6 missionaries with a boat of 5 seats"
print()


begin_state = State(6, 6, 5, 6, 6, 0, "Starting State")
root_node = Node(parent=None, state=begin_state, depth=0)
solution_arr = []

# This loop keeps calling NDS until it finds the most optimal solution, where the total number of crossings is 7
while True:
  solution_arr = NDS(root_node)
  if len(solution_arr) == 8:
      break

# print("The number of total crossings: 7")
for item in solution_arr:
  print(str(item.state))
print("The number of total crossings: 7")

"""Output can vary depending on the random node selection
due to the behaviour of Non Determinist search. However, 
our program can solve the problem in 7 steps. The solution
never uses the same states more than once, thus making it
loop-free.

Sample Result:
Starting State, 6 6 0
Moved 0 missionaries and 5 cannibals from the LEFT side to the RIGHT, 6 1 1\n
Moved 0 missionaries and 2 cannibals from the RIGHT side to the LEFT, 6 3 0
Moved 4 missionaries and 1 cannibals from the LEFT side to the RIGHT, 2 2 1
Moved 1 missionaries and 1 cannibals from the RIGHT side to the LEFT, 3 3 0
Moved 3 missionaries and 0 cannibals from the LEFT side to the RIGHT, 0 3 1
Moved 0 missionaries and 2 cannibals from the RIGHT side to the LEFT, 0 5 0
Moved 0 missionaries and 5 cannibals from the LEFT side to the RIGHT, 0 0 1
"""



