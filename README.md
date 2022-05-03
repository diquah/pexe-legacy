# pexe

![](https://img.shields.io/badge/license-GPLv3-blue) ![](https://img.shields.io/badge/python-3-blue)
 
Pexe is a way of packing a python project directory into a single file that feels like an executable (.exe) while still being python code.
 
Pexe is ***not*** for you if:
* You are trying to create a standalone executable.
* Pexe is not on your client machine.
* Python is not installed on your client machine.

---
### Usage:
In the command line:

`pexe.py <target> <args>`

**\<target>** - A file or a directory.

*In Build Mode:*

If a .py file is specified it will be the file run in run mode, i.e. your "main.py" file.  If a directory is specified it will automatically look for "main.py". If "main.py" is not found, the program will error.

*In Run Mode:*

A .pexe file.

**\<args>** - Arguments.
* `-b` `--build`: Build mode.
* `-i` `--include`: Specify files or regex include in executable. By default, all files and folders in the directory are included besides .pexe files and the bin folder.
* `-l` `--lib`: Specify files or regex to put in a linked library instead of the executable. Create multiple linked libraries by using the argument again: `-l a.py -l b.py c.py`


* `-r` `--run`: Run mode.
* `-a` `--args`: Specify list of arguments to pass to .pexe: `pexe.py applicaton.pexe -r -a <arguments>`

If both build and run modes are used, the target should be as specified for build mode.

If no modes are specified, run mode is default.

---
### A bit on .pll files:

What's up with the `--lib` command, and the .pll files it generates?

Pll files are like .pexe files with one major exception: they do not have a 'main.py' and are not executed when the program is unpacked. Instead, they act more as resources for your code to use.

Take this example: Your application has a collection of JSON, YAML, or other data files. To update these datasets, you shouldn't need to rebuild the application. Instead, put those files into a .pll and only update the .pll as required.

Think of this like replacing the GPU in your computer. Why buy a whole new computer with pre-installed GPU when you could just pull out the old GPU and slide in the new one?

Anything you can pack into a .pexe can also be packed into a .pll, including code.