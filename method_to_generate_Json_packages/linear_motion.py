
from tkinter import *
import socket
import json
from handler import handlerDict

handler = handlerDict()

# create a dictionary from text file
with open('from_manual.txt', 'r') as file:
    file_content = file.read()
    dict = handler.convert_data_to_dict(file_content)



# create GUI window
c_window = Tk()
c_window.geometry('600x200+50+50')
c_window.title('Test Client')


# initialize socket
# ip_connect = '192.168.1.100'
# port_connect = '16002'
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((ip_connect, port_connect))


# def button_connect():
#     global s
#     ip_connect = ip_text.get()
#     port_connect = int(port_text.get())

#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((ip_connect, port_connect))
#         receive_entry.insert("1.0", "connection established")
#     except Exception as e:
#         receive_entry.insert("1.0", f"fail to connect: {e}")

#     return

# def button_submit():
#     pass


def create_pkg(dict ,X, Y ,Z , W, P, R):
    updated_dict = dict
    for item in dict:
        if item == 'X':
            updated_dict[item] = X
        if item == 'Y':
            updated_dict[item] = Y
        if item == 'Z':
            updated_dict[item] = Z
        if item == 'W':
            updated_dict[item] = W
        if item == 'P':
            updated_dict[item] = P
        if item == 'R':
            updated_dict[item] = R
        else:
            continue
    return updated_dict



def button_submit():
    global s
    if s:
            # note \r \n is interpret as backslash so don't try to include them in regular input instead 
            # I include them automatically after each commnd input 
        x = x_text.get()
        y = y_text.get()
        z = z_text.get()
        w = w_text.get()
        p = p_text.get()
        r = r_text.get()
        motion_package = create_pkg(dict['PRC_LinearMotion'], x , y ,z, w, p ,r)
        # package = handler.update_value(called_entry)
        data = motion_package + '\r\n'
        try:
            s.send(data.encode('ascii')) 
            s.settimeout(5)
            try:
                rcvd = s.recv(1024)
            except socket.timeout:
                print("time out waiting for return messages")

            receive_entry.delete("1.0", END)
            receive_entry.insert("1.0", rcvd)
        except Exception as e:
            receive_entry.delete("1.0", END)
            receive_entry.insert("1.0", f"Send failed: {e}" )
        return

        receive_info.delete("1.0",END)
        receive_info.insert("1.0",json.dumps(called_entry))        
    else:
        receive_entry.insert("1.0", "connection is not established")
    return



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
y_text.grid(row = 1, column = 1)\

# z pos
z_label = Label(text = 'Y')
z_label.grid(row = 0, column = 2)

z_text = Entry()
z_text.insert(0,"0.0")
z_text.grid(row = 1, column = 2)


# w angle
w_label = Label(text = 'Y')
w_label.grid(row = 0, column = 3)

w_text = Entry()
w_text.insert(0,"0.0")
w_text.grid(row = 1, column = 3)

# p angle
p_label = Label(text = 'Y')
p_label.grid(row = 0, column = 4)

p_text = Entry()
p_text.insert(0,"0.0")
p_text.grid(row = 1, column = 4)

# r angle
r_label = Label(text = 'Y')
r_label.grid(row = 0, column = 5)

r_text = Entry()
r_text.insert(0,"0.0")
r_text.grid(row = 1, column = 5)


submit_btn = Button(c_window, text = 'Submit', command = button_submit)
submit_btn.grid(row = 2, column = 0)

# send_label = Label(text = 'Remote Out')
# send_label.grid(row = 0, column = 3)

# send_entry = Entry(c_window, width = 60)
# send_entry.insert(0, 'FRC_')
# send_entry.grid(row = 1, column = 3)

# send_button = Button(c_window, text = 'config', command = button_config)
# send_button.grid(row = 2, column = 3)

receive_label = Label(text = 'Robot Out')
receive_label.grid(row = 3, column = 0)

receive_entry = Text(c_window, width=50, height=10, font=("Arial", 16))
receive_entry.grid(row = 3, column = 0)

# request_info = Label(text= "input_field" )
# request_info.grid(row=0, column= 2)

# receive_info = Text(c_window, width=50, height=10, font=("Arial", 16))
# receive_info.grid(row = 1, column=2)

# submit_info = Button(c_window, text='submit', command= submit_button)
# submit_info.grid(row = 3, column=3)


c_window.mainloop()