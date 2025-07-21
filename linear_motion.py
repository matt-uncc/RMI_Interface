
from tkinter import *
import socket
from handler import handlerDict
from FRC_ import FRC_
import time

handler = handlerDict()
getPackage = FRC_()
motion_data = FRC_().dict



# create GUI window
c_window = Tk()
c_window.geometry('600x200+50+50')
c_window.title('Test Client')


# initialize socket
global s
ip_connect = "192.168.2.100"
port_connect = 16002
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip_connect, port_connect))

# preinitialize values





















def button_submit():
    sequence = button_get_status()

    if s:
            # note \r \n is interpret as backslash so don't try to include them in regular input instead 
            # I include them automatically after each commnd input 
        x = x_text.get()
        y = y_text.get()
        z = z_text.get()
        w = w_text.get()
        p = p_text.get()
        r = r_text.get()
        motion_package = getPackage.LinearMotion(sequence, x , y ,z, w, p ,r)
        # package = handler.update_value(called_entry)
        pkg = handler.dict_to_json(motion_package)
        send_pkg(pkg)
    else:
        receive_entry.insert("1.0", "connection is not established")
    return



def button_reset():
    pkg = getPackage.Reset()
    pkg = handler.dict_to_json(pkg)
    send_pkg(pkg)
    return

def button_pause():
    pkg = getPackage.Pause()
    pkg = handler.dict_to_json(pkg)
    send_pkg(pkg)
    return

def button_abort():
    pkg = getPackage.Abort()
    pkg = handler.dict_to_json(pkg)
    send_pkg(pkg)
    return

def button_continue():
    pkg = getPackage.Continue()
    pkg = handler.dict_to_json(pkg)
    send_pkg(pkg)
    return

def button_disconnect():
    pkg = getPackage.Disconnect()
    pkg = handler.dict_to_json(pkg)
    send_pkg(pkg)
    return

def button_get_status():
    pkg = getPackage.GetStatus()
    pkg = handler.dict_to_json(pkg)
    rcvd = send_pkg(pkg)
    sequence =get_sequenceID(rcvd)
    return sequence

def button_get_curr_pos():
    pkg = getPackage.ReadCartesianPosition()
    pkg = handler.dict_to_json(pkg)
    rcvd = send_pkg(pkg)
    update_position(rcvd)
    return   

def update_position(pkg):
    global motion_data  # Avoid using 'dict' as a variable name
    data = handler.json_to_dict(pkg)
    print(data)

    config = data.get('Configuration', {})
    pos = data.get('Position', {})

    lm = motion_data.setdefault('FRC_LinearMotion', {})
    lm['UToolNumber'] = config.get('UToolNumber')
    lm['UFrameNumber'] = config.get('UFrameNumber')
    lm['Front'] = config.get('Front')
    lm['Up'] = config.get('Up')
    lm['Left'] = config.get('Left')
    lm['Flip'] = config.get('Flip')
    lm['Turn4'] = config.get('Turn4')
    lm['Turn5'] = config.get('Turn5')
    lm['Turn6'] = config.get('Turn6')



    position = lm.setdefault('Position', {})
    position['X'] = str(round(pos.get('X', 0.0), 3))
    position['Y'] = str(round(pos.get('Y', 0.0), 3))
    position['Z'] = str(round(pos.get('Z', 0.0), 3))
    position['W'] = str(round(pos.get('W', 0.0), 3))
    position['P'] = str(round(pos.get('P', 0.0), 3))
    position['R'] = str(round(pos.get('R', 0.0), 3))

    # Clear and insert rounded values into GUI text boxes
    x_text.delete(0, 'end')
    x_text.insert(0, str(position['X']))

    y_text.delete(0, 'end')
    y_text.insert(0, str(position['Y']))

    z_text.delete(0, 'end')
    z_text.insert(0, str(position['Z']))

    w_text.delete(0, 'end')
    w_text.insert(0, str(position['W']))

    p_text.delete(0, 'end')
    p_text.insert(0, str(position['P']))

    r_text.delete(0, 'end')
    r_text.insert(0, str(position['R']))



    return

            




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

