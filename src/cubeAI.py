from cubeSolvingFunction import Move, get_neighbors, check_valid_white_cross, is_edge_correct, is_corner_correct, mapper
from rubiksCube import RubikCube
import random
import copy
from variables import *

def drop_from_list(elem, lst : list):
    list_buffer = lst.copy()
    if elem in lst:
        lst.remove(elem)
    return [elem for elem in lst if elem in list_buffer]

def add_to_list(elem, lst : list):
    lst.append(elem)
    return lst

def base_moves(front_face: str) -> list[Move]:
    """
    Base sequence to solve the white cross.

    The base sequence is the following:
    Right face clockwise, Top face clockwise, Right face counter clockwise, Top face clockwise
    2nd Col of front face clockwise, 1st row of the front face clockwise, 2nd col of the front face counter clockwise, 1st row of the front face clockwise
    """
    moves = [
        Move(face=front_face, num_rotations=1, is_clockwise=True),
        Move(face=front_face, num_rotations=1, is_clockwise=True),
        Move(face=front_face, num_rotations=1, is_clockwise=False),
        Move(face=front_face, num_rotations=1, is_clockwise=False)
    ]

    return moves

def generate_sequence(base_sequence: list[Move], drop_add : int, random_state : int) -> list[Move]:
    """
    Generate a sequence of moves based on a base sequence
    """
    if random_state <= 10 :
        face = random.choice(["F", "R", "L", "U", "D", "B"])
        dropping = random.choice([True, False])
        new_sequence = base_sequence.copy()

        if dropping:
            for _ in range(drop_add):
                new_sequence = drop_from_list(random.choice(new_sequence), new_sequence)
        else:
            for _ in range(drop_add):
                new_sequence = add_to_list(random.choice(new_sequence), new_sequence)
        
        for _ in range(drop_add):
            num_rotations = random.randint(1, 2)
            is_clockwise = random.choice([True, False])
            new_sequence.append(Move(face=face, num_rotations=num_rotations, is_clockwise=is_clockwise))

    elif random_state > 10:
        dropping = random.choice([True, False])
        new_sequence = base_sequence.copy()
        if dropping:
            for _ in range(drop_add):
                new_sequence = drop_from_list(random.choice(new_sequence), new_sequence)
        else:
            for _ in range(drop_add):
                new_sequence = add_to_list(random.choice(new_sequence), new_sequence)
        
        for _ in range(drop_add):
            num_rotations = random.randint(1, 2)
            is_clockwise = random.choice([True, False])
            face = random.choice(["F", "R", "L", "U", "D", "B"])
            new_sequence.append(Move(face=face, num_rotations=num_rotations, is_clockwise=is_clockwise))

    return new_sequence

def crossover(seq1 : list[Move], seq2 : list[Move]):
    point = random.randint(1, min(len(seq1), len(seq2)) - 1)
    child = seq1[:point] + seq2[point:]
    return child

def mutate(sequence : list[Move], mutation_rate : float) -> list[Move]:
    mutated_sequence = copy.deepcopy(sequence)
    for i in range(len(mutated_sequence)):
        if random.random() < mutation_rate:
            mutated_sequence[i] = Move(
                face=random.choice(["F", "R", "L", "U", "D", "B"]),
                num_rotations=random.randint(1, 2),
                is_clockwise=random.choice([True, False])
            )

    return mutated_sequence

def get_distance_between_states(state1 : dict, state2 : dict) -> int:
    """
    Compute the distance between two states of the cube
    """

    distance = 0
    for face in state1:
        for i in range(3):
            for j in range(3):
                if state1[face][i][j][0] != state2[face][i][j][0]:
                    distance += 1

    return distance

def ec_scoring(current_state : dict, end_state : dict):
    edge_score = sum(1 for face in current_state if not is_edge_correct(face, current_state, end_state))
    corner_score = sum(1 for face in current_state if not is_corner_correct(face, current_state, end_state))
    score = edge_score + corner_score
    return score

def cubies_scoring(current_state : dict, end_state : dict):
    cubie_score = 0
    for face in current_state:
        for i in range(3):
            for j in range(3):
                if current_state[face][i][j][0] != end_state[face][i][j][0]:
                    cubie_score += 1

    return cubie_score 

