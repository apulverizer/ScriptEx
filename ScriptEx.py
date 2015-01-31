"""
SciptEx.py

This is a command line script which allows someone to run a list of python
scripts. It's main purpose is for running student submitted scripts all
at once with the same arguments. It uses JSON config file(s) to store the
interactive and commandline arguments which the scripts need to be tested
with.It logs the output of the scripts to a specified file.

Usage: python ScriptEx <Zip file of scripts> <Configuration file> <Output file> 
Optional Args: --file, --dir, --zip
"""

import os
import sys
import subprocess
import json
import zipfile
import time
import argparse

def readConfig(file):
	"""
	Read the specified configuration file and parse out the arguments.
	Returns a list of string arguments to pass as STDIN and a list of list
	of arguments
	"""
	jsonData = open(file) # open jsonFile
	data = json.load(jsonData) # load json data
	interactiveArgs = [] # 2D list of list of arguments for each configuration
	commandlineArgs = [] # 2D list of commandline arguments
	for config in data['configs']:
		intArgList = [] # arg list
		clArgList = [] # CL arg list
		for arg in config["Interactive"]:
			intArgList.append(str(arg))
		for arg in config["Commandline"]:
			clArgList.append(str(arg))
		interactiveArgs.append(intArgList)
		commandlineArgs.append(clArgList)
	return interactiveArgs, commandlineArgs
	
def processFile(filename,interactiveArgs,commandlineArgs,outputfile):
	"""
	Attempts to run the given python file with the given arguments
	Outputs to the specified file.
	"""
	with open(outputfile, 'a') as outfile: # open logfile
		# write newline and file name
		outfile.write(filename+'\n')
		outfile.write("--------------------------------------------------------------------------------\n")
		outfile.flush()
		# iterate over arguments
		for i in range(0, len(interactiveArgs)):
			# write list of arguments used
			outfile.write("Interactive Arguments: "+str(interactiveArgs[i])+'\n')
			outfile.write("Commandline Arguments: "+str(commandlineArgs[i])+'\n')
			outfile.flush()
			# Call python script and pipe output to the file
			p = subprocess.Popen([sys.executable, filename, ' '.join(str(i) for i in commandlineArgs[i])], stdin=subprocess.PIPE, stdout=outfile, stderr=outfile)
			p.communicate(input = '\n'.join(str(i) for i in interactiveArgs[i])+'\n')
			p.wait()				
			outfile.write("--------------------------------------------------------------------------------\n")
			outfile.flush()
		# write new lines		
		outfile.write("\n\n\n")
		outfile.flush()

def main(argv):
	"""
	Runs all of the files in a directory. Uses different config files to pass 
	in various STDIN inputs. Outputs results to a logfile.
	"""
	# set up argument parsing
	parser = argparse.ArgumentParser()
	parser.add_argument("path", help="Path to file(s)")
	parser.add_argument("config", help="Path to configuration file")
	parser.add_argument("output", help="Path to new output file")
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--zip", "--z", action="store_true")
	group.add_argument("--dir", "--d", action="store_true")
	group.add_argument("--file","--f", action="store_true")
	args = parser.parse_args()
	
	# Get command line arguments
	interactiveArgs,commandlineArgs = readConfig(args.config)
	
	# If zip file, unzip to new directory and process all files in directory
	if args.zip:
		print "Unzipping and running scripts. Please wait..."
		path = os.path.dirname(os.path.realpath(args.path))+"\\Extracted"+time.strftime("%d%m%Y%H%M%S")
		with zipfile.ZipFile(args.path, "r") as z:
			z.extractall(path)
		for filename in os.listdir(path):
			print "Running {}...".format(os.path.realpath(filename))
			processFile(os.path.join(path,filename),interactiveArgs,commandlineArgs,args.output)
	# if directory, process all files in it
	elif args.dir:
		print "Running scripts. Please wait..."
		for filename in os.listdir(args.path):
			print "Running {}...".format(os.path.realpath(filename))
			processFile(os.path.join(args.path,filename),interactiveArgs,commandlineArgs,args.output)
	# if just a single file, process that file
	elif args.file:
		print "Running {}.\nPlease wait...".format(os.path.realpath(args.path))
		processFile(os.path.realpath(args.path),interactiveArgs,commandlineArgs,args.output)
	# default to zip
	else:
		print "Unzipping and running scripts. Please wait..."
		path = os.path.dirname(os.path.realpath(args.path))+"\\Extracted"+time.strftime("%d%m%Y%H%M%S")
		with zipfile.ZipFile(args.path, "r") as z:
			z.extractall(path)
		for filename in os.listdir(path):
			print "Running {}...".format(os.path.realpath(args.path))
			processFile(os.path.join(path,filename),interactiveArgs,commandlineArgs,args.output)
			
	print "Completed!"
if __name__ == "__main__":
	main(sys.argv)
