# xFreeRdp-connect
Simple minimail GUI for xFreeRdp based on Python 3 Tkinter

**Installation instructions:**

Clone this project:  

    git clone https://github.com/xtimon/xFreeRdp-connect.git ~/.viewrdp

Install python3 Tkinter: 

    sudo apt-get install python3-tk

Prepare application label:

    sed -i "s|/home/user/|$HOME/|g" ~/.viewrdp/xfreepy.desktop

Create application label:

    sudo ln -s ~/.viewrdp/xfreepy.desktop /usr/share/applications/

**The configuration file will be stored here:**

    ~./viewrdp/config.conf

**An example configuration file:**

    [Connection_name]
    wsize = 1700x1000
    ip_address = 192.168.10.10
    username = User
    password = Password
    
    [Connection_name2]
    wsize = 1700x1000
    ip_address = 192.168.10.11:3122
    username = User2
    password = Password2


