from tkinter import *
import socket
from handler import handlerDict
from FRC_ import FRC_
import time
from command import Command
from pkg_2_call import MotionMethod


handler = handlerDict()
getPackage = FRC_()

move= ["LinearMotion", "JointMotion", "LinearRelativeMotion", "JointRelativeMotion"] 


# create GUI window
c_window = Tk()
c_window.geometry('600x200+50+50')
c_window.title('Test Client')


# initialize socket
# global s
# ip_connect = "192.168.1.100"
# port_connect = 16002
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.settimeout(5)  # Set a timeout for the socket operations
# try:
#     s.connect((ip_connect, port_connect))
# except socket.timeout:
#     print(f"Error connecting to socket at {ip_connect}:{port_connect}")


# create a dictionary from text file
with open('from_manual.txt', 'r') as file:
    file_content = file.read()
    dict = handler.json_to_dict(file_content)



def button_connect():
    global s
    ip_connect = ip_text.get()
    port_connect = int(port_text.get())

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_connect, port_connect))
        receive_entry.insert("1.0", "connection established")
    except Exception as e:
        receive_entry.insert("1.0", f"fail to connect: {e}")

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
def send_pkg(pkg):       
    try:
        s.send(pkg.encode('ascii')) 
        s.settimeout(5)
        start_time = time.time()

        while time.time() - start_time < 10:
            try:
                rcvd = s.recv(1024)
                receive_entry.delete("1.0", END)
                receive_entry.insert("1.0", rcvd)
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




def moveTo(mode):
    sequence = button_get_status()
    
    if s:
        val1 = x_text.get()
        val2 = y_text.get()
        val3 = z_text.get()
        val4 = w_text.get()
        val5 = p_text.get()
        val6 = r_text.get()
        if mode == "LinearMotion":
            motion_package = MotionMethod.linear_move(sequence, val1, val2, val3, val4, val5, val6)
            send_pkg(motion_package)

        elif mode == "LinearRelativeMotion":
            motion_package = MotionMethod.linear_relative_move(sequence, val1, val2, val3, val4, val5, val6)
            send_pkg(motion_package)
        elif mode == "JointMotion":
            motion_package = MotionMethod.joint_motion(sequence, val1, val2, val3, val4, val5, val6)
            send_pkg(motion_package)
        elif mode == "JointRelativeMotion":
            motion_package = MotionMethod.joint_relative_motion(sequence, val1, val2, val3, val4, val5, val6)
            send_pkg(motion_package)
    else:
        receive_entry.insert("1.0", "connection is not established")
    return


opt = StringVar(value="LinearMotion")  # Default value)

OptionMenu(c_window, opt, *move).grid(row=2, column=4)
Button(c_window, text="Move", command=moveTo).grid(row=1, column=11)




# button and place holder creation
port_label = Label(text = 'Port')
port_label.grid(row = 0, column = 0)

port_text = Entry()
port_text.insert(0, '16002')
port_text.grid(row = 0, column = 1)

ip_label = Label(text = 'IP Address')

ip_label.grid(row = 1, column = 0)

ip_text = Entry()
ip_text.insert(0,"192.168.1.100")
ip_text.grid(row = 1, column = 1)

connect_btn = Button(c_window, text = 'Connect', command = button_connect)
connect_btn.grid(row = 2, column = 0)


receive_label = Label(text = 'Robot Out')
receive_label.grid(row = 5, column = 4)

receive_entry = Text(c_window, width=50, height=10, font=("Arial", 16))
receive_entry.grid(row = 6, column = 1, columnspan=8, padx=10, pady=10)






# Reset Button 
reset_btn = Button(c_window, text = 'Reset', command = button_reset)
reset_btn.grid(row = 1, column = 3)
# Pause Button 
pause_btn = Button(c_window, text = 'Pause', command = button_pause)
pause_btn.grid(row = 0, column = 3)
#  Button 
continue_btn = Button(c_window, text = 'Continue', command = button_continue)
continue_btn.grid(row = 0, column = 4)
# Reset Button 
abort_btn = Button(c_window, text = 'Abort', command = button_abort)
abort_btn.grid(row = 0, column = 5)
# disconnect
disconnect_btn = Button(c_window, text = 'Disconnect', command = button_disconnect)
disconnect_btn.grid(row = 3, column = 0)
# get status
getST_btn = Button(c_window, text = 'GetStatus', command = button_get_status)
getST_btn.grid(row = 3, column = 1)


# position input
# x pos
x_label = Label(text = "X/J1")
x_label.grid(row = 0, column = 7)

x_text = Entry()
x_text.insert(0, '0.0')
x_text.grid(row = 1, column = 7)

# y pos
y_label = Label(text = "Y/J2")
y_label.grid(row = 0, column = 8)

y_text = Entry()
y_text.insert(0,"0.0")
y_text.grid(row = 1, column = 8)

# z pos
z_label = Label(text = "Z/J3")
z_label.grid(row = 0, column = 9)

z_text = Entry()
z_text.insert(0,"0.0")
z_text.grid(row = 1, column = 9)


# w angle
w_label = Label(text = "W/J4")
w_label.grid(row = 2, column = 7)

w_text = Entry()
w_text.insert(0,"0.0")
w_text.grid(row = 3, column = 7)

# p angle
p_label = Label(text = "P/J5")
p_label.grid(row = 2, column = 8)

p_text = Entry()
p_text.insert(0,"0.0")
p_text.grid(row = 3, column = 8)

# r angle
r_label = Label(text = "R/J6")
r_label.grid(row = 2, column = 9)

r_text = Entry()
r_text.insert(0,"0.0")
r_text.grid(row = 3, column = 9)

# speed
speed_label = Label(text = "Speed (mmSec)")
speed_label.grid(row = 2, column = 10)

speed_text = Entry()
speed_text.insert(0,"50")
speed_text.grid(row = 3, column = 10)
# term type
term_label = Label(text = "Term Type")
term_label.grid(row = 2, column = 11)

term_text = Entry()
term_text.insert(0,"0.0")
term_text.grid(row = 3, column = 11)

# term val
term_val = Label(text = "Term Val")
term_val.grid(row = 2, column = 12)

term_val_text = Entry()
term_val_text.insert(0,"0.0")
term_val_text.grid(row = 3, column = 12)

# submit_btn = Button(c_window, text = 'Submit', command = button_submit)
# submit_btn.grid(row = 1, column = 7)



send_pkg(handler.dict_to_json(getPackage.Connect()))
send_pkg(handler.dict_to_json(getPackage.Reset()))
send_pkg(handler.dict_to_json(getPackage.Initialize()))
sequence = send_pkg(handler.dict_to_json(getPackage.GetStatus()))

c_window.mainloop()