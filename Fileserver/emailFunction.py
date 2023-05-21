import smtplib
from email.mime.text import MIMEText

from datetime import datetime

def sendEmail(addr):
    time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    ip = addr[0]
    port = addr[1]
    sender = ""
    empfaenger = [""]
    text = f"[IP] {ip}\n[PORT] {port} \n[TIME] {time}"
    betreff = f"LOGIN {time}"
    passwort = ""
    
    
    msg = MIMEText(text)
    msg["Subject"] = betreff
    msg["From"] = sender
    msg["To"] = ", ".join(empfaenger)
    smtpServer = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpServer.login(sender, passwort)
    smtpServer.sendmail(sender, empfaenger, msg.as_string())
    smtpServer.quit()

