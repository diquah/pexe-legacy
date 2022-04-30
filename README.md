# pexe

![](https://img.shields.io/badge/license-GPLv3-blue) ![](https://img.shields.io/badge/python-3-blue)
 
Pexe is a way of packing a python project directory into a single file that feels like an executable (.exe) while still being python code.
 
Pexe is ***not*** for you if:
* You are trying to create a standalone executable.
* Pexe is not on your client machine.
* Python is not installed on your client machine.

### Usage:
In the command line:

`pexe.py <target> <args>`

---
**\<target>** - A file or a directory.

*In Build Mode:*

If a .py file is specified it will be the file run in run mode, i.e. your "main.py" file.  If a directory is specified it will automatically look for "main.py". If "main.py" is not found, the program will error.

*In Run Mode:*

A .pexe file.

---
**\<args>** - Arguments.
* `-b`: Build mode.
* `-i`: Specify files to include, or a regex match to include. By default, all files and folders in the directory are included besides .pexe files.


* `-r`: Run mode.

If both build and run modes are used, the target should be as specified for build mode.

If no modes are specified, run mode is default.