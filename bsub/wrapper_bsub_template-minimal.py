#!/usr/bin/env python2.7

import os
import time

import subprocess


def submit():
	processes = []

	for var1 in var1_parameter_list:
		print "****** RUNNING: var1=%s *******" % var1
		for var2 in var2_paramter_list:
			print "****** RUNNING: var2=%s *******" % var2


				dir_out = "{base}/{var1}/{var2}".format(base=output_dir_base, var1=var1, var2=var2)
				if not os.path.exists(dir_out):
					os.makedirs(dir_out)
				out = XXX

				cmd_program = "python XXX.py --out {out} --var1 {var1} --var2 {var2}".format(out=out, var1=var1, var2=var2)
				print "COMMAND: %s" % cmd_program

				job_name = "XXXX".format(XXXX)
				project_name = "projectXXX"
				output_bsub = "/dev/null"
				queue = "priority"
				p_mem = "20"
				p_proc = "1"


				cmd_queue = "bsub -P {project_name} -J {job_name} -o {output_bsub} -r -q {p_queue} -R 'rusage[mem={p_mem}] -n {p_proc}".format(project_name=project_name, job_name=job_name, output_bsub=output_bsub, p_queue=p_queue, p_mem=p_mem, p_proc=p_proc)
				processes.append(cmd_queue)

	for p in processes:
		subprocess_out = subprocess.check_output(cmd_queue, shell=True)
		print "SUBPROCESS OUT: {}".format(subprocess_out)
		time.sleep(0.5)



###################################### CONSTANTS ######################################
# current_script_name = os.path.basename(__file__).replace('.py','')

############################# LOOP VARIABLES ##########################################

var1_parameter_list = ["XXX"]
var2_paramter_list = ["YYY"]

##############################################################################

output_dir_base = "/cvar/jhlab/XXX"

if not os.path.exists(output_dir_base):
	print "Output path %s does not exist. Will create it" % output_dir_base
	os.makedirs(output_dir_base)


###################################### RUN FUNCTIONS ######################################

start_time = time.time()
submit()
elapsed_time = time.time() - start_time
print "DONE. Total runtime: %s s (%s min)" % (elapsed_time, elapsed_time/60)








