#!/usr/bin/env python2.7


import sys
import glob
import os

import datetime
import time
import argparse

sys.path.insert(1, '/home/unix/ptimshel/git/snpsnap') # do not use sys.path.insert(0, 'somepath')
import pplaunch
import pphelper
import pplogger

import re
import subprocess
import logging

import pdb


def submit():
	processes = []
	for i in xrange(1,22+1): # gives 1,2,..,21,22
		chr_no = str(i)
		file_in_impute = "/cvar/jhlab/TONU/LC_MS_EGCUT_GTypes/Prote_370K_chr{number}_imputation_1000G_02052012.impute.gz".format(number=chr_no)
		#logger.info( "RUNNING: file %s" % os.path.basename(file_in_impute) )


		file_out_exclude = '{base}/chr{no}_exclusion.list'.format(base=output_dir_base, no=chr_no)
		### example line: --- rs58108140 10583 G A 0.3340 0.5190 0.1470 ....
		cmd = """'zcat {file_in} | cut -d " " -f 2 | egrep "^(.*):[D,I]$" > {file_out}'""".format(file_in=file_in_impute, file_out=file_out_exclude)
		#cmd = """'/bin/bash zcat {file_in} | cut -d " " -f 2 | egrep "^(.*):[D,I]$" > {file_out}'""".format(file_in=file_in_impute, file_out=file_out_exclude)

		logger.info( "command to be run on cluster:\n%s" % cmd )
		
		jobname = "chr%s" % chr_no

		processes.append( pplaunch.LaunchBsub(cmd=cmd, queue_name=queue_name, mem=mem, jobname=jobname, projectname='epistasis', path_stdout=log_dir, file_output=None, no_output=False, email=email, email_status_notification=email_status_notification, email_report=email_report, logger=logger) ) #

	for p in processes:
		p.run()
		time.sleep(args.pause)
	### IMPORTANT!!! MODIFYING QUEUE!!!
	for p in processes:
		p.modify_queue("hour")
	return processes


def check_jobs(processes, logger):
	logger.info("PRINTING IDs")
	list_of_pids = []
	for p in processes:
		logger.info(p.id)
		list_of_pids.append(p.id)
	logger.info( " ".join(list_of_pids) )
	if args.multiprocess:
		logger.info( "Running report_status_multiprocess " )
		pplaunch.LaunchBsub.report_status_multiprocess(list_of_pids, logger) # MULTIPROCESS
	else:
		logger.info( "Running report_status" )
		pplaunch.LaunchBsub.report_status(list_of_pids, logger) # NO MULTIPROCESS




def ParseArguments():
	arg_parser = argparse.ArgumentParser(description="Python submission Wrapper")
	arg_parser.add_argument("--logger_lvl", help="Set level for logging", choices=['debug', 'info', 'warning', 'error'], default='info') # TODO: make the program read from STDIN via '-'
	arg_parser.add_argument("--multiprocess", help="Swtich; [default is false] if set use report_status_multiprocess. Requires interactive multiprocess session", action='store_true')
	#TODO: implement formatting option
	arg_parser.add_argument("--format", type=int, choices=[0, 1, 2, 3], help="Formatting option parsed to pplaunch", default=1)
	arg_parser.add_argument("--pause", type=int, help="Sleep time after run", default=1)
	
	args = arg_parser.parse_args()
	return args

def LogArguments():
	# PRINT RUNNING DESCRIPTION 
	now = datetime.datetime.now()
	logger.critical( '# ' + ' '.join(sys.argv) )
	logger.critical( '# ' + now.strftime("%a %b %d %Y %H:%M") )
	logger.critical( '# CWD: ' + os.getcwd() )
	logger.critical( '# COMMAND LINE PARAMETERS SET TO:' )
	for arg in dir(args):
		if arg[:1]!='_':
			logger.critical( '# \t' + "{:<30}".format(arg) + "{:<30}".format(getattr(args, arg)) ) ## LOGGING



###################################### Global params ######################################
queue_name = "bhour" # [bhour, bweek] priority
#queue_name = "priority" # [bhour, bweek] priority
# priority: This queue has a per-user limit of 10 running jobs, and a run time limit of three days.
mem="2" # gb 
email='pascal.timshel@gmail.com' # [use an email address 'pascal.timshel@gmail.com' or 'False'/'None']
email_status_notification=False # [True or False]
email_report=False # # [True or False]

current_script_name = os.path.basename(__file__).replace('.py','')

###################################### ARGUMENTS ######################################
args = ParseArguments()

###################################### SETUP logging ######################################
current_script_name = os.path.basename(__file__).replace('.py','')
log_dir =  "/cvar/jhlab/timshel/LC_MS_EGCUT_logs" #OBS VARIABLE
logger = pplogger.Logger(name=current_script_name, log_dir=log_dir, log_format=1, enabled=True).get()
def handleException(excType, excValue, traceback, logger=logger):
	logger.error("Logging an uncaught exception", exc_info=(excType, excValue, traceback))
#### TURN THIS ON OR OFF: must correspond to enabled='True'/'False'
sys.excepthook = handleException
logger.info( "INSTANTIATION NOTE: placeholder" )
###########################################################################################

############################# SWITCH ##########################################


##############################################################################

input_dir_base = "/cvar/jhlab/TONU/LC_MS_EGCUT_GTypes"
output_dir_base = "/cvar/jhlab/timshel/LC_MS_EGCUT_GTypes_clean"

if not os.path.exists(output_dir_base):
	logger.warning( "UPS: output path %s does not exist. Fix it! Exiting..." % output_dir_base )
	sys.exit(1)

if not os.path.exists(log_dir):
	logger.warning( "UPS: log dir %s does not exist. Fix it! Exiting..." % log_dir )
	sys.exit(1)



###################################### RUN FUNCTIONS ######################################
# NOW RUN FUNCTIONS
LogArguments()
processes = submit()

start_time_check_jobs = time.time()
check_jobs(processes, logger) # TODO: parse multiprocess argument?
elapsed_time = time.time() - start_time_check_jobs
logger.info( "Total Runtime for check_jobs: %s s (%s min)" % (elapsed_time, elapsed_time/60) )
logger.critical( "%s: finished" % current_script_name)








