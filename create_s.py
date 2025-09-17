from app import bcrypt
secret = bcrypt.generate_password_hash('24')

print(secret)