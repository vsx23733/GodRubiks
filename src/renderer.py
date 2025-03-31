from ursina import *
from config import *

class Game:
    def __init__(self):
        app = Ursina()
        window.fullscreen = True
        window.color = color.black
        Entity(
            model='quad',
            scale=SQUARE,
            texture='white_cube',
            texture_scale=(SQUARE, SQUARE),
            rotation_x=90,
            y=-5,
            color=color.light_gray
        )  # ground
        Entity(
            model='sphere',
            scale=SPHERE,
            texture='textures/background',
            double_sided=True
        )  # background

        EditorCamera()
        camera.world_position = INITIAL_POS
        self.model, self.texture = 'cube', 'textures/rubiks_model'
        self.load_game()
        app.run()

    def load_game(self):
        self.generate_cube_orientations()
        self.CUBES = [Entity(
            model=self.model,
            texture=self.texture,
            position=pos,
        ) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {
            'LEFT': 'x',
            'RIGHT': 'x',
            'TOP': 'y',
            'BOTTOM': 'y',
            'FACE': 'z',
            'BACK': 'z'
        }
        self.cubes_side_positions = {
            'LEFT': self.LEFT,
            'BOTTOM': self.BOTTOM,
            'RIGHT': self.RIGHT,
            'FACE': self.FACE,
            'BACK': self.BACK,
            'TOP': self.TOP
        }
        self.animation_time = ANIMATION_TIME
        self.action_trigger = True
        self.action_mode = True
        self.message = Text(origin=(0, 17.5), color=color.yellow)
        self.controls = Text(origin=(0, 19), color=color.light_gray)
        self.switch_mode()
        self.create_sensors()
        self.initial_mixing()

    def initial_mixing(self, rotations=INITIAL_ROTATIONS):
        [self.initial_rotation(random.choice(list(self.rotation_axes))) for _ in range(rotations)]

    def initial_rotation(self, side_name):
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = 90')

    def generate_cube_orientations(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP

    def create_sensors(self):
        create_sensor = lambda name, pos, scale: Entity(
            name=name,
            position=pos,
            model='cube',
            color=color.dark_gray,
            scale=scale,
            collider='box',
            visible=False
        )
        #sensor for each side
        self.LEFT_SENSOR = create_sensor(
            name='LEFT', 
            pos=(-0.99, 0, 0),
            scale=(1.01, 3.01, 3.01)
            )
        self.RIGHT_SENSOR = create_sensor(
            name='RIGHT', 
            pos=(0.99, 0, 0),
            scale=(1.01, 3.01, 3.01)
            )
        self.TOP_SENSOR = create_sensor(
            name='TOP', 
            pos=(0, 1, 0),
            scale=(3.01, 1.01, 3.01)
            )
        self.BOTTOM_SENSOR = create_sensor(
            name='BOTTOM', 
            pos=(0, -1, 0),
            scale=(3.01, 1.01, 3.01)
            )
        self.FACE_SENSOR = create_sensor(
            name='FACE', 
            pos=(0, 0, -0.99),
            scale=(3.01, 3.01, 1.01)
            )
        self.BACK_SENSOR = create_sensor(
            name='BACK', 
            pos=(0, 0, 0.99),
            scale=(3.01, 3.01, 1.01)
            )
        

    def switch_mode(self):
        #changing game mode
        self.action_mode = not self.action_mode
        display_text = dedent(
            f"{'ACTION mode' if self.action_mode else 'VIEW mode'}"
            f" (to switch game mode press the space bar)"
        ) 
        controls_text = dedent(
            f" (To rotate LEFT, RIGHT, FACE, BACK sides: click the left mouse button)"
            f" (To rotate TOP and BOTTOM sides: click the right mouse button)"
        )  
        self.message.text = display_text
        self.controls.text = controls_text 

    def toggle_animation_trigger(self):
        self.animation_trigger = not self.animation_trigger


    def rotate_clicked_side(self, side_name):
        self.animation_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(
                    f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)'
                )
        invoke(
            self.toggle_animation_trigger, delay=self.animation_time + 0.11
        )

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_position, world_rotation = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_position, world_rotation
        self.PARENT.rotation = 0

    def generate_cube_orientations(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.BOTTOM = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FACE = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.TOP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM | self.FACE | self.BACK | self.RIGHT | self.TOP


    def input(self, key):
        if key in 'mouse1 mouse3' and self.action_mode and self.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if (key == 'mouse1' and collider_name in 'LEFT RIGHT FACE BACK' or
                        key == 'mouse3' and collider_name in 'TOP BOTTOM'):
                    # print('left key was pressed')
                    self.rotate_clicked_side(collider_name)
                    break
        if key == 'space':
            self.switch_mode()
        super().input(key)

if __name__ == '__main__':
    Game()
