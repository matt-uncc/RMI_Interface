
# this is subject to be change if the physical canvas size changes
# please configure the canvas size everytime the physical canvas size changes
ws_origin = (20, 20)
ws_span_x = 130
ws_span_y = 360

def convert_screen_to_ws(x, y, screen_width, screen_height):
    
    # increment_x = ws_span_x / 600
    # increment_y = ws_span_y / 800
    # ws_y = ws_origin[0] + x * increment_y
    # ws_x = ws_origin[1] + y * increment_x
    ws_y = x * ws_span_x / screen_height + ws_origin[0]
    ws_x = y * ws_span_y / screen_width + ws_origin[1]
    print(f"Converted screen coordinates ({x}, {y}) to workspace coordinates ({ws_x}, {ws_y})")
   
    return ws_x, ws_y

# def convert_screen_to_ws(x, y, min_x, max_x, min_y, max_y, rotated_90=True):
#     # Normalize input coordinates to [0,1]
#     norm_x = (x - min_x) / (max_x - min_x)
#     norm_y = (y - min_y) / (max_y - min_y)

#     if rotated_90:
#         # Rotate coordinates 90 degrees CCW and scale to workspace
#         ws_x = ws_origin[0] + norm_y * ws_span_x
#         ws_y = ws_origin[1] + (1 - norm_x) * ws_span_y
#     else:
#         # No rotation, just scale normally
#         ws_x = ws_origin[0] + norm_x * ws_span_x
#         ws_y = ws_origin[1] + norm_y * ws_span_y

#     print(f"Converted screen ({x}, {y}) → workspace ({ws_x:.2f}, {ws_y:.2f})")
#     return ws_x, ws_y
# def convert_screen_to_ws(x, y):
#     increment_x = ws_span_x / 400 
#     increment_y = ws_span_y / 600 
#     ws_y = ws_origin[0] + x * increment_y
#     ws_x = ws_origin[1] + y * increment_x
#     print(f"Converted screen coordinates ({x}, {y}) to workspace coordinates ({ws_x}, {ws_y})")
#     return ws_x, ws_y




def convert_ws_to_screen(ws_x, ws_y):
    increment_x = ws_span_x / 600  # Assuming tkinter canvas width is 800 pixels
    increment_y = ws_span_y / 800  # Assuming tkinter canvas height is 600 pixels
    screen_x = (ws_x + ws_origin[0]) / increment_x
    screen_y = (ws_y + ws_origin[1]) / increment_y
    return screen_x, screen_y



