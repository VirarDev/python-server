import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys

# BOT_MAIL = "Helper.gcc@outlook.com" #spamed
BOT_MAIL = "helper.vac@outlook.com"

BOT_MAIL_PASS = "Jayaraj@87"

def getLoginOutlook():
    # if("smtpConnectionToOutlook" in sys.SharedMemory):
    #     return sys.SharedMemory["smtpConnectionToOutlook"]
    sys.SharedMemory["smtpConnectionToOutlook"] = smtplib.SMTP('smtp-mail.outlook.com', 587)
    sys.SharedMemory["smtpConnectionToOutlook"].starttls()
    sys.SharedMemory["smtpConnectionToOutlook"].login(BOT_MAIL, "Jayaraj@87")
    return sys.SharedMemory["smtpConnectionToOutlook"]

def mail(body):
    try:
        # user = body["USER"]
        # if (not (isinstance(user, str)) or (user.strip() == "") or ("/" in user) or ("\\" in user)):
        #     return "Invalid User"
        mail_to = body["MAIL_TO"]
        subject = body["SUBJECT"]
        body_content = body["BODY"]

        sent = send_outlook_email(mail_to, subject, body_content)
        return {"is_mail_sent":sent}
    except Exception as e:
        return "Error : "+str(e)


def stop_email():
    getLoginOutlook().quit()
    return "Stoped Mailing Service"


def send_outlook_email(mail_to, subject, body_content):
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = BOT_MAIL
    msg['To'] = mail_to
    msg['Subject'] = subject

    # Attach message
    msg.attach(MIMEText(body_content, 'plain'))

    try:
        # Send email
        getLoginOutlook().sendmail(BOT_MAIL, mail_to, msg.as_string())
        return True
    except Exception as e:
        return False
