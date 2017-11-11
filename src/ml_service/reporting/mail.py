import smtplib

def send_email(message):
    print("sending email")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("soen490.justice@gmail.com", "bustychicks")
    server.sendmail("soen490.justice@gmail.com", "samuel.pcampbell@gmail.com", ("\r\n" + message))
    server.quit()