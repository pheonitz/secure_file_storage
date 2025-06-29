import bcrypt

def hash_password(password : str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password , salt)
    return hashed.decode('utf-8')

def verify_password(password : str , hashed : str):
    return bcrypt.checkpw(password.encode('utf-8') , hashed.encode('utf-8'))