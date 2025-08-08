from tkinter import *
import socket
from handler import handlerDict
from FRC_ import FRC_
import time
from command import Command
from pkg_2_call import MotionMethod


handler = handlerDict()
getPackage = FRC_()

move= ["LinearMotion", "JointMotion","JointRelativeMotion"] 


# create GUI window
c_window = Tk()
c_window.geometry('600x200+50+50')
c_window.title('Test Client')


# initialize socket
global s
ip_connect = "192.168.1.100"
port_connect = 16002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)  # Set a timeout for the socket operations
try:
    s.connect((ip_connect, port_connect))
except socket.timeout:
    print(f"Error connecting to socket at {ip_connect}:{port_connect}")


# create a dictionary from text file
with open('from_manual.txt', 'r') as file:
    file_content = file.read()
    dict = handler.json_to_dict(file_content)



def button_connect():
    pkg = Command().button_connect()
    rcvd = send_pkg(pkg)
    receive_entry.insert("1.0", rcvd)
    button_initialize()
    return

def button_reset():
    pkg = Command().button_reset()
    send_pkg(pkg)
    return

def button_pause():
    pkg = Command().button_pause()
    send_pkg(pkg)
    return

def button_abort():
    pkg = Command().button_abort()
    send_pkg(pkg)
    return

def button_continue():
    pkg = Command().button_continue()
    send_pkg(pkg)
    return

def button_disconnect():
    pkg = Command().button_disconnect()
    send_pkg(pkg)
    return

def button_get_status():
    pkg = Command().button_get_status()
    rcvd = send_pkg(pkg)
    sequence = get_sequenceID(rcvd)
    return sequence

# def button_get_curr_pos():
#     pkg = getPackage.ReadCartesianPosition()
#     pkg = handler.dict_to_json(pkg)
#     rcvd = send_pkg(pkg)
#     update_position(rcvd)
#     return 

# this method take json pkg and send it to the robot
def send_pkg(pkg, bit = False): 
    global s      
    try:
        print(f"Sending: {pkg}")
        s.send(pkg.encode('ascii')) 
        # time.sleep(0.5)  # wait for the server to process the request
        s.settimeout(5)
        start_time = time.time()
        if bit == False:
            while time.time() - start_time < .5:
                try:
                    rcvd = s.recv(1024)
                    receive_entry.delete("1.0", END)
                    receive_entry.insert("1.0", rcvd)
                    print(f"Received: {rcvd}")
                    return rcvd
                    # sequence = sequence + 1
                except socket.timeout:
                    print("time out waiting for return messages")
        
    except Exception as e:
        receive_entry.delete("1.0", END)
        receive_entry.insert("1.0", f"Send failed: {e}" )
    return 



def submit_button(): 
    pass
    

def get_sequenceID(pkg):
    global sequence
    dict = handler.json_to_dict(pkg)
    for item in dict:
        if item == 'NextSequenceID':
            sequence = dict['NextSequenceID']
    return sequence

def button_initialize():
    pkg = Command().button_initialize()
    rcvd = send_pkg(pkg)
    receive_entry.insert("1.0", rcvd)
    return


def moveTo(mode):
    sequence = button_get_status()
    time.sleep(0.5)
    if s:
        uFrameNumber = int(uFrame_text.get())
        uToolNumber = int(uTool_text.get())
        val1 = float(x_text.get())
        val2 = float(y_text.get())
        val3 = float(z_text.get())
        val4 = float(w_text.get())
        val5 = float(p_text.get())
        val6 = float(r_text.get())


        # Create an instance of MotionMethod
        motion_method = MotionMethod(sequence)
        
        if mode == "LinearMotion":
            motion_package = handler.dict_to_json(motion_method.linear_move(val1, val2, val3, val4, val5, val6, uFrameNumber, uToolNumber))
            send_pkg(motion_package ,bit = True)
        elif mode == "JointMotion":
            # Remove 'sequence' parameter since it's already set in constructor
            motion_package = handler.dict_to_json(motion_method.joint_motion(val1, val2, val3, val4, val5, val6, uFrameNumber, uToolNumber))
            send_pkg(motion_package)
        elif mode == "JointRelativeMotion":
            # Remove 'sequence' parameter since it's already set in constructor
            motion_package = handler.dict_to_json(motion_method.joint_motion_relative(val1, val2, val3, val4, val5, val6, uFrameNumber, uToolNumber))
            send_pkg(motion_package)
    else:
        receive_entry.insert("1.0", "connection is not established")
    return


opt = StringVar(value="LinearMotion")  # Default value)

# --- Frames for organization ---
connection_frame = Frame(c_window)
connection_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

motion_frame = Frame(c_window)
motion_frame.grid(row=0, column=2, columnspan=6, pady=5, sticky="w")

status_frame = Frame(c_window)
status_frame.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")

