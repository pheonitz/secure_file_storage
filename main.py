from app.utils import hash_password , verify_password

hashed = hash_password(b"mypassword")
print(hashed)
print("verfied : ", verify_password("mypassword" , hashed))
print("wrong : ", verify_password("wrongpass" , hashed))