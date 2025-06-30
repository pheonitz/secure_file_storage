import bcrypt

def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'pdf' , 'docx' , 'txt' , '.ppt'}
        return '.' in filename and filename.rsplit('.' ,1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(password : str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8') , salt)
    return hashed.decode('utf-8')

def verify_password(password : str , hashed : str):
    return bcrypt.checkpw(password.encode('utf-8') , hashed.encode('utf-8'))