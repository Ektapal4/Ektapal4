from flask_mail import Mail, Message

def send_myemail(app_obj, sendto, subject, message):
    try:
        app_obj.config["MAIL_SERVER"] = "smtp.gmail.com"
        app_obj.config['MAIL_PORT'] = 587
        app_obj.config['MAIL_USE_TLS'] = True
        app_obj.config['MAIL_USERNAME'] ='ektapal73@gmail.com'
        app_obj.config['MAIL_PASSWORD'] ='isio iunw wzow likh'  # App password
        app_obj.config['MAIL_DEFAULT_SENDER'] ='ektapal73@gmail.com'

        mail = Mail(app_obj)
        msg = Message(subject=subject, recipients=[sendto]);
        msg.html=message;
        mail.send(msg)
        return True
    except Exception as e:
        print(" Mail Error:", e)  # Add this for debugging
        return False
