import os

def get_category_selections():
    categories = ["<End Selection>", "AudioVideo", "Development", "Education", "Game", "Graphics",
                    "Network", "Office", "Science", "Settings", "System", "Utility"]
    selecteds = []
    while True:
        # prompt for input
        print("Select one or more categories.  Select 0 when done.")
        for i, category in enumerate(categories):
            asterisk = ""
            if i in selecteds:
                asterisk = "* "
            print(f"\t({i}) {asterisk}{category}")

        # sanity checks on the input
        try:
            curr_choice = int(input())
        except ValueError:
            curr_choice = -1
        if curr_choice < 0 or curr_choice > len(categories)-1:
            print("You did not select an item in the list.")
            continue

        # quit the loop and return the category string if user entered 0
        if curr_choice == 0:
            retval = ""
            for i in selecteds:
                retval += categories[i] + ";"
            return retval

        # handle selection or de-selection of the item entered
        un = ""
        if curr_choice in selecteds:
            un = "un-"
            selecteds.remove(curr_choice)
        else:
            selecteds.append(curr_choice)

        print(f"You {un}selected '({curr_choice}) {categories[curr_choice]}'")

def main():
    print("Creating a new *.desktop file!")
    fname = input("Enter the file name (just the part before .desktop): ")
    fname += ".desktop"
    # try to create the file ... for now, exist if it exists
    try:
        f = open(fname, 'x')
    except FileExistsError:
        print("A file with that name already exists.  Exitting.")
        exit()
    except:
        print("Error creating file.  Exitting.")
        exit()

    appname = "Name=" + input("Enter the name of the app as you'd like it to appear in the menus: ")
    exec = "Exec=" + input("Enter the app's commandline command, including path and arguments: ")
    path = "Path=" + input("Enter the working directory of the app: ")
    icon = "Icon=" + input("Enter the full path of the app's icon: ")
    catstring = "Categories=" + get_category_selections()

    # write to the file
    f.write("[Desktop Entry]\n")
    f.write("Encoding=UTF-8\n")
    f.write("Version=1.0\n")
    f.write("Type=Application\n")
    f.write("Terminal=false\n")
    f.write(appname + "\n")
    f.write(exec + "\n")
    f.write(path + "\n")
    f.write(icon + "\n")
    f.write(catstring + "\n")
    f.close()

    # offer to move the file to the proper linux system folder
    system_path = "/usr/share/applications/"
    confirm_move =input("Would you like to move the file to the system directory? ")
    if confirm_move.upper() in ("Y", "YES"):
        print("Moving the file...")
        os.system(f"mv -i --backup=numbered {fname} {system_path}{fname}")


if __name__ == '__main__':
    main()
