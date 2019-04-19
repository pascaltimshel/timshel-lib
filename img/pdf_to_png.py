#!/usr/bin/env python3

# Author: Pascal N. Timshel
# Date: April 2019

import sys
import os
import glob
import argparse
import subprocess
import math

###################################### Usage ######################################

# python3 --dir "/Users/djw472/Google Drive/Pers Lab/Projects/BMI-Brain/Manuscript/PUBLICATION-FIGS" --recursive

###################################### DOCS/REFS ######################################

# OSX pdf to png conversion: https://stackoverflow.com/a/6350037/6639640
# Sips docs: https://ss64.com/osx/sips.html

###################################### FUNCTIONS ######################################

def query_yes_no(question, default="no"):
	# REF: https://stackoverflow.com/a/3041990/6639640
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower() # python3
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def job_scheduler(list_cmds, n_parallel_jobs):
	""" 
	Schedule parallel jobs with at most n_parallel_jobs parallel jobs.
	"""
	N_TOTAL_JOBS = len(list_cmds)
	N_TOTAL_BATCHES = math.ceil(N_TOTAL_JOBS/n_parallel_jobs) # round up
	list_of_processes = []
	batch = 1
	for i, cmd in enumerate(list_cmds, start=1):
		print("job schedule batch = {}/{} | i = {}/{} | Running command: {}".format(batch, N_TOTAL_BATCHES, i, N_TOTAL_JOBS, cmd))
		
		### Output
		# p = subprocess.Popen(cmd, shell=True)
		# p = subprocess.Popen(cmd, shell=True, bufsize=0) # unbuffered
		### No output
		### You need to keep devnull open for the entire life of the Popen object, not just its construction. 
		FNULL = open(os.devnull, 'w') # devnull filehandle does not need to be closed?
		p = subprocess.Popen(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
		
		list_of_processes.append(p)
		print("job schedule batch = {}/{} | i = {}/{} | PIDs of running jobs (list_of_processes):".format(batch, N_TOTAL_BATCHES, i, N_TOTAL_JOBS))
		print(" ".join([str(p.pid) for p in list_of_processes])) # print PIDs
		if i % n_parallel_jobs == 0: # JOB BATCH SIZE
			batch += 1
			for p in list_of_processes:
				print("=========== Waiting for process: {} ===========".format(p.pid))
				sys.stdout.flush()
				p.wait()
				print("Returncode = {}".format(p.returncode))
			list_of_processes = [] # 'reset' list

	### wait for the rest for the rest of the processes
	for p in list_of_processes:
		print("=========== Waiting for process: {} ===========".format(p.pid))
		p.wait()

	return list_of_processes

###################################### ARGS ######################################

arg_parser = argparse.ArgumentParser(description="Convert PDF files to PNG using OSX build-in command line tool 'Scriptable image processing system' (sips). Script will convert all *.pdf/*.PDF in --dir to .png")
arg_parser.add_argument("--dir", help="Directory to look for .pdf/.PDF to convert to png")
arg_parser.add_argument("--dpi", type=float, help="DPI of output PNG", default=300)
arg_parser.add_argument("--recursive", help="If set, then traverse directory resursively to convert pdfs in subfolders.", action='store_true')
arg_parser.add_argument("--n_parallel_jobs", type=int, help="Number of parallel conversion jobs to run.", default=10)
args = arg_parser.parse_args()

###################################### CONSTANTS ######################################

file_extensions = [".pdf", ".PDF"]

###################################### MAIN ######################################

### Get files
list_pdf_files = [] # this list will contain full pathnames for pdfs to convert
for file_extension in file_extensions:
	pattern_glob = "{dir}{recursive}/*{ext}".format(dir=args.dir, 
													recursive="/**" if args.recursive else "", 
													ext=file_extension)
	tmp_glob = glob.glob(pattern_glob, recursive=args.recursive) # REF: https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
	list_pdf_files.extend(tmp_glob)


### Ask user for consent
n_files = len(list_pdf_files)
if n_files==0:
	print("Did not find any files in dir={} matching [{}]".format(args.dir, ",".join(file_extensions)))
	sys.exit(0)
else:
	print("Found n={} files in dir (recursive={}):".format(n_files, args.recursive))
	for filepath in list_pdf_files:
		print(filepath)
	print("Ready to convert files. NB: existing .png files will be overwritten.")
	flag_bool_user_accept = query_yes_no("Do you want to convert these files (yes/no)?") # return True/False
	if not flag_bool_user_accept:
		print("No files converted. Quitting gracefully...")
		sys.exit(0)

### Subprocess
list_cmds = []
for filepath in list_pdf_files:
	file_no_ext, file_ext = os.path.splitext(filepath)
	cmd = "sips -s format png -s dpiWidth {dpi} -s dpiHeight {dpi} '{f}.pdf' --out '{f}.png'".format(dpi=args.dpi, f=file_no_ext)
	# ^ *OBS IMPORTANT*: input and output files must be quoted ('{f}.pdf') to allow for spaces in filepath.
	# p = subprocess.Popen(cmd, shell=True)
	list_cmds.append(cmd)

### Call scheduler
job_scheduler(list_cmds=list_cmds, n_parallel_jobs=args.n_parallel_jobs)

print("Script is done!")
	

