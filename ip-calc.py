
"""
    This script is programmed by Mouhab-dev
    Follow me on Github: https://github.com/mouhab-dev
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from ipgui import Ui_MainWindow
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# Function to convert Decimal to Binary
def dtb(n):
    return format(n,'08b')

# Function to convert from CIDR Notation to Subnet mask
def cidr_to_subnet(CIDR):
    counter = 0
    subnet=[]
    while (CIDR>8):
        CIDR = CIDR-8
        counter +=1
    for i in range(4):
        if i < counter:
            subnet.append(255)
        elif i == counter:
            subnet.append(256-pow(2,(8-CIDR)))
        else:
            subnet.append(0)
    return subnet

# Hide Group Box By Default
ui.groupBox.setHidden(True)

# Hide Error labels by Default
ui.label_17.setHidden(True)
ui.label_18.setHidden(True)

def reset():
    ui.groupBox.setHidden(True)
    ui.label_17.setHidden(True)
    ui.label_18.setHidden(True)

def calculate():
    # Get user input for IP Address
    try:
        ip = list(map(int,ui.lineEdit.text().split('.')))
        # Error handling for ip address
        if len(ip) != 4 :
            ui.label_17.setText("IP Format: x.x.x.x")
            ui.label_17.setHidden(False)
            return False
        for i in ip:
            if i > 255:
                ui.label_17.setText("IP Range: (0-255)")
                ui.label_17.setHidden(False)
                return False
    except ValueError:
        ui.label_17.setText("Only digits allowed!")
        ui.label_17.setHidden(False)
        return False
    except:
        ui.label_17.setText("Error !")
        return False
    
    subnet=[]
    # Get user input for subnet mask
    try:
        CIDR = ui.lineEdit_2.text()
        if CIDR[0] == '/':
            CIDR=int(CIDR[1:])
            if not CIDR in range(8,31):
                ui.label_18.setText("CIDR Range (8-30)")
                ui.label_18.setHidden(False)
                return False
            else:
                subnet=cidr_to_subnet(CIDR)
        else:
            subnet = list(map(int,CIDR.split('.')))
            if subnet[0] != 255:
                ui.label_18.setText("Must begin with 255")
                ui.label_18.setHidden(False)
                return False
        # Error handling for subnet
        if len(subnet) != 4 :
            ui.label_18.setText("Valid Format: x.x.x.x")
            ui.label_18.setHidden(False)
            return False
        for j in subnet:
            # Check if the number exceeds 255
            if j > 255:
                ui.label_18.setText("Valid Range (0-255)")
                ui.label_18.setHidden(False)
                return False
            # Check for invalid subnetmask (continous binary ones)
            if '01' in dtb(j):
                ui.label_18.setText("Invalid subnet mask")
                ui.label_18.setHidden(False)
                return False
    except ValueError:
        ui.label_18.setText("Only digits allowed!")
        ui.label_18.setHidden(False)
        return False
    except:
        ui.label_18.setText("Error !")
        return False

    subnet_ones=0 # count no of ones in subnet mask
    t_no_hosts=0 # calculate total number of hosts
    network_id=[] # list to store network id
    broadcast_address=[0,0,0,0] # list to store broadcast address

    # Program Logic
    for i in range(4):
        # count the number of ones in the subnet mask
        subnet_ones = subnet_ones + len(dtb(subnet[i]).strip('0'))
        
        # perform a logical and operation between ip and subnet mask to get the network id
        network_id.append(int(ip[i]) & int(subnet[i]))

        # Calculate Broadcast Address
        if subnet[i] == 255 :
            broadcast_address[i] = network_id[i]
        else:
            broadcast_address[i] = 255 - subnet[i] + network_id[i]

    # Output the result using labels in GUI
    # Print the CIDR Notation for the given subnet mask
    ui.label_16.setText(str(subnet_ones))

    # Print Network ID
    ui.label_9.setText('.'.join(map(str, network_id)))

    # Calculate Total Number of Hosts in the subnet
    t_no_hosts = pow(2,32-subnet_ones) - (2)

    # Print First Host Address
    first_id = network_id.copy()
    first_id[3] += 1
    ui.label_10.setText('.'.join(map(str, first_id)))

    # Print Last Host Address
    last_address = broadcast_address.copy()
    last_address[3] -= 1
    ui.label_11.setText('.'.join(map(str, last_address)))

    # Print Broadcast Address
    ui.label_12.setText('.'.join(map(str, broadcast_address)))

    # Print Total Number of Hosts
    ui.label_13.setText(str(t_no_hosts))
    
    # Unhide the Group Box
    ui.groupBox.setHidden(False)

    return 0

# Conncections
# PushButton
ui.pushButton.setAutoDefault(True)
ui.pushButton.clicked.connect(calculate)
# LineEdit
ui.lineEdit.returnPressed.connect(calculate)
ui.lineEdit.textChanged.connect(reset)
# LineEdit_2
ui.lineEdit_2.returnPressed.connect(calculate)
ui.lineEdit_2.textChanged.connect(reset)

# Exit successfully
sys.exit(app.exec_())