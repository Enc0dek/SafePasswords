# BY ENC0D3K
# e.b.e Encoded by Ecodek

import os
import base64
import getpass
from secrets import *
from dotenv import load_dotenv
from colorama import Fore, Style

RED = Fore.RED
GREEN = Fore.GREEN
YELLOW = Fore.YELLOW
PURPLE = Fore.MAGENTA
BLUE = Fore.BLUE
WHITE = Fore.WHITE

path = os.getcwd()


def encode_64(data: str) -> str:
    """
    Encode the given string into Base64 format.

    Args:
        data: The string to encode.

    Returns:
        The Base64 encoded string.

    Raises:
        UnicodeError: If the given string contains non-ASCII characters.
    """
    try:
        # Encode the string to ASCII format
        data_ascii = data.encode("ascii")
        # Encode the ASCII string to Base64 format
        data_64 = base64.b64encode(data_ascii)
        # Decode the Base64 encoded string to ASCII format and return it
        return data_64.decode("ascii")
    except UnicodeError:
        # Handle the error if the given string contains non-ASCII characters
        print("Only ASCII characters are allowed.")


def decode_64(data: str) -> str:
    """
    Decode the given Base64 encoded string into its original string.

    Args:
        data: The Base64 encoded string to decode.

    Returns:
        The original string.

    Raises:
        UnicodeError: If the given string contains non-ASCII characters.
    """
    try:
        # Decode the Base64 encoded string to bytes
        datadecoded = base64.b64decode(data)
        # Decode the bytes to ASCII string and return it
        return datadecoded.decode("ascii")
    except UnicodeError:
        # Handle the error if the given string contains non-ASCII characters
        print("Only ASCII characters are allowed.")
    
# Encryptation


def encrypt(email: str = None, pwd: str = None, name: str = None, filename: bool = False):
    """
    Encrypt the given data (email, password, and/or name) by encoding it into Base64 format.

    Args:
        email: The email address to encrypt.
        pwd: The password to encrypt.
        name: The name to encrypt.
        filename: A boolean flag to indicate whether to encrypt a filename instead of the email, password, and name.

    Returns:
        If filename is True, returns the Base64 encoded filename string. 
        Otherwise, returns a tuple of Base64 encoded email, password, and name strings.

    Raises:
        AttributeError: If the input data contains non-ASCII characters.
    """
    if filename:
        try:
            # Encode the filename to Base64 format and return it
            return encode_64(name)
        except AttributeError:
            # Handle the error if the input data contains non-ASCII characters
            print("All data needs to be string.")
    else:
        try:
            # Encode the email, password, and name to Base64 format and return them in a tuple
            return encode_64(email), encode_64(pwd), encode_64(name)
        except AttributeError:
            # Handle the error if the input data contains non-ASCII characters
            print("Only ASCII characters are allowed.")
        
    
def decrypt(data: str, filename: bool = False):
    """
    Decrypt the given Base64 encoded data (email and/or password) into their original strings.

    Args:
        data: The Base64 encoded email and/or password to decrypt.
        filename: A boolean flag to indicate whether to decrypt a filename instead of the email and password.

    Returns:
        If filename is True, returns the original filename string. 
        Otherwise, returns a tuple of original email and password strings.

    Raises:
        IndexError: If the input data does not contain both email and password.
    """
    if filename:
        # Decode the Base64 encoded filename and return the original filename string
        return decode_64(data)
    else:
        try: 
            # Split the Base64 encoded email and password by the colon delimiter and decode them
            email, pwd = data.split(":")
            return decode_64(email), decode_64(pwd)
        except IndexError:
            # Handle the error if the input data does not contain both email and password
            print("Please provide both the email and password.") 
        
        
def savepwd(email: str, pwd: str, name: str) -> None:
    # Check if a file with the given name already exists
    if os.path.isfile(os.path.join(path, f"{name}.txt")):
        print("password already saved")
    else:
        try:
            # Open the file with the given name in write mode and write the encrypted email and pwd to it
            with open(f"{name}.ebe", "w+") as f:
                f.writelines(f"{email}:{pwd}")
        except PermissionError:
            # If the program doesn't have the permission to write to the file, print an error message
            print("try to run this program as admin or move the program to other path")
            
            
def readpwd(name: str) -> None:
    try:
        # Try to open the file {name}.ebe in read mode
        with open(f"{name}.ebe", "r") as f:
            # Read the first line of the file and store it in pwdencrypted
            pwdencrypted = f.readlines()
            # Decrypt the password stored in pwdencrypted[0] using the decrypt() function
            print(decrypt(pwdencrypted[0]))
    except FileNotFoundError:
        # If the file is not found, print an error message
        print("The password does not exist")
        
        
def deletepwd(name: str) -> None:
    try:
        # Try to delete the file {name}.ebe using os.remove()
        os.remove(f"{name}.ebe")
        # If the file is successfully deleted, print a message indicating the file has been deleted
        # and the decrypted name of the file that was deleted
        print(f"You just deleted {decrypt(name, filename=True)}")
    except FileNotFoundError:
        # If the file is not found, print an error message
        print("The password does not exist")
    
   
# Read the file list and see if is a password
def listofpwd() -> list:
    # Create an empty list called pwdsaved to store the decrypted password names
    pwdsaved = []
    # Iterate over all the entries in the current working directory using os.scandir()
    for entry in os.scandir('.'):
        # Check whether the entry is a file and whether its name ends with .ebe
        if entry.is_file() and entry.name.endswith('.ebe'):
            # Extract the name of the file without the extension using os.path.splitext()
            name = os.path.splitext(entry.name)[0]
            # Call the decrypt() function, passing the name argument and setting the filename parameter to True
            # to decrypt the name of the file and append it to the pwdsaved list
            pwdsaved.append(decrypt(name, True))
    # If no decrypted password names are added to pwdsaved, print an error message
    if not pwdsaved:
        print("No passwords added. Try to add one.")
    # If at least one decrypted password name is added to pwdsaved, return the list of decrypted password names
    else:
        return pwdsaved
    

def configfile() -> str:
    # Read File
    if os.path.exists(".env"):
        load_dotenv()
        return os.getenv("PASSWORD")
    # Make File
    else:
        with open(".env", "w") as f:
            f.write(f"PASSWORD='{encode_64(getpass.getpass('Password: '))}'")
          
          
def main() -> None:
    os.system("cls")
    while True:
        print(PURPLE + "    1. See the passwords saved.", end="\n")
        print(BLUE + "    2. Read a password.", end="\n")
        print(GREEN + "    3. Save a new password.", end="\n")
        print(RED + "    4. Delete a password.", end="\n")
        print(YELLOW + "    5. Exit.", end="")
        print(WHITE + "\n")
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
            
            
try:
    if compare_digest(decode_64(configfile()), getpass.getpass("Password: ")):
        main()
    else:
        print("Incorrect password")
except:
    configfile()
