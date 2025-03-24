import matplotlib.pyplot as plt
import numpy as np
import random
import copy

class RubikCube:
    def __init__(self):

        self.white = [["W1", "W2", "W3"], ["W4", "W5", "W6"], ["W7", "W8", "W9"]]
        self.red = [["R1", "R2", "R3"], ["R4", "R5", "R6"], ["R7", "R8", "R9"]]
        self.blue = [["B1", "B2", "B3"], ["B4", "B5", "B6"], ["B7", "B8", "B9"]]
        self.orange = [["O1", "O2", "O3"], ["O4", "O5", "O6"], ["O7", "O8", "O9"]]
        self.green = [["G1", "G2", "G3"], ["G4", "G5", "G6"], ["G7", "G8", "G9"]]
        self.yellow = [["Y1", "Y2", "Y3"], ["Y4", "Y5", "Y6"], ["Y7", "Y8", "Y9"]]

        white_pixels = [["⬜", "⬜", "⬜"], ["⬜", "⬜", "⬜"], ["⬜", "⬜", "⬜"]]
        blue_pixels = [["🟦", "🟦", "🟦"], ["🟦", "🟦", "🟦"], ["🟦", "🟦", "🟦"]]
        red_pixels = [["🟥", "🟥", "🟥"], ["🟥", "🟥", "🟥"], ["🟥", "🟥", "🟥"]]
        orange_pixels = [["🟧", "🟧", "🟧"], ["🟧", "🟧", "🟧"], ["🟧", "🟧", "🟧"]]
        green_pixels = [["🟩", "🟩", "🟩"], ["🟩", "🟩", "🟩"], ["🟩", "🟩", "🟩"]]
        yellow_pixels = [["🟨", "🟨", "🟨"], ["🟨", "🟨", "🟨"], ["🟨", "🟨", "🟨"]]

        self.faces = {
            "white": self.white,
            "red": self.red,
            "blue": self.blue,
            "orange": self.orange,
            "green": self.green,
            "yellow": self.yellow,
        }
        
        self.pixels = {
            "white": white_pixels,
            "blue": blue_pixels,
            "red": red_pixels,
            "orange": orange_pixels,
            "green": green_pixels,
            "yellow": yellow_pixels,
        }

    def get_state(self):
        return self.faces, self.is_resolved()

    def is_resolved(self): 
        
        # Check if each square in each face is the same color as the first square
        for face in list(self.faces.values()):
            for row in face:
                for square in row:
                    if square[0] != row[0][0]:
                        return False
        return True
    
    def visualize(self):
        pass

    def rotate_face_clockwise(self, face, pixels):
        """Rotate a face 90 degrees clockwise."""
        return [list(row) for row in zip(*face[::-1])], [list(row) for row in zip(*pixels[::-1])]

    def rotate_face_counterclockwise(self, face, pixels):
        """Rotate a face 90 degrees counterclockwise."""
        return [list(row) for row in zip(*face)][::-1], [list(row) for row in zip(*pixels)][::-1]

    def rotate_row_or_column(self, face_name, index, is_row, direction):
        """
        Rotate a row or column on a face and update adjacent rows/columns on neighboring faces.
        - face_name: the face to rotate on
        - index: the row/column index
        - is_row: True if rotating a row, False if rotating a column
        - direction: 1 for clockwise, -1 for counterclockwise
        """
        if face_name not in self.faces:
            raise ValueError(f"Invalid face name: {face_name}")
        
        neighbors = {
            # Each face maps to its neighbors in [up, right, down, left] order
            "white": ["green", "red", "blue", "orange"],
            "yellow": ["blue", "red", "green", "orange"],
            "red": ["white", "blue", "yellow", "green"],
            "orange": ["white", "green", "yellow", "blue"],
            "green": ["white", "orange", "yellow", "red"],
            "blue": ["white", "red", "yellow", "orange"]
        }

        face = self.faces[face_name]
        pixel_face = self.pixels[face_name]
        neighbor_faces = neighbors[face_name]
        
        if is_row:
            # Get the row to rotate
            row = face[index][:]
            pixel_row = pixel_face[index][:]
            if direction == 1:  # Clockwise
                # Rotate row among neighbors
                neighbor_rows = [
                    self.faces[neighbor][index][:] for neighbor in neighbor_faces
                ]
                neighbor_pixel_rows = [
                    self.pixels[neighbor][index][:] for neighbor in neighbor_faces
                    ]
                
                neighbor_rows = neighbor_rows[-1:] + neighbor_rows[:-1]
                neighbor_pixel_rows = neighbor_pixel_rows[-1:] + neighbor_pixel_rows[:-1]

                for i, neighbor in enumerate(neighbor_faces):
                    self.faces[neighbor][index] = neighbor_rows[i]

                for i, neighbor in enumerate(neighbor_faces):
                    self.pixels[neighbor][index] = neighbor_pixel_rows[i]

            elif direction == -1:  # Counterclockwise
                neighbor_rows = [
                    self.faces[neighbor][index][:] for neighbor in neighbor_faces
                ]
                neighbor_pixel_rows = [
                    self.pixels[neighbor][index][:] for neighbor in neighbor_faces
                ]

                neighbor_rows = neighbor_rows[1:] + neighbor_rows[:1]
                neighbor_pixel_rows = neighbor_pixel_rows[-1:] + neighbor_pixel_rows[:-1]


                for i, neighbor in enumerate(neighbor_faces):
                    self.faces[neighbor][index] = neighbor_rows[i]
                
                for i, neighbor in enumerate(neighbor_faces):
                    self.pixels[neighbor][index] = neighbor_pixel_rows[i]
            
            # Rotate the face itself if it's the top/bottom row
            if index in [0, 2]:
                if direction == 1:
                    self.faces[face_name], self.pixels[face_name] = self.rotate_face_clockwise(face, pixel_face)
                else:
                    self.faces[face_name], self.pixels[face_name] = self.rotate_face_counterclockwise(face, pixel_face)
        else:
                # Handle column rotation
            col = [face[i][index] for i in range(3)]
            pixel_col = [pixel_face[i][index] for i in range(3)]

            if direction == 1:  # Clockwise
                # Rotate column among neighbors
                neighbor_columns = [
                    [self.faces[neighbor][i][index] for i in range(3)] for neighbor in neighbor_faces
                ]

                neighbor_pixels_columns = [
                    [self.pixels[neighbor][i][index] for i in range(3)] for neighbor in neighbor_faces
                ]

                neighbor_columns = neighbor_columns[-1:] + neighbor_columns[:-1]
                neighbor_pixels_columns = neighbor_pixels_columns[-1:] + neighbor_pixels_columns[:-1]

                for i, neighbor in enumerate(neighbor_faces):
                    for j in range(3):
                        self.faces[neighbor][j][index] = neighbor_columns[i][j]
                
                for i, neighbor in enumerate(neighbor_faces):
                    for j in range(3):
                        self.pixels[neighbor][j][index] = neighbor_pixels_columns[i][j]

            elif direction == -1:  # Counterclockwise
                neighbor_columns = [
                    [self.faces[neighbor][i][index] for i in range(3)] for neighbor in neighbor_faces
                ]
                neighbor_pixels_columns = [
                    [self.pixels[neighbor][i][index] for i in range(3)] for neighbor in neighbor_faces
                ]
                
                neighbor_columns = neighbor_columns[1:] + neighbor_columns[:1]
                neighbor_pixels_columns = neighbor_pixels_columns[1:] + neighbor_pixels_columns[:1]

                for i, neighbor in enumerate(neighbor_faces):
                    for j in range(3):
                        self.faces[neighbor][j][index] = neighbor_columns[i][j]
                
                for i, neighbor in enumerate(neighbor_faces):
                    for j in range(3):
                        self.pixels[neighbor][j][index] = neighbor_pixels_columns[i][j]
            
            # Rotate the face itself if it's the left/right column
            if index in [0, 2]:
                if direction == 1:
                    self.faces[face_name], self.pixels[face_name] = self.rotate_face_clockwise(face, pixel_face)
                else:
                    self.faces[face_name], self.pixels[face_name] = self.rotate_face_counterclockwise(face, pixel_face)

    def rotate(self, face_name, row_index, is_row, direction):
        """
        Wrapper function to rotate a face row and its adjacent neighbors.
        """
        self.rotate_row_or_column(face_name, row_index, is_row, direction=direction)

    def visualize_in_terminal(self):
        U = self.white
        D = self.yellow
        F = self.blue
        B = self.green
        L = self.red
        R = self.orange

        print("            ", " ".join(U[0]))
        print("            ", " ".join(U[1]))
        print("            ", " ".join(U[2]))
        print("\n")
        print(" ".join(B[0]), "   ", " ".join(L[0]), "   ", " ".join(F[0]), "   ", " ".join(R[0]))
        print(" ".join(B[1]), "   ", " ".join(L[1]), "   ", " ".join(F[1]), "   ", " ".join(R[1]))
        print(" ".join(B[2]), "   ", " ".join(L[2]), "   ", " ".join(F[2]), "   ", " ".join(R[2]))
        print("\n")
        print("            ", " ".join(D[0]))
        print("            ", " ".join(D[1]))
        print("            ", " ".join(D[2]))

    def __str__(self):
        print("            ", " ".join(self.pixels["white"][0]))
        print("            ", " ".join(self.pixels["white"][1]))
        print("            ", " ".join(self.pixels["white"][2]))
        print("\n")
        print(" ".join(self.pixels["green"][0]), "   ", " ".join(self.pixels["red"][0]), "   ", " ".join(self.pixels["blue"][0]), "   ", " ".join(self.pixels["orange"][0]))
        print(" ".join(self.pixels["green"][1]), "   ", " ".join(self.pixels["red"][1]), "   ", " ".join(self.pixels["blue"][1]), "   ", " ".join(self.pixels["orange"][1]))
        print(" ".join(self.pixels["green"][2]), "   ", " ".join(self.pixels["red"][2]), "   ", " ".join(self.pixels["blue"][2]), "   ", " ".join(self.pixels["orange"][2]))
        print("\n")
        print("            ", " ".join(self.pixels["yellow"][0]))
        print("            ", " ".join(self.pixels["yellow"][1]))
        print("            ", " ".join(self.pixels["yellow"][2]))
        return ""
    
    def str_that_cube(self):
        str1 = "                    " + " ".join(self.pixels["white"][0]) # Added 10 spaces to make the face align with the others on the GUI
        str2 = "                    " + " ".join(self.pixels["white"][1]) # Added 10 spaces to make the face align with the others on the GUI
        str3 = "                    " + " ".join(self.pixels["white"][2]) # Added 10 spaces to make the face align with the others on the GUI
        str4 = " ".join(self.pixels["green"][0]) + "   " + " ".join(self.pixels["red"][0]) + "   " + " ".join(self.pixels["blue"][0]) + "   " + " ".join(self.pixels["orange"][0])
        str5 = " ".join(self.pixels["green"][1]) + "   " + " ".join(self.pixels["red"][1]) + "   " + " ".join(self.pixels["blue"][1]) + "   " + " ".join(self.pixels["orange"][1])
        str6 = " ".join(self.pixels["green"][2]) + "   " + " ".join(self.pixels["red"][2]) + "   " + " ".join(self.pixels["blue"][2]) + "   " + " ".join(self.pixels["orange"][2])
        str7 = "                    " + " ".join(self.pixels["yellow"][0]) # Added 10 spaces to make the face align with the others on the GUI
        str8 = "                    " + " ".join(self.pixels["yellow"][1]) # Added 10 spaces to make the face align with the others on the GUI
        str9 = "                    " + " ".join(self.pixels["yellow"][2]) # Added 10 spaces to make the face align with the others on the GUI
        return str1 + "\n" + str2 + "\n" + str3 + "\n\n" + str4 + "\n" + str5 + "\n" + str6 + "\n\n" + str7 + "\n" + str8 + "\n" + str9
    
    def str_the_cube(self):
        # Align and format the squares for better representation
        row_format = " ".join(["{:^3}" for _ in range(3)])

        # Format each face with the correct alignment and spacing
        str1 = row_format.format(*self.pixels["white"][0])
        str2 = row_format.format(*self.pixels["white"][1])
        str3 = row_format.format(*self.pixels["white"][2])
        str4 = " ".join([row_format.format(*self.pixels["green"][i]) for i in range(3)])
        str5 = " ".join([row_format.format(*self.pixels["red"][i]) for i in range(3)])
        str6 = " ".join([row_format.format(*self.pixels["blue"][i]) for i in range(3)])
        str7 = " ".join([row_format.format(*self.pixels["orange"][i]) for i in range(3)])
        str8 = row_format.format(*self.pixels["yellow"][0])
        str9 = row_format.format(*self.pixels["yellow"][1])
        str10 = row_format.format(*self.pixels["yellow"][2])

        # Construct the full cube string with proper spacing
        return "\n".join([
            " " * 10 + str1,
            " " * 10 + str2,
            " " * 10 + str3,
            "",
            str4,
            str5,
            str6,
            str7,
            "",
            " " * 10 + str8,
            " " * 10 + str9,
            " " * 10 + str10
        ])

    
    def scramble(self):
        # Perform a random sequence of moves on the cube
        scrambled_cube = self
        for _ in range(100):
            random_face = random.choice(list(scrambled_cube.faces.keys()))
            random_direction = random.choice([-1, 1])
            scrambled_cube.rotate(random_face, row_index=0, is_row = True, direction=random_direction)

        return scrambled_cube
    
    def copy(self):
        return copy.deepcopy(self)
        

if __name__ == "__main__":
    cube = RubikCube()
    print("Is the cube resolved ?", cube.is_resolved())
    print("\n")
    print("Rotating the cube 90 degrees clockwise on the white face\n")
    cube.rotate("white", 0, True, 1)
    str_cube = cube.str_that_cube()
    print(cube)
    print("\n=========================")
    print(str_cube)



