# dtopr
A command line tool in python3 for maintaining Linux *.desktop files

Background
----------
In most of the major Linux variants, *.desktop files are used to tell the
system how to launch a given application, where in the Applications menu it should
be located, and what its name and icon should be in the menu.

dtopr
-----
The dtopr command line utility (short for "desktopper") makes it easier to create
a *.desktop file for a given application and (optionally) put it in the correct
Linux system directory for it to appear in the Applications menu.

The program works by repeatedly prompting the user for the main
*.desktop file entries that are required for the Applications menu to work. After
the user has entered the required information, dtopr creates the *.desktop
file and offers to move it to the system folder where it needs to go.
