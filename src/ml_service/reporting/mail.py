import smtplib
import os

def send_email(message):
    __script_dir = os.path.abspath(__file__ + "/../")
    __rel_path = r'credentials.txt'
    __output_directory = os.path.join(__script_dir, __rel_path)

    passwd_file = open('credentials.txt', 'r')
    line = passwd_file.readline()
    line = line.split('\t')
    sender = line[0]
    password = line[1]
    recepient = line[2]
    print("sending email")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, recepient, ("\r\n" + message))
    server.quit()