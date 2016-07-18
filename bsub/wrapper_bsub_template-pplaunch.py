#!/usr/bin/env python2.7

import sys
import glob
import os

import datetime
import time
import argparse

import pplaunch
import pphelper
import pplogger

import re
import subprocess
import logging


import pdb

###################################### SYNOPSIS ######################################

# See also: wrapper_bsub_run_FastEpistasis_cache.py

####################################################################################

# def test():
# 	""" Test for loaded dependencies """
# 	try:
# 		FNULL = open(os.devnull, 'w')
# 		subprocess.Popen(["<PROGRAM OF INTEREST>"], stdout=FNULL, stderr=subprocess.STDOUT)
# 		FNULL.close()
# 	except Exception as e:
# 		raise Exception("Could not find <PROGRAM OF INTEREST> as executable on path. Please check that you have LOADED THE PROGRAM. Error msg: %s" % e)
# 	# reuse <PROGRAM OF INTEREST>



def submit():
	processes = []

	for var1 in var1_parameter_list:
		logger.info( "****** RUNNING: var1=%s *******" % var1 )
		for var2 in var2_paramter_list:
			logger.info( "****** RUNNING: var2=%s *******" % var2 )


				dir_out = "{base}/{var1}/{var2}".format(base=output_dir_base, var1=var1, var2=var2)
				if not os.path.exists(dir_out):
					os.makedirs(dir_out)
				out = XXX

				cmd = "python XXX.py --out {out} --var1 {var1} --var2 {var2}".format(out=out, var1=var1, var2=var2)
				logger.info( "making command:\n%s" % cmd )

				jobname = "XXXX".format(XXXX)

				processes.append( pplaunch.LaunchBsub(cmd=cmd, queue_name=queue_name, mem=mem, proc=proc, shared_mem=shared_mem, jobname=jobname, projectname='projectXXX', path_stdout=log_dir, file_output=file_job_bsub_out, no_output=False, email=email, email_status_notification=email_status_notification, email_report=email_report, logger=logger) ) #

	for p in processes:
		p.run()
		time.sleep(args.pause)
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
	arg_parser = argparse.ArgumentParser(description="Python submission wrapper")
	arg_parser.add_argument("--logger_lvl", help="Set level for logging", choices=['debug', 'info', 'warning', 'error'], default='info') # TODO: make the program read from STDIN via '-'
	arg_parser.add_argument("--multiprocess", help="Swtich; [default is false] if set use report_status_multiprocess. Requires interactive multiprocess session", action='store_true')
	#TODO: implement formatting option
	arg_parser.add_argument("--format", type=int, choices=[0, 1, 2, 3], help="Formatting option parsed to pplaunch", default=1)
	arg_parser.add_argument("--pause", type=int, help="Sleep time after run", default=0.5)
	
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
queue_name = "hour" # [bhour, bweek] priority
	# priority: This queue has a per-user limit of 10 running jobs, and a run time limit of three days.
mem=20 # GB
email='pascal.timshel@gmail.com' # [use an email address 'pascal.timshel@gmail.com' or 'False'/'None']
email_status_notification=False # [True or False]
email_report=False # # [True or False]

script2call = "/cvar/jhlab/XXXX.py"


###################################### ARGUMENTS ######################################
args = ParseArguments()

###################################### CONSTANTS ######################################
batch_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H.%M.%S')

current_script_name = os.path.basename(__file__).replace('.py','')

###################################### SETUP logging ######################################
log_dir = "/cvar/jhlab/XXX" #OBS VARIABLE. E.g. "/cvar/jhlab/snpsnap/logs_pipeline/logs_bsub"
if not os.path.exists(log_dir):
	os.makedirs(log_dir)

log_name = "{current_script_name}_{timestamp}".format(current_script_name=current_script_name, timestamp=batch_time)

logger = pplogger.Logger(name=log_name, log_dir=log_dir, log_format=1, enabled=True).get()
def handleException(excType, excValue, traceback, logger=logger):
	logger.error("Logging an uncaught exception", exc_info=(excType, excValue, traceback))
#### TURN THIS ON OR OFF: must correspond to enabled='True'/'False'
sys.excepthook = handleException
logger.info( "INSTANTIATION NOTE: placeholder" )
###########################################################################################


############################# SWITCH ##########################################

var1_parameter_list = ["XXX"]
var2_paramter_list = ["YYY"]



##############################################################################


output_dir_base = "/cvar/jhlab/XXX"

if not os.path.exists(output_dir_base):
	logger.warning( "Output path %s does not exist. Will create it" % output_dir_base )
	os.makedirs(output_dir_base)


###################################### RUN FUNCTIONS ######################################
# NOW RUN FUNCTIONS
LogArguments()
processes = submit()

start_time_check_jobs = time.time()
check_jobs(processes, logger) # TODO: parse multiprocess argument?
elapsed_time = time.time() - start_time_check_jobs
logger.info( "Total Runtime for check_jobs: %s s (%s min)" % (elapsed_time, elapsed_time/60) )
logger.critical( "%s: finished" % current_script_name)








