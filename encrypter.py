import os
import base64
import getpass

path = os.getcwd()


def encode_64(data: str) -> str:
    try:
        dataascii = data.encode("ascii")
        data_64 = base64.b64encode(dataascii)
        return data_64.decode("ascii")
    except UnicodeError:
        print("only ascii characters")
        

def decode_64(data: str) -> str:
    try:
        datadecoded = base64.b64decode(data)
        return datadecoded.decode("ascii")
    except UnicodeError:
        print("only ascii characters are allowed")
    
    
def encrypt(email: str = None, pwd: str = None, name: str = None, filename: bool = False):
    if filename:
        try:
            return encode_64(name)
        except AttributeError:
            print("all of data need to be string")
    else:
        try:
            return encode_64(email), encode_64(pwd), encode_64(name)
        except AttributeError:
            print("only ascii characters")
        
    
def decrypt(data: str, filename: bool = False):
    if filename:
        return decode_64(data)
    else:
        try: 
            email, pwd = data.split(":")
            return decode_64(email), decode_64(pwd)
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
    for entry in os.scandir('.'):
        if entry.is_file() and entry.name.endswith('.txt'):
            name = os.path.splitext(entry.name)[0]
            pwdsaved.append(decrypt(name, True))
    if not pwdsaved:
        print("No passwords added try to add one")
    else:
        return pwdsaved
    
    
def main() -> None:
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
            
            
main()
