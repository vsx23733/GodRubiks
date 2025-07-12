import raylibpy as rl
import numpy as np
import random 

class Cube:
    def __init__(self, size, center, face_color):
        self.size = size
        self.center = center
        self.face_color = face_color
        self.orientation = np.eye(3)
    
        self.model = None
        self.gen_mesh(size)

        self.create_model()

    def gen_mesh(self, scale : tuple):

        self.mesh = rl.gen_mesh_cube(*scale)

    def create_model(self):
        self.model = rl.load_model_from_mesh(self.mesh)
        self.model.transform = rl.matrix_translate(self.center[0], self.center[1], self.center[2])

    def apply_rotation(self, axis, angle_degrees):
        rotation_matrix = rl.matrix_rotate(axis, angle_degrees * rl.DEG2RAD)
        self.model.transform = rl.matrix_multiply(self.model.transform, rotation_matrix)

    def rotate(self, axis, theta):
        if axis == 0:
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])
        elif axis == 1:
            rotation_matrix = np.array([
                [np.cos(theta), 0, np.sin(theta)],
                [0, 1, 0],
                [-np.sin(theta), 0, np.cos(theta)]
            ])
        elif axis == 2:
            rotation_matrix = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
                ])
        else:
            raise ValueError("Invalid Axis. Use 0, 1, or 2 for x, y, z axis respectively")
        
        self.center = rotation_matrix

class Rubik:
    def __init__(self):
        self.cubes = []
        self.generate_cube(2)


    def generate_cube(self, size):
        colors = [rl.WHITE, rl.BLUE, rl.ORANGE, rl.RED, rl.YELLOW, rl.GREEN]
        offset = size - 0.7
        size_z = size * 0.9, size * 0.9, size * 0.1
        size_x = size * 0.9, size * 0.1, size * 0.9
        size_y = size * 0.1, size * 0.9, size * 0.9
        
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    face_colors = [
                        rl.BLACK if z != 2 else colors[0], # front
                        rl.BLACK if z != 0 else colors[1], # back
                        rl.BLACK if x != 2 else colors[2], # right
                        rl.BLACK if x != 0 else colors[3], # left
                        rl.BLACK if y != 2 else colors[4], # top
                        rl.BLACK if y != 0 else colors[5], # bottom
                    ]

                    # Center

                    center_position = np.array([(x - 1) * offset, 
                                                (y - 1) * offset, 
                                                (z - 1) * offset])
                    center = Cube((size, size, size), 
                                  center_position, 
                                  rl.BLACK) 
                    

                    # Front Face
                    front_position = np.array([center_position[0],
                                               center_position[1],
                                               center_position[2] + size/2])
                                            
                    front = Cube(size_z, front_position, face_colors[0])

                    # Back Face
                    back_position = np.array([center_position[0],
                                               center_position[1],
                                               center_position[2] - size/2])
                    back = Cube(size_z, back_position, face_colors[1])
                    #back.apply_rotation(rl.Vector3(0, 1, 0), 180.0)


                    # Right Face
                    right_position = np.array([center_position[0] + size/2,
                                              center_position[1],
                                              center_position[2]])
                    right = Cube(size_x, right_position, face_colors[2])
                    #right.apply_rotation(rl.Vector3(0, 1, 0), -90.0)


                    # Left face 
                    left_position = np.array([center_position[0] - size/2,
                                              center_position[1],
                                              center_position[2]])
                    left = Cube(size_x, left_position, face_colors[3])
                    #left.apply_rotation(rl.Vector3(0, 1, 0), 90.0)


                    # Top face
                    top_position = np.array([center_position[0],
                                              center_position[1] + size/2,
                                              center_position[2]])
                    top = Cube(size_y, top_position, face_colors[4])
                    #top.apply_rotation(rl.Vector3(1, 0, 0), -90.0)


                    # Bottom face
                    bottom_position = np.array([center_position[0],
                                              center_position[1] - size/2,
                                              center_position[2]])
                    bottom = Cube(size_y, bottom_position, face_colors[5])
                    #bottom.apply_rotation(rl.Vector3(1, 0, 0), 90.0)


                    self.cubes.append([center, front, back, right, left, top, bottom])

    def choose_piece(self, piece, axis_index, level):
        if level == 0 and round(piece[0].center[axis_index], 1) < 0:
            return True
        elif level == 1 and round(piece[0].center[axis_index], 1) == 0:
            return True
        elif level == 2 and round(piece[0].center[axis_index], 1) > 0:
            return True
        
        return False
    
    def get_face(self, axis, level):
        axis_index = np.nonzero(axis)[0][0]
        segment = [i for i, cube in enumerate(self.cubes) if self.choose_piece(cube, axis_index, level)]
        return segment

    def handle_rotation(self, rotation_queue, animation_step=None):
        
        # Check if there is a request and if not rotating already
        if rotation_queue and not self.is_rotating:

            # Get the next rotation axis and level
            self.target_rotation, self.rotation_axis, self.level = rotation_queue.pop(0)

            if self.target_rotation > 0:
                self.target_rotation += random.uniform(0, 1) ** 10 ** -3
            else:
                self.target_rotation -= random.uniform(0, 1) ** 10 ** -3

            self.segment = self.get_face(self.rotaton_axis, self.level)

            # Reset rotation angle at the start of a new rotation 
            self.rotation_angle = 0

            # Set rotating to true to start a rotation
            self.is_rotating = True

        if self.is_rotating:
            if (self.rotation_angle != self.target_rotation):
                diff = abs(self.target_rotation - self.rotation_angle)
                delta_angle = min(np.radians(1), diff)

                # Increment rotation angle in the correct direction
                self.rotation_angle += delta_angle if self.target_rotation > 0 else -delta_angle
            else:
                delta_angle = 0

                # Stop rotating when target rotation is reached 
                self.is_rotating = False

                if animation_step is not None:
                    animation_step += 1

            for id, cube in enumerate(self.cubes):
                axis_index = np.nonzero(self.rotation_axis)[0][0]

                if id in self.segment:
                    for part_id, _ in enumerate(cube):
                        if self.target_rotation > 0:
                            self.cubes[id][part_id].rotate(axis_index, delta_angle)
                        else:
                            self.cubes[id][part_id].rotate(axis_index, -delta_angle)

                        pos_x, pos_y, pos_z = self.cubes[id][part_id].center
                        translation = rl.matrix_translate(pos_x, pos_y, pos_z)
                        rota, angle = self.cubes[id][part_id].get_rotation_axis_angle()
                        rotation = rl.matrix_rotate(rota, np.radians(angle))
                        transform = rl.matrix_multiply(rotation, translation)
                        self.cubes[id][part_id].model.transform = transform

                else:
                    self.is_rotating = True

                return rotation_queue, animation_step

    