def get_sequenceID(pkg):
    global sequence
    dict = handler.json_to_dict(pkg)
    for item in dict:
        if item == 'NextSequenceID':
            sequence = dict['NextSequenceID']
    return sequence




# def recieve_box():
#     receive_info.delete("1.0",END)
#     receive_info.insert("1.0",json.dumps(called_entry)) 




# def submit_button(): 
#     data = receive_info.get("1.0", END).strip() + '\r\n'
#     try:
#         s.send(data.encode('ascii')) 
#         s.settimeout(5)
#         try:
#             rcvd = s.recv(1024)
#         except socket.timeout:
#             print("time out waiting for return messages")
#         receive_entry.delete("1.0", END)
#         receive_entry.insert("1.0", rcvd)
#     except Exception as e:
#         receive_entry.delete("1.0", END)
#         receive_entry.insert("1.0", f"Send failed: {e}" )
#     return



# Linear Move
# x pos
x_label = Label(text = 'X')
x_label.grid(row = 0, column = 0)

x_text = Entry()
x_text.insert(0, '0.0')
x_text.grid(row = 1, column = 0)

# y pos
y_label = Label(text = 'Y')
y_label.grid(row = 0, column = 1)

y_text = Entry()
y_text.insert(0,"0.0")
y_text.grid(row = 1, column = 1)

# z pos
z_label = Label(text = 'Z')
z_label.grid(row = 0, column = 2)

z_text = Entry()
z_text.insert(0,"0.0")
z_text.grid(row = 1, column = 2)


# w angle
w_label = Label(text = 'W')
w_label.grid(row = 0, column = 3)

w_text = Entry()
w_text.insert(0,"0.0")
w_text.grid(row = 1, column = 3)

# p angle
p_label = Label(text = 'P')
p_label.grid(row = 0, column = 4)

p_text = Entry()
p_text.insert(0,"0.0")
p_text.grid(row = 1, column = 4)

# r angle
r_label = Label(text = 'R')
r_label.grid(row = 0, column = 5)

r_text = Entry()
r_text.insert(0,"0.0")
r_text.grid(row = 1, column = 5)


submit_btn = Button(c_window, text = 'Submit', command = button_submit)
submit_btn.grid(row = 1, column = 7)





# Reset Button 
reset_btn = Button(c_window, text = 'Reset', command = button_reset)
reset_btn.grid(row = 2, column = 0)
# Pause Button 
pause_btn = Button(c_window, text = 'Pause', command = button_pause)
pause_btn.grid(row = 2, column = 1)
#  Button 
continue_btn = Button(c_window, text = 'Continue', command = button_continue)
continue_btn.grid(row = 2, column = 2)
# Reset Button 
abort_btn = Button(c_window, text = 'Abort', command = button_abort)
abort_btn.grid(row = 2, column = 3)
# disconnect
disconnect_btn = Button(c_window, text = 'Disconnect', command = button_disconnect)
disconnect_btn.grid(row = 2, column = 4)
# get status
getST_btn = Button(c_window, text = 'GetStatus', command = button_get_status)
getST_btn.grid(row = 2, column = 5)

# Get current Cartesian pos
get_curr_pos_btn = Button(c_window, text = 'GetPos', command = button_get_curr_pos)
get_curr_pos_btn.grid(row = 3, column = 0)


receive_label = Label(text = 'Robot Out')
receive_label.grid(row = 2, column = 6)

receive_entry = Text(c_window, width=50, height=10, font=("Arial", 16))
receive_entry.grid(row = 2, column = 6)

# request_info = Label(text= "input_field" )
# request_info.grid(row=0, column= 2)

# receive_info = Text(c_window, width=50, height=10, font=("Arial", 16))
# receive_info.grid(row = 1, column=2)

# submit_info = Button(c_window, text='submit', command= submit_button)
# submit_info.grid(row = 3, column=3)


send_pkg(handler.dict_to_json(getPackage.Connect()))
send_pkg(handler.dict_to_json(getPackage.Reset()))
send_pkg(handler.dict_to_json(getPackage.Initialize()))
sequence = send_pkg(handler.dict_to_json(getPackage.GetStatus()))


c_window.mainloop()