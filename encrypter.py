import os
import base64
import glob
import getpass

path = os.getcwd()


def encrypt(email: str = None, pwd: str = None, name: str = None, filename: bool = False):
    if filename:
        try:
            nameascii = name.encode("ascii")
            try:
                name64 = base64.b64encode(nameascii)
                return name64.decode('ascii')
            except UnicodeError:
                print("only ascii characters")
        except AttributeError:
            print("all of data need to be string")
    else:
        try:
            emailascii = email.encode("ascii")
            pwdascii = pwd.encode("ascii")
            nameascii = name.encode("ascii")
            try:
                email64 = base64.b64encode(emailascii)
                pwd64 = base64.b64encode(pwdascii)
                name64 = base64.b64encode(nameascii)
                return email64.decode('ascii'), pwd64.decode('ascii'), name64.decode('ascii')
            except UnicodeError:
                print("only ascii characters")
        except AttributeError:
            print("all of data need to be string")
        
    
def decrypt(encrypted: str, filename: bool = False):
    if filename:
        namebytes = base64.b64decode(encrypted)
        return namebytes.decode("ascii")
    else:
        try: 
            x = encrypted.split(":")
            emailencrypted = x[0]
            pwdencrypted = x[1]
            emailbytes = base64.b64decode(emailencrypted)
            pwdbytes = base64.b64decode(pwdencrypted)
            return emailbytes.decode("ascii"), pwdbytes.decode("ascii")
        except IndexError:
            print("put the password and the email not just one")
        
        
def savepwd(email: str, pwd: str, name: str) -> None:
    if os.path.isfile(os.path.join(path, f"{name}.txt")):
        print("password already saved")
    else:
        try:
            with open(f"{name}.txt", "w+") as f:
                f.writelines(f"{email}:{pwd}")
        except PermissionError:
            print("try to run this program as admin or move the program to other path")
            
            
def readpwd(name: str) -> None:
    try:
        with open(f"{name}.txt", "r") as f:
            pwd64 = f.readlines()
            print(decrypt(pwd64[0]))
    except FileNotFoundError:
        print("The password do not exist")
        
        
def deletepwd(name: str) -> None:
    try:
        os.remove(f"{name}.txt")
        print(f"You just delete {decrypt(name, filename=True)}")
    except FileNotFoundError:
        print("The password do not exist")
    
    
def listofpwd() -> list:
    pwdsaved = []
    listpwd = glob.glob("*.txt")
    for pwd in range(len(listpwd)):
        listpwd[pwd] = listpwd[pwd].replace(".txt", "")
    for pwdencrypted in range(len(listpwd)):
        pwdsaved.append(decrypt(listpwd[pwdencrypted], True))
    if len(pwdsaved) == 0:
        print("No passwords added try to add one")
    else:
        return pwdsaved
    
    
while True:
    print('''

    1. See the passwords saved.
    2. Read a password.
    3. Save a new password.
    4. Delete a password.
    5. Exit.

    ''')
    try:
        user = int(input("_: "))
        
        if user == 1:
            print(listofpwd())
        elif user == 2:
            pwdname = str(input("Enter the name of the password: "))
            readpwd(encrypt(name=pwdname, filename=True))
        elif user == 3:
            newemail = str(input("Put the email of the account: "))
            newpwd = getpass.getpass("Put the new password: ")
            namepwd = str(input("put the name of the password: "))
            if not newemail or not newpwd or not namepwd:
                print("all of the data new to be filled")
                print("password not added")
            else:
                newdata = encrypt(email=newemail, pwd=newpwd, name=namepwd)
                savepwd(newdata[0], newdata[1], newdata[2])
        elif user == 4:
            pwdel = str(input("Enter a password: "))
            deletepwd(encrypt(name=pwdel, filename=True))
        elif user == 5:
            break
        else:
            print("that is not a valid option")
    except ValueError:
        print("that is not a valid option")
    
    