#!/usr/bin/python3

# -------------------------------------------------------------------------------
# dtopr.py
# program to install an application desktop file so that it appears in the menus
# -------------------------------------------------------------------------------

import os
import readline
import signal
import sys

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
    bools = {"Y": "true", "YES": "true", "N": "false", "NO": "false"}
    while True:
        response = dtopr_input(prompt).upper()
        if response in bools.keys():
            return bools[response]

def get_categories(prompt=""):
    categories = ["AudioVideo", "Development", "Education", 
                "Game", "Graphics", "Network", "Office", 
                "Science", "Settings", "System", "Utility"]
    return get_multi_selection(prompt, categories)

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
            print(f"\t({i+1}) {asterisk}{item}")

        # get the user's selection - note that the selection is 1 to n
        # but the list is indexed 0 to n-1
        curr_choice = get_choice_int()

        # sanity checks on the input
        if curr_choice < 0 or curr_choice > len(choicelist):
            continue

        # quit the loop and return the category string if user entered 0
        if curr_choice == 0:
            retval = ""
            for i in selecteds:
                retval += choicelist[i] + ";"
            return retval

        # handle selection or de-selection of the item entered
        if (curr_choice-1) in selecteds:
            selecteds.remove(curr_choice-1)
        else:
            selecteds.append(curr_choice-1)

def get_choice_int():
        try:
            return int(input())
        except ValueError:
            return -1


class DesktopFileData:
    def __init__(self):
        self.input_manager = InputManager()
        self.setup_prompts()
        self.header = (
            "[Desktop Entry]\n"
            "Encoding=UTF-8\n"
            "Version=1.0\n"
            "Type=Application\n")

    def get_values(self, name="ALL"):
        self.input_manager.get_input(name)

    def review_prompt(self):
        print("Here are the desktop file entries you've created so far:")
        print()

        for i, name in enumerate(self.input_manager.names):
            str = self.input_manager.get_nameval_string(name)
            print(f"\t({i+1}) {str}")
        print()
        print("Select a number to change.\n"
            "Select 0 to continue if you are happy with it the way it is.")

    def review(self):
        while True:
            make_title()
            self.review_prompt()
            choice = get_choice_int()

            # sanity check on input
            if choice < 0 or choice > len(self.input_manager.data):
                continue

            # perform selection
            if choice == 0:
                return
            else:
                name = self.input_manager.names[choice-1]
                self.get_values(name);

    def write(self, f):
        # write the data to the file f
        f.write(self.header)
        for name in self.input_manager.names:
            str = self.input_manager.get_nameval_string(name)
            f.write(f"{str}\n")

    def setup_prompts(self):
        self.input_manager.add("Name",       "Enter the name of the app as you'd like it to appear in the menus:\n", dtopr_input)
        self.input_manager.add("Comment",    "Enter a brief description of the app:\n", dtopr_input)
        self.input_manager.add("Exec",       "Enter the app's commandline command, including arguments:\n", get_path)
        self.input_manager.add("Path",       "Enter the working directory of the app (blank for current directory):\n", get_path)
        self.input_manager.add("Icon",       "Enter the filename of the app's icon:\n", get_path)
        self.input_manager.add("Terminal",   "Will this be a terminal app (y/n)?\n", get_bool)
        self.input_manager.add("Categories", "Select one or more categories.  Select 0 when done.", get_categories)


#################################################################
class InputData:
    def __init__(self, name, prompt, input_func):
        self.name = name
        self.prompt = prompt
        self.input_func = input_func
        self.value = ""

class InputManager:
    def __init__(self):
        # I'm keeping a dictionary of data, plus a parallel list of names,
        # that way I can look up a name by index number, and then look up
        # that name in the dictionary.  Seems messy.  Might not be the best way.
        self.data = {}
        self.names = []
    def add(self, name, prompt, input_func):
        newData = InputData(name, prompt, input_func)
        self.data[name] = newData
        self.names.append(name)
    def get_input(self, name):
        for elt in self.data.values():
            if elt.name == name or name =="ALL":
                value = elt.input_func(elt.prompt)
                self.data[elt.name].value = value
    def get_nameval_string(self, name):
        return f"{name}={self.data[name].value}"
#################################################################

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