def genetic_algorithm(cube : RubikCube, start_state : dict, end_state : dict, 
                      drop_add : int, num_gen : int, fitness_func,
                      base_sequence : list[Move]) -> list:
    """
    Genetic algorithm to optimize the sequence of moves
    """
    n = 100
    gen_0 = [generate_sequence(base_sequence, drop_add, random_state=20) for _ in range(n)] # Generate n random sequences for the first generation
    gen_list = [gen_0]
    best_score = float("inf")
    best_sequence = None
    second_best_sequence = None
    for i in range(0, num_gen):
        distance_gen = [] # List of the distance between the end state and the current state for each sequence in the first generation
        print(f"Generation {i+1} : \n")

        for j, sequence in enumerate(gen_list[i]):
            print(f"Testing sequence {j+1} : ")
            copy_cube = cube.copy()
            for move in sequence:
                move.execute(copy_cube, is_row=True)

            current_state = copy_cube.get_state()[0]
            score_actual_end = fitness_func(current_state, end_state) # Compute the score of the current state
            print(f"Score after appying sequence {j+1} : {score_actual_end}")
            distance_gen.append(score_actual_end)

        distance_gen_duffer = copy.deepcopy(distance_gen)
        best_distance = min(distance_gen)
        best_idx = distance_gen.index(best_distance)
        distance_gen_duffer.remove(best_distance)
        second_best_distance = min(distance_gen_duffer)
        second_best_idx = distance_gen_duffer.index(second_best_distance) - 1


        if best_score > distance_gen[best_idx]:
            best_score = distance_gen[best_idx]
            best_sequence = gen_list[i][best_idx]
            second_best_sequence = gen_list[i][second_best_idx]
        
        best_sequence_mutated = crossover(best_sequence, second_best_sequence)
        #print("Child of best sequences are born : ")
        #print(best_sequence_mutated)
        new_gen = [mutate(generate_sequence(best_sequence_mutated, drop_add, random_state=distance_gen[distance_gen.index(best_distance)]), 0.1) for _ in range(n)] # Using the child of the 2 best sequences to generate the next generation
        gen_list.append(new_gen)
        print(f"Generation {i+1} best score: {best_distance}")
        #print(f"Generation {i+1} best sequence: {best_sequence}")
    winning_sequence = gen_list[-1][distance_gen.index(min(distance_gen))]
    return winning_sequence
    

class Neuron:

    def __init__(self, sequence : list[Move], occurence : int):
        self.sequence = sequence # Sequence of Moves that the neuron should perform  
        self.occurence = occurence # List of the number of times the sequence should be performed
        pass

    def execute_sequence(self, cube : RubikCube):
        for _ in range(self.occurence):
            for move in self.sequence:
                move.execute(cube, is_row=True)

class ChooseBestMoveAI():
    def __init__(self, start_state : dict, end_state : dict, cube : RubikCube):

        self.start_state = start_state
        self.end_state = end_state
        self.neurons = [] # One layer is one neuron
        self.cube = cube
        self.current_state = start_state

    def add_neuron(self, sequence: list[Move], occurence: int):
        self.neurons.append(Neuron(sequence, occurence))

    def compute_fitness(self, current_state : dict, end_state : dict, scoring_func=cubies_scoring):
        return scoring_func(current_state, end_state)

    def train(self, drop_add : int, num_gen : int, epochs : int):
        
        for epoch in range(epochs):
            best_fitness = float("inf")
            copy_cube = self.cube.copy()
            for neuron in self.neurons:
                neuron.execute_sequence(copy_cube)
                current_state = copy_cube.get_state()[0]
                self.start_state = current_state

                neuron.sequence = genetic_algorithm(copy_cube, self.start_state, self.end_state, drop_add, num_gen, fitness_func=self.compute_fitness, base_sequence=neuron.sequence)
                fitness = self.compute_fitness(copy_cube.get_state()[0], self.end_state)
                neuron.occurence = random.randint(1, 10 - fitness // 10)

                best_fitness = min(best_fitness, fitness)

            print(f"Epoch {epoch + 1}: Best Fitness = {best_fitness}")

            if best_fitness == 0:
                print("Solution found!")

    def execute(self):
        #print("Cube before applying the sequence of moves:")
        #print(self.cube.get_state())
        for i, neuron in enumerate(self.neurons):
            print(f"The cube is passing through the Neuron {i+1}")
            neuron.execute_sequence(self.cube)
            print(f"The cube has finished to pass through the Neuron {i+1}")
        
        #print(self.cube.get_state())

        return self.cube.get_state()

## Next step : Impove the Genetic Algorithm 
# Selection: Retain the top N performing sequences.
# Crossover: Combine parts of two sequences to create new ones.
# Mutation: Randomly modify sequences to maintain diversity

cube = RubikCube()
end_state = cube.get_state()[0]
#print(f"End state : \n{end_state}")
start_state = cube.copy().scramble().get_state()[0]
#print(f"Start state : \n{start_state}")
copy_cube = cube.copy().scramble()

# AI

bestMoveAI = ChooseBestMoveAI(start_state, end_state, copy_cube)
bestMoveAI.add_neuron(base_moves("F"), 2)
bestMoveAI.add_neuron(base_moves("U"), 2)
bestMoveAI.add_neuron(base_moves("D"), 1)
bestMoveAI.add_neuron(base_moves("B"), 1)

bestMoveAI.train(drop_add=2, num_gen=10, epochs=10)
bestMoveAI.execute()

