# ScriptEx
A commandline Python2 script to run a set of python scripts

ScriptEx is designed to execute python files and log the output to a file. It accepts single python files, zip files, or directory paths as commandline parameters. It uses JSON config files to store a series of configurations to run the files with. This includes interactive inputs as well as commandline arguments. 

It's provided as is. Only tested on Windows. I wrote this to run a batch of student homework assignments at once rather than having to manually test each one.

Basic usage: python ScriptEx.py \<Directory/Zip/File> \<Configuration File> \<Output File>

Optional Arguments: --file, --dir, --zip. These are used to specify the input type.
