import os
import base64


path = os.getcwd()


def encrypt(email: str, pwd: str) -> tuple:
    try:
        emailascii = email.encode("ascii")
        pwdascii = pwd.encode("ascii")
        try:
            email64 = base64.b64encode(emailascii)
            pwd64 = base64.b64encode(pwdascii)
            return email64.decode('ascii'), pwd64.decode('ascii')
        except AttributeError:
            print("only ascii characters")
    except AttributeError:
        print("both data need to be string")
    
    
def savepwd(email: str, pwd: str, name: str) -> str:
    if os.path.isfile(os.path.join(path, f"{name}.txt")):
        print("password already saved")
    else:
        with open(f"{name}.txt", "w+") as f:
            f.writelines(f"{email}:{pwd}")
pwd = encrypt("papacaliete", "luis102030")
savepwd(pwd[0], pwd[1], "hola")