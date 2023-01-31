#!/usr/bin/python3

# -------------------------------------------------------------------------------
# dtopr.py
# program to install an application desktop file so that it appears in the menus
# -------------------------------------------------------------------------------

import os
import readline
import signal
import sys


# constants
SECTIONS = [
    "header",
    "app_name",
    "app_comment",
    "app_exec",
    "app_path",
    "app_icon",
    "app_terminal",
    "app_categories"
]

categories = ["<End Selection>", "AudioVideo", "Development", "Education", 
                "Game", "Graphics", "Network", "Office", 
                "Science", "Settings", "System", "Utility"]

def handle_ctrl_c(signal_number, stack_frame):
    # Python note: I would like to offer the user a chance to cancel
    # the ctrl-c termination of the program, but issuing a call to input()
    # here causes the program to end ungracefully with a python callstack
    # dump.  So I'm just exitting.
    sys.exit(1)

def make_title():
    os.system("clear")
    print("***********************************************")
    print("  WELCOME TO DTOPR: APP INSTALLATION UTILITY!")
    print("***********************************************\n")

def dtopr_input(prompt="", errmsg=""):
    make_title()
    return input(prompt + errmsg)

def get_outfile(prompt):
    errmsg = ""
    while True:
        fname = dtopr_input(prompt, errmsg)
        fname += ".desktop"

        # handle existing file
        if os.path.exists(fname):
            yesno = input(f"A file named {fname} already exists. Overwrite (y/n)? ")
            if not yesno.upper() in ("Y", "YES"):
                continue

        # try to create the file
        try:
            f = open(fname, 'w')
        except:
            print(f"Error creating file {fname}.  Exitting.")
            exit()

        return (f, fname)

def get_path(prompt):
    errmsg = ""
    while True:
        retval = os.path.abspath((dtopr_input(prompt, errmsg)))
        if os.path.exists(retval.split()[0]):
            return retval
        else:
            errmsg = f"{retval} does not exist.\n"

def get_bool(prompt):
    values = {"Y": "true", "YES": "true", "N": "false", "NO": "false"}
    while True:
        response = dtopr_input(prompt).upper()
        if response in values.keys():
            return values[response]

def get_multi_selection(prompt="", choicelist=[]):
    selecteds = []
    while True:
        # prompt for input
        make_title()
        print(prompt)
        for i, item in enumerate(choicelist):
            asterisk = ""
            if i in selecteds:
                asterisk = "* "
            print(f"\t({i}) {asterisk}{item}")

        # sanity checks on the input
        curr_choice = get_choice_int()
        if curr_choice < 0 or curr_choice > len(choicelist)-1:
            continue

        # quit the loop and return the category string if user entered 0
        if curr_choice == 0:
            retval = ""
            for i in selecteds:
                retval += choicelist[i] + ";"
            return retval

        # handle selection or de-selection of the item entered
        if curr_choice in selecteds:
            selecteds.remove(curr_choice)
        else:
            selecteds.append(curr_choice)

def get_choice_int():
        try:
            return int(input())
        except ValueError:
            return -1


class DesktopFileData:
    def __init__(self):
        self.app_name = ""
        self.app_comment = ""
        self.app_exec = ""
        self.app_path = ""
        self.app_icon = ""
        self.app_terminal = ""
        self.app_categories = ""
        self.header = (
            "[Desktop Entry]\n"
            "Encoding=UTF-8\n"
            "Version=1.0\n"
            "Type=Application\n")

    def get_values(self, val_name="ALL"):
        if val_name == "ALL" or val_name == "app_name":
            self.app_name = "Name=" + dtopr_input("Enter the name of the app as you'd like it to appear in the menus:\n")
        if val_name == "ALL" or val_name == "app_comment":
            self.app_comment = "Comment=" + dtopr_input("Enter a brief description of the app:\n")
        if val_name == "ALL" or val_name == "app_exec":
            self.app_exec = "Exec=" + get_path("Enter the app's commandline command, including arguments:\n")
        if val_name == "ALL" or val_name == "app_path":
            self.app_path = "Path=" + get_path("Enter the working directory of the app (blank for current directory):\n")
        if val_name == "ALL" or val_name == "app_icon":
            self.app_icon = "Icon=" + get_path("Enter the filename of the app's icon:\n")
        if val_name == "ALL" or val_name == "app_terminal":
            self.app_terminal = "Terminal=" + get_bool("Will this be a terminal app (y/n)?\n")
        if val_name == "ALL" or val_name == "app_categories":
            self.app_categories = "Categories=" + get_multi_selection("Select one or more categories.  Select 0 when done.", categories)

    def values_prompt(self):
        print("Here are the desktop file entries you've created so far:")
        print()
        print("\t(1) " + self.app_name)
        print("\t(2) " + self.app_comment)
        print("\t(3) " + self.app_exec)
        print("\t(4) " + self.app_path)
        print("\t(5) " + self.app_icon)
        print("\t(6) " + self.app_terminal)
        print("\t(7) " + self.app_categories)
        print()
        print("Select a number to change.\n"
            "Select 0 to continue if you are happy with it the way it is.")

    def review(self):
        while True:
            make_title()
            self.values_prompt()
            choice = get_choice_int()

            # sanity check on input
            if choice < 0 or choice > 7:
                continue

            # perform selection
            if choice == 0:
                return
            else:
                self.get_values(SECTIONS[choice]);

    def write(self, f):
        # write the data to the file f
        f.write(self.header)
        f.write(self.app_terminal + "\n")
        f.write(self.app_name + "\n")
        f.write(self.app_comment + "\n")
        f.write(self.app_exec + "\n")
        f.write(self.app_path + "\n")
        f.write(self.app_icon + "\n")
        f.write(self.app_categories + "\n")



def main():
    signal.signal(signal.SIGINT, handle_ctrl_c)

    # Create the file and get all of the data from user input, allow user to
    # review their choices, then write everything to file.
    (f,fname) = get_outfile("Enter the desktop file name (just the part before .desktop):\n")
    data = DesktopFileData()
    data.get_values()
    data.review()
    data.write(f)
    f.close()

    # offer to move the file to the proper linux system folder
    system_path = "/usr/share/applications/"
    confirm_move =dtopr_input("Would you like to move the file to the system directory?\n")
    if confirm_move.upper() in ("Y", "YES"):
        print("Moving the file...\n")
        cmd = f"mv -i --backup=numbered {fname} {system_path}{fname}"
        print(f"  {cmd}\n")
        os.system(cmd)

if __name__ == '__main__':
    main()
