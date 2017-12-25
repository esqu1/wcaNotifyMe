from flask_mail import Mail, Message
import os

mail = Mail()


def create_msg(comp_name, link, recipients):
    msg = Message('[WCA NotifyMe] Time to register for %s!' % comp_name,
                  sender=("WCA NotifyMe", os.environ.get('MAIL_USERNAME')),
                  recipients=recipients)
    msg.html = """Hello,<br><br>You've signed up to receive an email notification
                when registration for %s opens. You can register at
                <a href="%s">this link</a>.<br><br>

                Thank you for using WCA NotifyMe!<br><br>--<br>Brandon Lin
               """ % (comp_name, link)
    return msg


def send_msg(msg):
    mail.send(msg)
