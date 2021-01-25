import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename


class sender:
    # email: inibir.test.123@gmail.com
    # password: cuentatest123
    # need to set account less security in this link
    # https://myaccount.google.com/lesssecureapps
    EMAIL_SERVER = 'smtp.gmail.com'

    def __init__(self, email, pasw):
        self.email = email
        self.pasw = pasw
        self.files = []

    def attach_file(self, file):
        name = basename(file)
        with open(file, "rb") as fil:
            data = fil.read()
        self.files.append({'name': name, 'content': data})

    def attach_content(self, name, content):
        self.files.append({'name': name, 'content': content})

    def send(self, to, subject, text):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = to  # msg['To'] = ', '.join(self.EMAIL_TO)
        msg.attach(MIMEText(text))

        for file in self.files:
            part = MIMEApplication(file.get("content"), Name=file.get("name"),)
            part['Content-Disposition'] = f'attachment; filename="{file.get("name")}"'
            msg.attach(part)

        smtp = smtplib.SMTP_SSL(self.EMAIL_SERVER, 465)
        smtp.login(self.email, self.pasw)
        smtp.sendmail(self.email, to, msg.as_string())
        smtp.close()
