#!/usr/bin/env python3
import os
import subprocess
import configparser
from tkinter import *
from tkinter import ttk
root = Tk()

# You can configure these settings:
window_width = str(root.winfo_screenwidth() - 70)
# example: window_width = "1700"

window_height = str(root.winfo_screenheight() - 70)
# example: window_height = "1000"

window_size = "{}x{}".format(window_width, window_height)
homepath = str(os.getenv("HOME"))
fwd_path = homepath
# example: fwd_path = "/path/to"

config_file = "{}/.viewrdp/config.conf".format(homepath)
# example: config_file = "/path/to/config.conf"

icon_file = "{}/.viewrdp/icon.png".format(homepath)
# example: icon_file =

bg_color = "#DF7401"
save_button_color = "#0B3B17"
connect_button_color = "#61380B"
delete_button_color = "#B40404"
buttons_font_color = "#F6E3CE"

connect_list = []
connect_list.append("")
config = configparser.ConfigParser()
if os.path.isfile(config_file):
    config.read_file(open(config_file))
    connect_list.extend(config.sections())
    connect_list.sort()


def my_init(action, value):
    global connect_list
    if action == "delete":
        delete_values()
        connect_list.remove(value)
        connections_list.set("")
        ipaddr.focus_set()
    if action == "save":
        if value not in connect_list:
            connect_list.append(value)
        connections_list.set(value)
        connect.focus_set()
    connections_list.configure(values=connect_list)
    button_name()


def button_name():
    if connections_list.get():
        get_connection_name.configure(text='change')
    else:
        get_connection_name.configure(text='save')


def delete_values():
    username.delete(0, 'end')
    ipaddr.delete(0, 'end')
    password.delete(0, 'end')
    button_name()


def insert_values(value):
    delete_values()
    if connections_list.get():
        username.insert(0, config.get(connections_list.get(), 'username'))
        ipaddr.insert(0, config.get(connections_list.get(), 'ip_address'))
        password.insert(0, config.get(connections_list.get(), 'password'))
    connect.focus_set()


def connect():
    if ipaddr.get() and username.get() and password.get():
        if wsize.get():
            connect_wsize = wsize.get()
        else:
            connect_wsize = "800x600"
        proc = subprocess.Popen(["xfreerdp", "-u", username.get(),
                                 "-p", password.get(),
                                 "-g", connect_wsize,
                                 "--ignore-certificate",
                                 "--plugin", "cliprdr",
                                 "--plugin", "rdpdr",
                                 "--data", "disk:MyPC:" + fwd_path,
                                 "--", ipaddr.get()],
                                stdout=subprocess.PIPE)
        root.destroy()
        proc.wait()
        subprocess.Popen(["notify-send", "-i", icon_file,
                          "FreeRDP message:", str(proc.communicate()[0])],
                         stdout=subprocess.PIPE)


def get_connection_name():
    def save_connect():
        if connection_name.get() and ipaddr.get() and username.get() and password.get():
            config[connection_name.get()] = {'ip_address': ipaddr.get(),
                                             'username': username.get(),
                                             'password': password.get()}
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            my_init("save", connection_name.get())
            save_window.destroy()

    def delete_connect():
        config.remove_section(connection_name.get())
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        my_init("delete", connection_name.get())
        save_window.destroy()

    save_window = Tk()
    save_window.configure(bg=bg_color)
    save_window.resizable(0, 0)
    connection_name = Entry(save_window, width=20, bd=3, font='12')
    connection_name.insert(0, connections_list.get())
    connection_name.grid(row=1, column=1, columnspan=2)
    if connections_list.get():
        save_window.title("Change connection")
        delete_connection = Button(save_window, text='delete', width=7, font='12', bg=delete_button_color,
                                   fg=buttons_font_color, command=delete_connect)
        delete_connection.grid(row=2, column=1)
        save_connection = Button(save_window, text='save', width=7, font='12', bg=save_button_color,
                                 fg=buttons_font_color, command=save_connect)
        save_connection.grid(row=2, column=2)
    else:
        save_window.title("Save connection")
        save_connection = Button(save_window, text='save', width=18, font='12', bg=save_button_color,
                                 fg=buttons_font_color, command=save_connect)
        save_connection.grid(row=2, column=1, columnspan=2)
    save_window.mainloop()


root.configure(bg=bg_color)
root.resizable(0, 0)
root.title("xFreeRdp connect")
root.minsize(300, 135)

ipaddr = Entry(root, width=20, bd=3, font='12')
ipaddr.grid(row=1, column=1)

ipaddr_label = Label(root, text='ip address', bg=bg_color, font='12')
ipaddr_label.grid(row=1, column=2, columnspan=2)

username = Entry(root, width=20, bd=3, font='12')
username.grid(row=2, column=1)

username_label = Label(root, text='username', bg=bg_color, font='12')
username_label.grid(row=2, column=2, columnspan=2)

password = Entry(root, width=20, bd=3, show="*", font='12')
password.grid(row=3, column=1)

password_label = Label(root, text='password', bg=bg_color, font='12')
password_label.grid(row=3, column=2, columnspan=2)

wsize = Entry(root, width=20, bd=3, font='12')
wsize.insert(0, window_size)
wsize.grid(row=4, column=1)

wsize_label = Label(root, text='window size', bg=bg_color, font='12')
wsize_label.grid(row=4, column=2, columnspan=2)

connections_list = ttk.Combobox(width=22, values=connect_list, height=20)
connections_list.grid(row=5, column=1)
connections_list.bind("<<ComboboxSelected>>", insert_values)
connections_list.focus_set()

get_connection_name = Button(root, text='save', width=4, font='12', bg=save_button_color,
                             fg=buttons_font_color, command=get_connection_name)
get_connection_name.grid(row=5, column=2)

connect = Button(root, text='connect', width=5, font='12', bg=connect_button_color,
                 fg=buttons_font_color, command=connect)
connect.grid(row=5, column=3)

root.mainloop()
