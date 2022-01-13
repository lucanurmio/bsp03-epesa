import smtplib
import poplib
from tkinter import *
from email.message import EmailMessage
from email.parser import BytesParser
from email.generator import DecodedGenerator
from email import policy
from smail import encrypt_message
from M2Crypto import BIO, SMIME, X509

def send_message():

    msg = EmailMessage()

    address_info = address.get()

    cert = cert_filename.get()

    msg['To'] = address_info

    msg['From'] = user.get()

    email_body_info = emailBodyTextbox.get("1.0", 'end-1c')

    msg.set_content(email_body_info)

    encrypted_email = encrypt_message(msg, [cert])

    server = smtplib.SMTP('smtp.lmail.test',25)

    server.send_message(encrypted_email)

def fetch_messages():

    mailbox = poplib.POP3('pop3.lmail.test',110)

    s = SMIME.SMIME()

    keypair = mykey_filename.get()

    cert = mycert_filename.get()

    s.load_key(keypair, cert)

    try:

        mailbox.user(user.get())

        mailbox.pass_(password.get())

    except:

        receivedMessageTextbox.delete("1.0", END)
        receivedMessageTextbox.insert(END, "Authentication failed")

    open("localMailbox.mbox", "w").close()

    mbox = open("localMailbox.mbox", "a")

    g = DecodedGenerator(mbox)

    numMessages = len(mailbox.list()[1])

    for i in range(numMessages):

        msg = BytesParser().parsebytes(b'\n'.join(j for j in mailbox.retr(i+1)[1]))

        g.flatten(msg)

    with open("encrypt.p7", "w") as o:

        o.write(msg.as_string())

        o.close()

    p7, data = SMIME.smime_load_pkcs7('encrypt.p7')

    out = s.decrypt(p7)

    print(out)

    outstring = out.decode("utf-8")

    print(outstring)

    receivedMessageTextbox.delete("1.0", END)

    receivedMessageTextbox.insert(END, "From: " + msg['from'] + "\n" + "To: " + msg['to'] + "\n\n" + outstring)

app = Tk()

app.geometry("600x600")

app.title("Python Mail Send App")

heading = Label(text="Python Email Sending App",bg="yellow",fg="black",font="10",width="500",height="3")

heading.pack()

address_field = Label(text="Recipient Address :")
email_body_field = Label(text="Message :")
user_field = Label(text="Your email account :")
password_field = Label(text="Your password :")
cert_field = Label(text="Recipient's certificate filename:")
mycert_field = Label(text="Your certificate filename:")
mykey_field = Label(text="Your keypair filename:")

address_field.place(x=15,y=70)
email_body_field.place(x=15,y=140)
user_field.place(x=300,y=70)
password_field.place(x=300,y=140)
cert_field.place(x=300,y=220)
mycert_field.place(x=300,y=280)
mykey_field.place(x=300,y=340)

address = StringVar()
user = StringVar()
password = StringVar()
cert_filename = StringVar()
mycert_filename = StringVar()
mykey_filename = StringVar()

address_entry = Entry(textvariable=address,width="30")
user_entry = Entry(textvariable=user,width="30")
password_entry = Entry(textvariable=password,width="30")
cert_filename_entry = Entry(textvariable=cert_filename,width="30")
mycert_filename_entry = Entry(textvariable=mycert_filename,width="30")
mykey_filename_entry = Entry(textvariable=mykey_filename,width="30")

address_entry.place(x=15,y=100)
user_entry.place(x=300,y=100)
password_entry.place(x=300,y=180)
cert_filename_entry.place(x=300,y=250)
mycert_filename_entry.place(x=300,y=310)
mykey_filename_entry.place(x=300,y=370)

buttonSend = Button(app,text="Send Message",command=send_message,width="30",height="2",bg="grey")

buttonFetch = Button(app,text="Show latest message",command=fetch_messages,width="30",height="2",bg="grey")

buttonSend.place(x=15,y=220)

buttonFetch.place(x=15,y=280)

emailBodyTextbox = Text(app, height=2, width=30)

emailBodyTextbox.place(x=15,y=180)

receivedMessageTextbox = Text(app, height=10, width=64)

receivedMessageTextbox.place(x=15,y=400)

mainloop()