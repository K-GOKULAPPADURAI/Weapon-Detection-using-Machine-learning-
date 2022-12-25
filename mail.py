import smtplib,email 
from email.message import EmailMessage
msg = EmailMessage()
msg.set_content("ALERT!!! Weapon detected in the frame!")
with open("C:/Users/APPAtacker.py/Desktop/The Man From the Earth (2007) [1080p]/WWW.YIFY-TORRENTS.COM.jpg", "rb") as fp:
    msg.add_attachment(fp.read(), maintype="image", subtype="jpg")
    msg['subject'] = "Weapon detected!"

    msg['to'] = "rajskams@gmail.com"
    msg['to'] = "k.gokulappaduraikjgv@gmail.com"
    user = "minorproject002@gmail.com"
    msg['from'] = user
    password = "bflvgiwtazakvktc"
    server =smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
                    
