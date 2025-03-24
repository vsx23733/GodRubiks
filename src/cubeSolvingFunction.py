from rubiksCube import RubikCube

mapper = {
    "U": "red",
    "D": "orange",
    "F": "white",
    "B": "yellow",
    "L": "blue",
    "R": "green"
}

face_list = ["up", "down", "front", "back", "left", "right"]    # U, D, F, B, L, R

def get_neighbors(cube_state : dict, face_name : str, square_name_to_fetch : str):

    local_neighbors = {}
    face = cube_state[face_name]
    squares = {}
    for row_idx, row in enumerate(face):
        for square_name in row:
            col_idx = row.index(square_name)
            squares[square_name] = (row_idx, col_idx)
    
    for square_name, (row_idx, col_idx) in zip(squares.keys(), squares.values()):
        if square_name == square_name_to_fetch:
            if row_idx == 0 and col_idx == 0:
                neighbors_positions = {
                    "down": (row_idx+1, col_idx),
                    "right": (row_idx, col_idx+1)
                }
            elif row_idx == 0 and col_idx == 1:
                neighbors_positions = {
                    "down": (row_idx+1, col_idx),
                    "left": (row_idx, col_idx-1),
                    "right": (row_idx, col_idx+1)
                }
            elif row_idx == 0 and col_idx == 2:
                neighbors_positions = {
                    "down": (row_idx+1, col_idx),
                    "left": (row_idx, col_idx-1)
                }
            elif row_idx == 1 and col_idx == 0:
                neighbors_positions = {
                    "up": (row_idx-1, col_idx),
                    "down": (row_idx+1, col_idx),
                    "right": (row_idx, col_idx+1)
                }
            elif row_idx == 1 and col_idx == 1:
                neighbors_positions = {
                    "up": (row_idx-1, col_idx),
                    "down": (row_idx+1, col_idx),
                    "left": (row_idx, col_idx-1),
                    "right": (row_idx, col_idx+1)
                }
            elif row_idx == 1 and col_idx == 2:
                neighbors_positions = {
                    "up": (row_idx-1, col_idx),
                    "down": (row_idx+1, col_idx),
                    "left": (row_idx, col_idx-1)
                }
            elif row_idx == 2 and col_idx == 0:
                neighbors_positions = {
                    "up": (row_idx-1, col_idx),
                    "right": (row_idx, col_idx+1)
                }
            elif row_idx == 2 and col_idx == 1:
                neighbors_positions = {
                    "up": (row_idx-1, col_idx),
                    "left": (row_idx, col_idx-1),
                    "right": (row_idx, col_idx+1)
                }
            elif row_idx == 2 and col_idx == 2:
                neighbors_positions = {
                    "up": (row_idx-1, col_idx),
                    "left": (row_idx, col_idx-1)
                }            

            for direction, (n_row, n_col) in neighbors_positions.items():
                if 0 <= n_row < 3 and 0 <= n_col < 3:
                    local_neighbors[direction] = cube_state[face_name][n_row][n_col]
        else:
            continue

    return local_neighbors

def check_valid_white_cross(cube : RubikCube):

    # Here the idea is to make successive checks on the white face
    # 1. Check if the white face has a white cross
    # 2. Check if the neighbors of the ends of the cross have as neighbors the centers of their respective faces
    white_face = cube.white
    neighbors = ["green", "red", "blue", "orange"]
    face_mapper = {
        "G": "green",
        "R": "red",
        "B": "blue",
        "O": "orange",
        "W": "white",
        "Y": "yellow",
    } # Map the face name to the face id
    checks = []

    # Check if the white face has a white cross
    # Check the middle row
    for i in range(3):
        if white_face[i][1][0] == "W":
            checks.append(True)
        else :
            checks.append(False)
    # Check the middle column
    for i in range(3):
        if white_face[1][i][0] == "W":
            checks.append(True)
        else:
            checks.append(False)
    
    # Check if the neighbors of the ends of the cross have as neighbors the centers of their respective faces
    ends_white = [white_face[0][1], white_face[2][1], white_face[1][0], white_face[1][2]]
    ends = [cube.faces[neighbor][2][1] for neighbor in neighbors]
    for end in ends:
        face_id = end[0].capitalize()
        face = face_mapper[face_id] # Get the face name
        neighbors = get_neighbors(cube_state=cube.get_state()[0], face_name=face, square_name_to_fetch=end)
        if f"{face_id}5" in neighbors.values():
            checks.append(True)

    # Check if all the checks are True
    if all(checks):
        return True
    else:
        return False
    
def is_edge_correct(face : str, actual_state : dict, expected_state : dict):
    """
    This function checks if the edge of a given face is correct.
    We suppose that the expected state is the state of the edge of the face in the solved cube.
    If not the function needs to be adjusted according to the expected state.
    """
    # Check if the edge is correct
    checks = []
    for row in actual_state[face] : 
        for piece in row :
            piece_neighbors = get_neighbors(actual_state, face, piece)
            subchecks = []
            for i, neighbor in enumerate(list(piece_neighbors.values())):
                if neighbor[0] == piece[0]:
                    subchecks.append(True)
            checks.append(subchecks)

    num_correct_edges = 0

    for subchecks in checks:
        if len(subchecks) == 3 :
            if all(subchecks):
                num_correct_edges += 1
    
    if num_correct_edges == 4 : return True 
    else : return False

def is_corner_correct(face : str, actual_state : dict, expected_state : dict):
    """
    This function checks if the corner of a given face is correct.
    We suppose that the expected state is the state of the corner of the face in the solved cube.
    If not the function needs to be adjusted according to the expected state.
    """

    checks = []
    for row in actual_state[face]:
        for piece in row:
            piece_neighbors = get_neighbors(actual_state, face, piece)
            subchecks = []
            for i, neighbor in enumerate(list(piece_neighbors.values())):
                if neighbor[0] == piece[0]:
                    subchecks.append(True)
            checks.append(subchecks)

    num_correct_corners = 0

    for subchecks in checks:
        if len(subchecks) == 2 :
            if all(subchecks):
                num_correct_corners += 1

    if num_correct_corners == 4 : return True # A corner has only 2 neighbors with the same color
    else : return False

def ec_scoring(current_state : dict, end_state : dict):
    edge_score = sum(1 for face in current_state if not is_edge_correct(face, current_state, end_state))
    corner_score = sum(1 for face in current_state if not is_corner_correct(face, current_state, end_state))
    score = edge_score + corner_score
    return score

class Move:
    def __init__(self, face : str, num_rotations : int, is_clockwise : bool):
        self.face_to_move = face
        self.num_rotations = num_rotations
        self.is_clockwise = is_clockwise
    
    def execute(self, cube : RubikCube, is_row : bool):
        face_name = mapper[self.face_to_move[0].capitalize()]
        direction = 1 if self.is_clockwise else -1
        for _ in range(self.num_rotations):
            cube.rotate(face_name, row_index=0, is_row=is_row, direction=direction)

    def __str__(self):
        return f"Move {self.face_to_move} {self.num_rotations} times {'clockwise' if self.is_clockwise else 'anticlockwise'}"
    



def main():
    cube = RubikCube()
    end_state = cube.get_state()[0]
    start_state = cube.copy().scramble().get_state()[0]
    copy_cube = cube.copy().scramble()
    print("Terminal Visualization of the cube")
    print("===================================")
    print(cube)
    print("===================================")
    print("Terminal Visualization of the scrambled cube")
    print("===================================")
    print(copy_cube)
    print("EC Score between scrambled state and solved state")
    print(ec_scoring(start_state, end_state))


if __name__ == "__main__":
    main()