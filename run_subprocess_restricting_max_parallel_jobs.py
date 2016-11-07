### SUBPROCESS variables
MAX_NO_PARALLEL_SUBPROCESSES = 5
n_active_jobs = 0 # initial value
list_processes = [] # TODO: use a dict instead with all the job variables saved.
list_cmds = [] # TODO: use a dict instead with all the job variables saved.

### ANALYSIS variables
params = range(0,100,2) # 0,2,4,6,8, ..., 96, 98 # --> linar increasing sleep time for this test command.
#params = range(100,200,2) 

time_subprocess_submission = time.time() # initial value
for job_no, param in enumerate(params,start=1):
    print "CALL #{}/#{} | param={}".format(job_no, len(params), param)

    print "time since last submission: {:.3f}".format(time.time()-time_subprocess_submission) 
    time_subprocess_submission = time.time()
    cmd = """/bin/bash -c "sleep {}; ls -l ~/; echo 'done sleeping'" """.format(param) 
        # NOTE for test-command: sleep must we the first command in this test case, otherwise subprocess will think the command is finshed 
        # because of the semicolons seperating the bash statements
    #print cmd


    ### SUBPROCESS CALL
    p = subprocess.Popen(["/bin/sleep", "{}".format(param)], shell=False) # this is the simpel version of the test case.
    #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # this works independent of what shell "/bin/sh" is.
    #first_line_of_output = p.stdout.readline() # read one line from the output (stdout + stderr)
    #print first_line_of_output
    
    ### SAVE CALL to list tracking subprocesses
    list_processes.append(p) # saving object - important for job control
    list_cmds.append(cmd) # nice to save commands, so we can inspect them later
    print "submitted process. PID = {}".format(p.pid)
    
    ### CONTROLLER: limit the maximal number of jobs
    n_active_jobs = sum([1 for p in list_processes if p.poll() is None]) # update n_active_jobs | must also be done outside while loop.
    print "Number of active jobs: {}".format(n_active_jobs)
    while n_active_jobs >= MAX_NO_PARALLEL_SUBPROCESSES: # stay in this while-loop, as long as we have reached the maximum number of parallel jobs
        n_active_jobs = sum([1 for p in list_processes if p.poll() is None]) # update n_active_jobs
            # p.poll(): get returncode. A None value indicates that the process hasn’t terminated yet
        time.sleep(1) # take a nap - no reason to run this while-loop too many times.


###################################### NOTES on STDOUT/STDERR from JUPYTER SUBPROCESS CALLS ######################################

### No output to jupyter, but to the terminal running jupyter
#list_processes = [subprocess.Popen(["/bin/sleep", "10"], shell=False)]

### Output to jupyter works
# subprocess.Popen(["/bin/ls", "-l", "/bin"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()

### This works
# list_processes = [subprocess.Popen("""/bin/bash -c "sleep 2; ls -l; echo 'done sleeping'" """, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)]
# list_processes[0].stdout.readlines()
