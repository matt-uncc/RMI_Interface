from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT
from position_conversion import convert_screen_to_ws
from HSPO_extract import hspo_extract
import threading
import time
from time import sleep
import struct
import csv


def run_canvas_gui(method, HSPO):  # Accept method from main
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

    # def show_points():
    #     print("Path points:")
    #     for point in path_points:
    #         print(point)
    def get_portrait_points():
        with open(r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\oneline_drw\csv\one_line_drawing.csv", 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            path_points.clear()
            for row in reader:
                path_points.append((float(row[0]), float(row[1])))
        
    def clear_canvas():
        canvas.delete("all")
        path_points.clear()

    def wait_for_sequence_ack(method, timeout=2):
        start = time.time()
        while method.sequenceDiff > 0:
            if time.time() - start > timeout:
                print("Timeout waiting for sequence ack.")
                break
            time.sleep(0.01)
            
            
    def move_robot_to_path():
        method.FRC_call("_GET_Z_HEIGHT")
        wait_for_sequence_ack(method)
        method.get_current_position()
        method.FRC_call("_DW_MOVEUP")
        def move():
            if not path_points:
                print("No points to move to.")
                return
            for point in path_points:
                ws_x, ws_y = convert_screen_to_ws(point[0], point[1])
                method.linear_move(ws_x, ws_y)
            method.FRC_call("_DW_MOVEUP")
            wait_for_sequence_ack(method)
        threading.Thread(target=move, daemon=True).start()

    
    
    def hspo_loop(sock):
        last_output = None
        while True:
            binary_format = ">LLLHH6fLL"
            required_length = struct.calcsize(binary_format)
            data, _ = HSPO.recvfrom(1024)
            result = hspo_extract(data, required_length, binary_format)
            if result and result != last_output:
                last_output = result
                pos['position'] = result

                       
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
        
    def disconnect_sequence():
        method.FRC_call("_DW_HOME")
        wait_for_sequence_ack(method)
        method.FRC_reset()
        method.FRC_abort()
        method.FRC_disconnect()
        wait_for_sequence_ack(method)
        print("Sequence aborted.")
        root.quit()
            
                     
    # Bind mouse events
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", draw)

    # Create a frame for buttons
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # Add buttons
    Button(button_frame, text="Draw portrait", command=get_portrait_points).pack(side=LEFT, padx=5)
    Button(button_frame, text="Clear Canvas", command=clear_canvas).pack(side=LEFT, padx=5)
    Button(button_frame, text="Move Robot", command=move_robot_to_path).pack(side=LEFT, padx=5)
    Button(button_frame, text="Reset", command=method.FRC_reset).pack(side=LEFT, padx=5)
    Button(button_frame, text="Pause", command=method.FRC_pause).pack(side=LEFT, padx=5)
    Button(button_frame, text="Continue", command=method.FRC_continue).pack(side=LEFT, padx=5)
    Button(button_frame, text="Abort", command=method.FRC_abort).pack(side=LEFT, padx=5)
    Button(button_frame, text="Disconnect", command=disconnect_sequence).pack(side=LEFT, padx=5)
    Button(button_frame, text="Connect", command=method.FRC_connect).pack(side=LEFT, padx=6)
    Button(button_frame, text="Get Status", command=method.FRC_get_status).pack(side=LEFT, padx=5)
    Button(button_frame, text="Get Current Position", command=method.get_current_position).pack(side=LEFT, padx=5)
    
    
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
    
    threading.Thread(target=hspo_loop, args=(HSPO,), daemon=True).start()
    update_current_position()
    root.mainloop()
