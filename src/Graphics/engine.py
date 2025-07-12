import raylibpy as rl
import configs
from graphicCube import Rubik


rl.init_window(
    configs.window_w, 
    configs.window_h,
    b"Building a Rubik's Cube"  
)

rubik_cube = Rubik()

rl.set_target_fps(configs.fps)

while not rl.window_should_close():

    # ─── Handle Camera & Input ───────────────────────────
    rl.update_camera(configs.camera, rl.CAMERA_THIRD_PERSON)

    if rl.is_key_pressed(rl.KEY_SPACE):
        print("SPACE was pressed")

    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        mouse_pos = rl.get_mouse_position()
        print(f"Left click at: {mouse_pos}")


    # ─── Drawing Phase ────────────────────────────────────
    rl.update_camera(configs.camera, 
                     rl.CAMERA_THIRD_PERSON)
    


    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE) 
    rl.begin_mode3d(configs.camera)
    rl.draw_grid(20, 1.0)

    for i, cube in enumerate(rubik_cube.cubes):
        for cube_part in cube:
            position = rl.Vector3(cube[0].center[0], cube[0].center[1], cube[0].center[2])
            print(cube[0].center)
            rl.draw_model(
                cube_part.model, 
                position, 
                1   , 
                cube_part.face_color
            )

    rl.end_mode3d()
    rl.end_drawing()

rl.close_window()
