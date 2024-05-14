import hashlib
import os
import secrets
import base64
import smtplib
 
password_length = 12  # Change this to your desired password length
iterations = 600000  # Change this to your desired number of iterations
sender_email = 'your_email@example.com'  # Update with your email address
sender_password = 'your_email_password'  # Update with your email password

salt = secrets.token_bytes(16)
password = secrets.token_urlsafe(password_length)

hashed_password = hashlib.pbkdf2_hmac(
    'sha256',  # Hashing algorithm
    password.encode('utf-8'),  # Password to hash
    salt,  # Salt
    iterations  # Number of iterations
)

hashed_password = base64.b64encode(hashed_password).decode('utf-8')
salt = base64.b64encode(salt).decode('utf-8')

final_password = f"pbkdf2_sha256${iterations}${salt}${hashed_password}"

# Send the password to the user's email
# receiver_email = 'user_email@example.com'  # Update with the user's email address

# message = f"Subject: Your Password\n\nYour password is: {password}"

# Create a secure SSL connection to the mail server
# with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, receiver_email, message)

print("Password sent to user's email.")
print("Hashed password:", final_password)
