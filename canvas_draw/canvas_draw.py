from tkinter import Tk, Canvas, Frame, Button, Label, Entry, END, LEFT
from position_conversion import convert_screen_to_ws
from HSPO_extract import hspo_extract
import threading
import csv
from time import sleep
import struct
from oneline_drw.generate_drawing import capture_and_process_image as generate_portrait_points


def run_canvas_gui(method, HSPO):  # Accept method from main
    root = Tk()
    root.title('Drawing Canvas')
    root.attributes('-fullscreen', True)  # Fullscreen mode
    pos = {'position': (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)}
    root.bind("<Escape>", lambda e: root.destroy())  # Exit fullscreen on Escape
    canvas = Canvas(root, bg='white')
    canvas.pack(fill='both', expand=True, pady=10)
    screen_width = canvas.winfo_screenwidth()
    screen_height = canvas.winfo_screenheight()
    all_paths = []
    path_points = []
    current_path_points = []
    requester = 0
    
    
    
    def start_drawing(event):
        # Start a new path for each mouse press
        nonlocal path_points
        path_points = [(event.x, event.y)]
        all_paths.append(path_points)

    def draw(event):
        x, y = event.x, event.y
        last_x, last_y = path_points[-1] if path_points else (x, y)
        distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
        if distance >= 10:
            canvas.create_line(last_x, last_y, x, y, fill='black', width=2)
            path_points.append((x, y))

    def clear_canvas():
        canvas.delete("all")
        all_paths.clear()
        path_points.clear()

    def move_robot_to_path(path):
        
        method.FRC_call("_DW_MOVEUP")
        sleep(0.5)
        method.FRC_get_status()

        def move():
            nonlocal requester
            if not path:
                print("No points to move to.")
                return
            max_distance = 0
            
            for curr_path in path:
                
                # if not path:
                #     return
                total_points = len(curr_path)
                previous_point = curr_path[0]
                for i, point in enumerate(curr_path):
                    # Wait until there’s room in the buffer
                    # while method.sequenceDiff >= 8:
                    #     sleep(0.01)

                    # Convert point to workspace coordinates
                    
                    if i >= total_points-1:
                        method.FRC_get_status()
                        sleep(0.5)
                        method.FRC_call("_DW_MOVEUP")
                    else:
                        if requester == 1:
                            distance = ((point[0] - previous_point[0]) ** 2 + (point[1] - previous_point[1]) ** 2) ** 0.5
                            if distance > max_distance:
                                max_distance = distance
                            print(f"Moving to point: {point}, Previous point: {previous_point}")
                            print(f"max_distance: {max_distance}")
                            print(f"distance: {distance}")
                            if distance >= 30:
                                method.FRC_call("_DW_MOVEUP")
                                
                            ws_x, ws_y = point[0], point[1]
                            method.linear_move(ws_x, ws_y)
                            previous_point = point
                        else:
                            ws_x, ws_y = convert_screen_to_ws(point[0], point[1], screen_width, screen_height)
                            method.linear_move(ws_x, ws_y)
                
        
            # wait_for_sequence_ack(method)
        move_thread = threading.Thread(target=move, daemon=True)
        move_thread.start()
        
    
    
    def hspo_loop(sock):
        last_output = None
        while True:
            binary_format = ">LLLHH6fLL"
            required_length = struct.calcsize(binary_format)
            data, _ =       HSPO.recvfrom(1024)
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
        sleep(0.5)
        method.FRC_reset()
        method.FRC_abort()
        method.FRC_disconnect()
        print("Sequence aborted.")
        
    def calibrate_Z():
        method.FRC_get_status()
        method.FRC_call("_GET_Z_HEIGHT")
        sleep(0.5)
        method.get_current_position()
        method.FRC_call("_DW_MOVEUP")
        
   
        
    def get_portrait_points():
        nonlocal requester
        requester = 1
        generate_portrait_points()
        all_csv_paths = []
        current_path = []
        with open(r"C:\Users\Matt\Documents\robot_RMIU\RMI_Interface\canvas_draw\oneline_drw\csv\one_line_drawing_cleaned.csv", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    if current_path:
                        all_csv_paths.append(current_path)
                        current_path = []
                else:
                    x, y = map(float, line.split(','))
                    current_path.append((x, y))
            if current_path:  # Add last path if file doesn't end with blank line
                all_csv_paths.append(current_path)
        method.FRC_reset()
        method.FRC_get_status()
        move_robot_to_path(all_csv_paths)
        print(f"Portrait points loaded from CSV. Number of paths: {len(all_csv_paths)}")
    
   
        
    
    
    def draw_path():
        nonlocal requester
        if not all_paths:
            print("No points to draw.")
            return
        requester = 0
        move_robot_to_path(all_paths)  
        
               
    
    
    # def update_sequence_dif():
    #     method.listen()
    # threading.Thread(target=update_sequence_dif , daemon=True).start()
                     
    # Bind mouse events
    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", draw)

    # Create a frame for buttons
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # Add buttons
    Button(button_frame, text="Draw Portrait", command=get_portrait_points).pack(side=LEFT, padx=5)
    Button(button_frame, text="Clear Canvas", command=clear_canvas).pack(side=LEFT, padx=5)
    Button(button_frame, text="Draw doodle", command=draw_path).pack(side=LEFT, padx=5)
    Button(button_frame, text="Reset", command=method.FRC_reset).pack(side=LEFT, padx=5)
    # Button(button_frame, text="Pause", command=method.FRC_pause).pack(side=LEFT, padx=5)
    # Button(button_frame, text="Continue", command=method.FRC_continue).pack(side=LEFT, padx=5)
    # Button(button_frame, text="Abort", command=method.FRC_abort).pack(side=LEFT, padx=5)
    Button(button_frame, text="Disconnect", command=disconnect_sequence).pack(side=LEFT, padx=5)
    Button(button_frame, text="Connect", command=method.FRC_connect).pack(side=LEFT, padx=6)
    Button(button_frame, text="Get Status", command=method.FRC_get_status).pack(side=LEFT, padx=5)
    Button(button_frame, text="Initialize Z", command=calibrate_Z).pack(side=LEFT, padx=5)
    
    
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