emergency_frame = Frame(c_window)
emergency_frame.grid(row=1, column=2, columnspan=6, pady=5, sticky="w")

position_frame = Frame(c_window)
position_frame.grid(row=2, column=0, columnspan=13, pady=5, sticky="w")

output_frame = Frame(c_window)
output_frame.grid(row=3, column=0, columnspan=13, pady=10, sticky="w")

# --- Connection Buttons ---
connect_btn = Button(connection_frame, text='Connect', command=button_connect)
connect_btn.pack(side=LEFT, padx=2)
disconnect_btn = Button(connection_frame, text='Disconnect', command=button_disconnect)
disconnect_btn.pack(side=LEFT, padx=2)

# --- Motion Controls ---
Label(motion_frame, text="Motion Type:").pack(side=LEFT, padx=2)
OptionMenu(motion_frame, opt, *move).pack(side=LEFT, padx=2)
Button(motion_frame, text="Move", command=lambda: moveTo(opt.get())).pack(side=LEFT, padx=2)

# --- Status Button ---
getST_btn = Button(status_frame, text='GetStatus', command=button_get_status)
getST_btn.pack(side=LEFT, padx=2)

# --- Emergency Buttons ---
reset_btn = Button(emergency_frame, text='Reset', command=button_reset)
reset_btn.pack(side=LEFT, padx=2)
pause_btn = Button(emergency_frame, text='Pause', command=button_pause)
pause_btn.pack(side=LEFT, padx=2)
continue_btn = Button(emergency_frame, text='Continue', command=button_continue)
continue_btn.pack(side=LEFT, padx=2)
abort_btn = Button(emergency_frame, text='Abort', command=button_abort)
abort_btn.pack(side=LEFT, padx=2)

# --- Position Inputs ---
Label(position_frame, text="UFrame Number").grid(row=0, column=0)
uFrame_text = Entry(position_frame)
uFrame_text.insert(0, '1')
uFrame_text.grid(row=1, column=0)

Label(position_frame, text="UTool Number").grid(row=0, column=1)
uTool_text = Entry(position_frame)
uTool_text.insert(0, '1')
uTool_text.grid(row=1, column=1)

Label(position_frame, text="X/J1").grid(row=0, column=2)
x_text = Entry(position_frame)
x_text.insert(0, '0.0')
x_text.grid(row=1, column=2)

Label(position_frame, text="Y/J2").grid(row=0, column=3)
y_text = Entry(position_frame)
y_text.insert(0,"0.0")
y_text.grid(row=1, column=3)

Label(position_frame, text="Z/J3").grid(row=0, column=4)
z_text = Entry(position_frame)
z_text.insert(0,"0.0")
z_text.grid(row=1, column=4)

Label(position_frame, text="W/J4").grid(row=0, column=5)
w_text = Entry(position_frame)
w_text.insert(0,"0.0")
w_text.grid(row=1, column=5)

Label(position_frame, text="P/J5").grid(row=0, column=6)
p_text = Entry(position_frame)
p_text.insert(0,"0.0")
p_text.grid(row=1, column=6)

Label(position_frame, text="R/J6").grid(row=0, column=7)
r_text = Entry(position_frame)
r_text.insert(0,"0.0")
r_text.grid(row=1, column=7)

Label(position_frame, text="Speed (mmSec/%)").grid(row=0, column=8)
speed_text = Entry(position_frame)
speed_text.insert(0,"50")
speed_text.grid(row=1, column=8)

Label(position_frame, text="Term Type").grid(row=0, column=9)
term_text = Entry(position_frame)
term_text.insert(0,"0.0")
term_text.grid(row=1, column=9)

Label(position_frame, text="Term Val").grid(row=0, column=10)
term_val_text = Entry(position_frame)
term_val_text.insert(0,"0.0")
term_val_text.grid(row=1, column=10)

# --- Output ---
receive_label = Label(output_frame, text='Robot Out')
receive_label.pack(side=TOP, anchor="w")
receive_entry = Text(output_frame, width=50, height=10, font=("Arial", 16))
receive_entry.pack(side=TOP, padx=10, pady=10)

sequence = send_pkg(handler.dict_to_json(getPackage.GetStatus()))

# --- Manual JSON Command Input ---
manual_frame = Frame(c_window)
manual_frame.grid(row=4, column=0, columnspan=13, pady=10, sticky="w")

Label(manual_frame, text="Manual JSON Command:").pack(side=LEFT, padx=2)
manual_entry = Entry(manual_frame, width=60)
manual_entry.pack(side=LEFT, padx=2)

def send_manual_json():
    json_cmd = manual_entry.get() + '\r\n'
    print(f"Sending manual command: {json_cmd}")
    send_pkg(json_cmd)

send_manual_btn = Button(manual_frame, text="Send", command=send_manual_json)
send_manual_btn.pack(side=LEFT, padx=2)

c_window.mainloop()