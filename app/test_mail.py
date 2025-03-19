import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)  # ✅ Enable Debugging
    server.starttls()
    server.login('rthakurinfo4@.com', 'grig irqy fdob maug')
    server.quit()
    print("SMTP Connection Successful!")
except smtplib.SMTPAuthenticationError:
    print("SMTP Authentication Error: Check your EMAIL & PASSWORD!")
except smtplib.SMTPException as e:
    print(f"SMTP Exception: {e}")
