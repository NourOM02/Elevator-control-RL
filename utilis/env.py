import numpy as np
from itertools import product

class Elevator:

    def __init__(self, n_elevator = 1, n_floor = 5, h_floor = 6, speed = 3, \
                 capacity = 4, stop_time=2):
        """
        This function initializes the elevator object. with its different variables.

        Parameters
        ----------

        n_elevator: int 
            number of elevators in the building, in this case we suppose there is \
            only one elevator, to relax the problem.
        n_floor: int
            number of floors in the building
        h_floor: int
            height of the floor in meters.
        speed: int
            speed of the elevator in m/s
        capacity: int
            capacity of the elevator in number of people.
        stop_time: int
            sum of the intervals needed by the passengers to enter and exit the \
            elevator on a floor.
        """
        self.n_elevator = n_elevator
        self.n_floor = n_floor
        self.h_floor = h_floor
        self.speed = speed
        self.capacity = capacity
        self.stop_time = stop_time
        self.states = set()

    def get_states(self):
        """
        This function returns the state of the elevator.

        A state x is defined by a tuple (c(1), ..., c(n_floor), p, v, o) where:
            c(i), i = 1, 2, ..., n_floor : Binary values, representing call requests\
                  (call flags) on each floor i. (supposed everyone goes up)
            p: Discrete elevator position {0, 1, ..., n_floor}
            v: Discrete vertical velocity taking values in {-speed, 0, speed}
            o : Discrete elevator occupancy, taking values in {0, 1, ..., capacity}.
        """

        c_values = [0, 1]
        p_values = list(range(self.n_floor))
        v_values = [-self.speed, 0, self.speed]
        o_values = list(range(self.capacity + 1))

        # Create a list of all possible combinations
        combinations = list(product(c_values, repeat=self.n_floor-1))
        combinations = product(combinations, p_values, v_values, o_values)

        # Append states to the set of all possible states
        for combination in combinations:
            self.states.add(combination)

        return self.states
    
    def get_actions(self, state):
        """
        This function returns the action of the elevator.

        The elevator controller can choose among three discrete actions: {−1, 0, 1} \
        The −1 action accelerates the elevator downwards, 1 accelerates it upwards, \
        and 0 stops the elevator. such that :
            . The controller cannot choose the action 1 when the elevator is on the top\
            floor. Similarly, it cannot choose the action −1 when the elevator is on \
            the ground floor.
            . The elevator cannot switch directions during a single sample. This \
            means the 0 action must be taken between the 1 and −1 actions.
        """

        # Get the current state
        c, p, v, o = state

        # Initialize the list of possible actions
        actions = []

        # If the elevator is on the ground floor, it cannot go down
        if p == 0:
            actions = [0, 1]
        # If the elevator is on the top floor, it cannot go up
        elif p == self.n_floor - 1:
            actions = [0, -1]