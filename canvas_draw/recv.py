import struct

# def hspo_extract(data):
#     binary_format = ">LLLHH6fLL"  # Adjust if your format changes
#     required_length = struct.calcsize(binary_format)

#     if len(data) >= required_length:
#         unpacked = struct.unpack(binary_format, data[:required_length])
#         X, Y, Z = unpacked[5], unpacked[6], unpacked[7]
#         W, P, R = unpacked[8], unpacked[9], unpacked[10]
#         return X, Y, Z, W, P, R
#     else:
#         print("Packet too short for expected format")
#         return None


        
from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT
from position_conversion import convert_screen_to_ws
from HSPO_extract import hspo_extract
import threading
import time
import struct


def run_canvas_gui(HSPO):  # Accept method from main
    root = Tk()
    root.title('Drawing Canvas')
    root.geometry('800x700')
    pos = {'position': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)}

    canvas = Canvas(root, width=800, height=500, bg='white')
    canvas.pack(pady=10)

    path_points = []

    def start_drawing(event):
        path_points.clear()
        path_points.append((event.x, event.y))

    def draw(event):
        x, y = event.x, event.y
        last_x, last_y = path_points[-1] if path_points else (x, y)
        distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
        if distance >= 20:
            canvas.create_line(last_x, last_y, x, y, fill='black', width=2)
            path_points.append((x, y))

    def show_points():
        print("Path points:")
        for point in path_points:
            print(point)

    def clear_canvas():
        canvas.delete("all")
        path_points.clear()

    
    
    def run_test(sock):
        last_output = None
        while True:
            binary_format = ">LLLHH6fLL"
            required_length = struct.calcsize(binary_format)
            data, addr = HSPO.recvfrom(1024)
            result = hspo_extract(data, required_length, binary_format)
            if result and result != last_output:
                print(f"From {addr}: X={result[0]:.2f}, Y={result[1]:.2f}, Z={result[2]:.2f}, "
                      f"W={result[3]:.2f}, P={result[4]:.2f}, R={result[5]:.2f}")
                last_output = result
    



                       
    def update_current_position():
        result = pos.get('position')
        if result:
            x_entry.delete(0, END)
            x_entry.insert(0, f"{result[0]:.2f}")
            y_entry.delete(0, END)
            y_entry.insert(0, f"{result[1]:.2f}")
            z_entry.delete(0, END)
            z_entry.insert(0, f"{result[2]:.2f}")
            w_entry.delete(0, END)
            w_entry.insert(0, f"{result[3]:.2f}")
            p_entry.delete(0, END)
            p_entry.insert(0, f"{result[4]:.2f}")
            r_entry.delete(0, END)
            r_entry.insert(0, f"{result[5]:.2f}")
        root.after(1000, update_current_position)
            
                     
    # Bind mouse events
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", draw)

    # Create a frame for buttons
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # Add buttons
    Button(button_frame, text="Show Points", command=show_points).pack(side=LEFT, padx=5)
    Button(button_frame, text="Clear Canvas", command=clear_canvas).pack(side=LEFT, padx=5)
    
    
    entry_frame = Frame(root)
    entry_frame.pack(pady=10)

    Label(entry_frame, text="X:").grid(row=0, column=0)
    x_entry = Entry(entry_frame, width=10)
    x_entry.grid(row=1, column=0)

    Label(entry_frame, text="Y:").grid(row=0, column=1)
    y_entry = Entry(entry_frame, width=10)
    y_entry.grid(row=1, column=1)

    Label(entry_frame, text="Z:").grid(row=0, column=2)
    z_entry = Entry(entry_frame, width=10)
    z_entry.grid(row=1, column=2)

    Label(entry_frame, text="W:").grid(row=0, column=3)
    w_entry = Entry(entry_frame, width=10)
    w_entry.grid(row=1, column=3)

    Label(entry_frame, text="P:").grid(row=0, column=4)
    p_entry = Entry(entry_frame, width=10)
    p_entry.grid(row=1, column=4)

    Label(entry_frame, text="R:").grid(row=0, column=5)
    r_entry = Entry(entry_frame, width=10)
    r_entry.grid(row=1, column=5)

    # Start periodic updates
    
    threading.Thread(target=run_test, args=(HSPO,), daemon=True).start()
    update_current_position()
    root.mainloop()
