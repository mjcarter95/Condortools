# Job
The job class is a programmatic representation of a job in HTCondor. The class takes three arguments:

```
name        | The name of the job
description | A Pythonic representation of the job description, usually an extension of a job template
num_jobs    | The number of jobs to submit - 'queue' in the job description file 
```

**Note:** A random string is added to the end of the job name. This means that the true job name is name_some0random1string.

and has the following attributes

```
last_updated | The time that the job was last updated
status       | The current status of the job
cluster_id   | Cluster that the job was submitted to (requires parsing of the job log file)
children     | If num_jobs > 1 we say that the Job has "children". The status of all child jobs (status, status_id, last_updated) is stored here.
```

**Note:** The job status gives preference to errors. That means, for example, if 1 out of N jobs fail the overall status of the job is fail.

## Usage
The example below shows how to define a Python job that utilises the Vanilla HTCondor universe.

### Create and submit job
1. Define the job description
```
my_job_description = templates.vanilla_python
my_job_description['python_file'] = "python_program.py"
```

2. Create the job object
```
python_job = Job(name="my_python_job",
                 description=my_job_description,
                 num_jobs=5)
```

**Note:** Creating the job object will also create a directory to store the job logs; all input files should be stored in this directory, similarly all output files will be written to this directory. It is recommended that all input files are created **before** step 3 below.

3. Build the job description and submit
```
python_job.build_submit_file()
python_job.submit()
```

### Waiting for the job to complete
#### Naive approach
HTCondor provides the command `condor_wait job.log` which allows us to determine when all jobs have finished. The same result can be achieved programmatically by

```
job.wait()
```

However, if jobs are held, we will be waiting forever. Actively parsing the log file allows us to react to and manage jobs that are held.

This is shown in practice in the `monte-carlo-naive-wait` example.

#### Parsing the log file
The Condortools module provides a `Parser` class which reads the log file to determine the current status of jobs. We can utilise this to actively determine the status of jobs and react to held jobs on the fly.

The latest status of a job (and its children) can be determined by

```
job.update_status()
```

We can utilise this functionality inside a while loop to repeatedly update the job status as follows

```
CHECK_LOG_FREQUENCY = 60

continue_waiting = True
while continue_waiting:
    idle = []
    running = []
    complete = []
    errors = []
    job.update_status()
    for job_id in job.children.keys():
        _job = job.children[job_id]
        if _job['status'] == 'idle':
            idle.append(job_id)
        elif _job['status'] == 'running':
            running.append(job_id)
        elif _job['status'] == 'error':
            errors.append(job_id)
        elif _job['status'] == 'complete':
            complete.append(job_id)
    print('Idle {} Running {} Complete {} Errors {}'.format(len(idle),
                                                            len(running),
                                                            len(complete),
                                                            len(errors)))
    # React to errors

    # If no jobs are running, exit

    sleep(CHECK_LOG_FREQUENCY)
```

This is shown in practice in the `monte-carlo-smart-wait` example.