#DataTransMitter
# Tool = "RFID Reader"
# HandcraftedBy : "AIVolved"\
# Version = "1.3"
# LastModifiedOn : "19th April 2022"
#______________________________________________________________________

import serial
import sys
import Resources
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui ,QtCore
import time
import smtplib
from threading import*

com1 = 'COM3'  # user should input
com2 = 'COM6'  # user should input
RecipietnMailID = "test233155ID@gmail.com"
tag_hex_value_list = []

Database = {
'EEEE0000E2E2808011117070' : "TestData1",
'303ACA4780DE93199C82FABD' : "TestData2",
'000000000000000000000000' : "InvalidData",
'EEEE000030303A3ACACA4747' : "TestData3",
'0000000011110000EEEE0000' : "TestData4",
'303ACA4780DE93199C82FA7A' : "TestData5" }


def showUserInfo(message):
   msgBox = QMessageBox()
   msgBox.setIcon(QMessageBox.Information)
   msgBox.setText(message)
   msgBox.setWindowTitle("Status Info")
   msgBox.setStandardButtons(QMessageBox.Ok)
   msgBox.show()

   returnValue = msgBox.exec()
   if returnValue == QMessageBox.Ok: pass
   else: pass


def convert_tag_from_bytes_to_hex(tag_bytes_list):
    #print("returning", tag_bytes_list)
    tag_hex_value = ""
    for index in range(len(tag_bytes_list)):
        #print("inside for",tag_bytes_list[index])
        #   First 3 bytes and last byte are placeholders
        if index > 3 and index < 16:
            tag_hex_value += "{0:02X}".format(tag_bytes_list[index])
    #print(tag_hex_value)
    return tag_hex_value
    
try:
    serial_device_1 = serial.Serial(
            com1, 57600, timeout=0.5
        )
    serial_device_2 = serial.Serial(
            com2, 57600, timeout=0.5
        )
except serial.serialutil.SerialException as err:
        try:
            showUserInfo('There was a problem while opening the ports for the reader')  # this will throw error message
        except:
            pass

def run_test():
    global tag_hex_value_list
   

    tag_bytes_list_for_device_1 = []
    tag_bytes_list_for_device_2 = []

    

    should_read_tag_from_device_1 = False
    should_read_tag_from_device_2 = False


    try:
        serial_device_1.reset_input_buffer()
        serial_device_2.reset_input_buffer()
        while True:
            if len(tag_hex_value_list)>=400:
                tag_hex_value_list.clear()
            #print("herheree")
            read_bytes_from_device_1 = serial_device_1.read()
            int_value_from_device_1 = int.from_bytes(
                read_bytes_from_device_1, "big")
            # print(int_value_from_device_1)
            read_bytes_from_device_2 = serial_device_2.read()
            int_value_from_device_2 = int.from_bytes(
                read_bytes_from_device_2, "big"
            )
            sys.stdout.flush()

            if int_value_from_device_1 == 0x11:
                should_read_tag_from_device_1 = True
            if int_value_from_device_2 == 0x11:
                should_read_tag_from_device_2 = True

            if should_read_tag_from_device_1 is True:
                tag_bytes_list_for_device_1.append(int_value_from_device_1)
            if should_read_tag_from_device_2 is True:
                tag_bytes_list_for_device_2.append(int_value_from_device_2)

                if len(tag_bytes_list_for_device_1) == 18:
                    should_read_tag_from_device_1 = False
                    tag_hex_value = convert_tag_from_bytes_to_hex(tag_bytes_list_for_device_1)
               
                    if tag_hex_value not in tag_hex_value_list:
                        
                        tag_hex_value_list.append(tag_hex_value)
                        print(f"Tag list device 1: {tag_hex_value_list}")  # this has to be displayed
                    tag_bytes_list_for_device_1.clear()
                    serial_device_1.flush()
                    serial_device_1.reset_input_buffer()

            if should_read_tag_from_device_2 is True:
                tag_bytes_list_for_device_2.append(int_value_from_device_2)

                if len(tag_bytes_list_for_device_2) == 18:
                    should_read_tag_from_device_2 = True
                    tag_hex_value = convert_tag_from_bytes_to_hex(tag_bytes_list_for_device_2)
                    if tag_hex_value not in tag_hex_value_list:
                        tag_hex_value_list.append(tag_hex_value)
                        print(f"Tag list device 2: {tag_hex_value_list}")
                    tag_bytes_list_for_device_2.clear()
                    serial_device_2.flush()
                    serial_device_2.reset_input_buffer()


    except : pass






