import json
import os
from getpass import getpass
import time

from aes_cipher import decrypt_passwords, encrypt_passwords


def get_master_password(fn):
    try_number = 0
    good_pwd = False
    while try_number < 3 and not good_pwd:  # Only 3 attempts before quitting Pasword Manager
        master_password = getpass(f"Number of attempts left: {3 - try_number}/3\nPlease enter your master password: ")
        try:
            decrypt_passwords(master_password, fn)
            return master_password
        except:
            print("Wrong password")
            try_number += 1
            time.sleep(0.5)  # slow down brute force attack
    quit()


def create_password_file(fn):
    if os.path.isfile(fn):
        c = input(f"{fn} already exist, do you want to overwrite it ? (Y/N)").upper()
        if c == "Y":
            m_pwd = getpass("Choose your master password :")
            encrypt_passwords({}, m_pwd, fn)
            print(f"{fn} overwritten !")
        else:
            quit()
    else:
        m_pwd = getpass("Choose your master password :")
        encrypt_passwords({}, m_pwd, fn)
        print(f"{fn} created !")


def add_password(m_pwd, fn):
    url = input("url: ")
    identifier = input("id: ")
    pwd = getpass("password: ")
    pwds = decrypt_passwords(m_pwd, fn)
    number_of_password = len(pwds)
    pwds[number_of_password] = {"url": url,
                                "id": identifier,
                                "password": pwd}
    encrypt_passwords(pwds, m_pwd, fn)
    print(f"Password for {url} added !")


def show_password(m_pwd, fn, url):
    pwds = decrypt_passwords(m_pwd, fn)
    for i in range(len(pwds)):
        if pwds[str(i)]["url"] == url:
            print()
            print(pwds[str(i)], end="\n\n")


def show_passwords(m_pwd, fn):
    pwds = decrypt_passwords(m_pwd, fn)
    print()
    [print(p) for p in pwds.values()]
    print()


def menu():
    choice = ""
    password_file = None
    os.system("clear")
    print("Welcome to Passord Manage, ", end='')
    while not choice == "4":  # Infinite menu to stay in Pasword Manager
        print("please select an option:\n"
              "0. Create a new file\n"
              "1. Add a password to the file\n"
              "2. Show passwords for a url\n"
              "3. Show all passwords\n"
              "4. Quit Password Manager")
        choice = input()
        os.system("clear")

        if choice in ["0", "1", "2", "3"]:  # if choice is a valid choice
            if not password_file:  # for the first time in the loop, we ask the user to enter the password file
                password_file = input("Please enter your password file name: ")

        if choice == "0":
            create_password_file(password_file)
        elif choice == "1":
            master_password = get_master_password(password_file)
            add_password(master_password, password_file)
        elif choice == "2":
            master_password = get_master_password(password_file)
            url_to_show = input("enter the url that you want to display: ")
            show_password(master_password, password_file, url_to_show)
        elif choice == "3":
            master_password = get_master_password(password_file)
            show_passwords(master_password, password_file)


if __name__ == "__main__":
    menu()
