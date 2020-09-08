'''
The following Python code shows how to utilise Condortools
to programmatically submit jobs to HTCondor. This example
problem estimates pi using the Monte Carlo method.

The general Condortools workflow is:
1. Create a description of your job
2. Create the job object
3. Build the job description and submit the job
4. Wait for the jobs to finish
5. Process the results

* Steps 1 and 2 are sometimes swapped, as shown below
'''

import os


from condortools import Templates, Job, Utils

templates = Templates()
utils = Utils()

# HTCondor settings
N_JOBS = 5

# Job object
monte_carlo = Job(name="monte_carlo",
                  num_jobs=N_JOBS)

# Job description - This extends from the base vanilla description defined in
#                   the Condortools module. However, note that we need to modify
#                   some of the arguments for our specific job.
job_description = templates.vanilla_python
job_description['job_name'] = monte_carlo.name
job_description['executable'] = '{}/helper_files/python_submit_o.bat'.format(utils.module_dir)
job_description['arguments'] = "estimate_pi.py $(PROCESS) output.txt python_3.7.4"
job_description['transfer_input_files'] = "{}/estimate_pi.py, /opt1/condor/apps/python/python_3.7.4.zip, /opt1/condor/apps/matlab/index.exe, /opt1/condor/apps/matlab/unindex.exe".format(os.getcwd())
job_description['transfer_output_files'] = "output$(PROCESS).txt"
job_description['output'] = '{}/jobs/{}/logs/stdout$(PROCESS).out'.format(os.getcwd(), monte_carlo.name)
job_description['error'] = '{}/jobs/{}/logs/stderr$(PROCESS).err'.format(os.getcwd(), monte_carlo.name)
job_description['log'] = '{}/jobs/{}/logs/log.log'.format(os.getcwd(), monte_carlo.name)
del job_description["python_file"]

# Update job description in job object
monte_carlo.description = job_description

# Create job description and submit
monte_carlo.build_submit_file()
monte_carlo.submit()

# Wait for job to complete
monte_carlo.wait()

# Process job outputs
pi_estimate = 0
for i in range(N_JOBS):
    file_name = '{}/output{}.txt'.format(monte_carlo.job_dir,
                               i)
    with open(file_name, 'r') as f:
        pi_estimate += float(f.readline())
pi_estimate /= N_JOBS

# Output final result
print('Estimate of pi: {}'.format(pi_estimate))