if __name__ == "__main__":

    Aplication = QApplication(sys.argv)
    MainWindowGUI = QWidget()
    MainWindowGUI.setFixedSize(780, 400)
    MainWindowGUI.setWindowTitle('RFID Reader')
    MainWindowGUI.setStyleSheet("background-color: black;")
    MainWindowGUI.setObjectName("MainMenu");
    IconFilepath = ":/resources/Icon.ico"
    MainWindowGUI.setStyleSheet("QWidget#MainMenu{background-image: url(:/resources/BackGroundImage.jpg);}");
    MainWindowGUI.setWindowIcon(QtGui.QIcon(IconFilepath))
    MainWindowGUI.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    LogTable = QTableWidget(MainWindowGUI)
    LogTable.setRowCount(505)
    LogTable.setColumnCount(2)
    LogTable.move(45, 60)
    LogTable.setFixedSize(500, 300)
    LogTable.setStyleSheet("background-color: 	white" "")
    RFIDTagID = QTableWidgetItem("RFID ID")
    RFIDTagValue = QTableWidgetItem("Product")
    LogTable.setHorizontalHeaderItem(0, RFIDTagID)
    LogTable.setHorizontalHeaderItem(1, RFIDTagValue)

    prevSentTime = 0
    currTransmitAttemptTime =0
    def SendEmail():
        return
        global prevSentTime,currTransmitAttemptTime
        currTransmitAttemptTime = time.time()

        if (currTransmitAttemptTime-prevSentTime) > 5 :
             pass
        else :
            showUserInfo("Attempt after min 5 seconds have elapsed since the last email attempt"+\
                         "\n"+"Time elapsed : "+str(currTransmitAttemptTime-prevSentTime)[0:5]+" seconds")
            return


        gmail_user = 'arun5k10@gmail.com'
        gmail_password = 'Indiannavy1'

        sent_from = gmail_user
        to = ['arun5k1095@gmail.com', 'arun5k10@gmail.com']
        subject = 'Python Test Email'
        body = 'consectetur adipiscing elit'


        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(gmail_user, gmail_password)
            smtp_server.sendmail(sent_from, to, "This is test mail")
            smtp_server.close()
            #RFIDinfoDisplayWindow.setText("Email sent successfully!")
        except Exception as ex:
            #RFIDinfoDisplayWindow.setText(str(ex))
            pass

    def SystemExit():
        
        serial_device_1.flush()
        serial_device_1.reset_input_buffer()
        serial_device_1.close()

        serial_device_2.flush()
        serial_device_2.reset_input_buffer()
        serial_device_2.close()
        
        #sys.exit(0)
        
        MainWindowGUI.close()
    def ScanRFID():
        pass
    def UpdateDispalyTable():
        while True:
            if len(tag_hex_value_list) > 0 :
                try:
                    global LogTable
                    for rfidDataPosition in range(len(tag_hex_value_list)):
                        LogTable.setItem(rfidDataPosition,0 , QTableWidgetItem(str(tag_hex_value_list[rfidDataPosition])))
                        LogTable.setItem(rfidDataPosition,1, QTableWidgetItem(str(Database[str(tag_hex_value_list[rfidDataPosition])])))
                        LogTable.update()
                except Exception as error :
                    print(error)


    Task1 = Thread(target=run_test)
    Task2 = Thread(target=UpdateDispalyTable)

    def ReadRFID():
        try:
            if not Task1.is_alive():
                Task1.start()
            else:
                showUserInfo("RFID read already initiated")

            if not Task2.is_alive():
                Task2.start()
            else:
                pass

        except Exception as error:
            print(error)
        


    ButtonScan = QPushButton("Scan" , MainWindowGUI)
    ButtonScan.setFixedSize(100,40)
    ButtonScan.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}")
    ButtonScan.move(650,50)
    ButtonScan.clicked.connect(ScanRFID)

    ButtonRead = QPushButton("Read" , MainWindowGUI)
    ButtonRead.setFixedSize(100,40)
    ButtonRead.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}")
    ButtonRead.move(650,100)
    ButtonRead.clicked.connect(ReadRFID)

    ButtonSend = QPushButton("Send" , MainWindowGUI)
    ButtonSend.setFixedSize(100,40)
    ButtonSend.setStyleSheet("QPushButton {border: 1px blue;border-radius: 5px;  background-color: #075691; color : white;}""QPushButton::hover"
            "{"
            "background-color : #1a85b4;"
            "}")
    ButtonSend.move(650,150)


    def SaveConfiguration():
        global com1,com1 ,RecipietnMailID

        com1 =COM1_inp.text().strip()
        com2 =COM2_inp.text().strip()
        RecipietnMailID = RecipientID_inp.text()
        DialogueBox.close()


    DialogueBox = QDialog(MainWindowGUI)
    DialogueBox.setFixedSize(300, 170)
    DialogueBox.setStyleSheet("background-color: 	white" "")
    DialogueBox.setWindowTitle("Settings")
    formGroupBox = QGroupBox("Product Configurations")
    layout = QFormLayout()
    COM1_inp = QLineEdit()
    COM2_inp = QLineEdit()
    RecipientID_inp = QLineEdit()
    layout.addRow(QLabel("COM 1"), COM1_inp)
    layout.addRow(QLabel("COM 2"), COM2_inp)
    layout.addRow(QLabel("Recipient mailID"), RecipientID_inp)
    formGroupBox.setLayout(layout)

    buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
    buttonBox.accepted.connect(SaveConfiguration)
    buttonBox.rejected.connect(DialogueBox.close)

    mainLayout = QVBoxLayout()

    mainLayout.addWidget(formGroupBox)
    mainLayout.addWidget(buttonBox)
    DialogueBox.setLayout(mainLayout)

    def SystemSettings():
        COM1_inp.setText(com1)
        COM2_inp.setText(com2)
        RecipientID_inp.setText(RecipietnMailID)

        DialogueBox.exec_()


    ButtonSend.clicked.connect(SystemSettings)

    toolbar = QToolBar(MainWindowGUI)
    toolbar.move(0,0)
    #toolbar.addToolBar(MainWindowGUI)


    toolButton = QToolButton()
    toolButton.setText("Settings")
    toolButton.setIcon(QIcon(":/resources/ConfigIcon.JPG"))
    toolButton.clicked.connect(SystemSettings)

    toolButtonClose = QToolButton()
    toolButtonClose.setText("System Exit")
    toolButtonClose.setIcon(QIcon(":/resources/CloseIcon.JPG"))
    toolButtonClose.clicked.connect(SystemExit)
    toolbar.addWidget(toolButtonClose)


    toolbar.addWidget(toolButton)
    button_action = QAction(QIcon("bug.png"),"Your button", MainWindowGUI)
    button_action.setStatusTip("This is your button")
    button_action.triggered.connect(SystemSettings)
    button_action.setCheckable(True)
    toolbar.addAction(button_action)

    MainWindowGUI.show()
    sys.exit(Aplication.exec_())