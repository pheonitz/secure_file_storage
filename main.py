from app.utils import hash_password , verify_password
from app.routes import app

hashed = hash_password("mypassword")
print(hashed)
print("verfied : ", verify_password("mypassword" , hashed))
print("wrong : ", verify_password("wrongpass" , hashed))

if __name__ == "__main__":
    app.run(debug=True)