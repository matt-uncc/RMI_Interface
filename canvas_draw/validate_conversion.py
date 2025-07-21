from position_conversion import convert_screen_to_ws

pos = input("Enter position in format X,Y")
ws_pos = convert_screen_to_ws(*map(float, pos.split(',')))
print(f"Workspace position: {ws_pos}")
