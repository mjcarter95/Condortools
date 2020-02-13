from collections import OrderedDict

import sys
sys.path.append('..')
from condortools import Scheduler, Job, Templates

scheduler = Scheduler()

desc = Templates().vanilla_python # Use the base vanilla description file
desc['job_name'] = 'predict_update'
desc['python_file'] = 'predict_update.py'
print('\n-- Start Job Description --\n{}\n-- End Job Description --\n\n'.format(desc))
job = Job(desc['job_name'], desc, 2) # Object representation of job

print(scheduler)
scheduler.add_job(desc['job_name'], job) # Add job to scheduler queue
scheduler.add_submitted('submitted_job', job) # Add job to scheduler queue
scheduler.add_failed('failed_job', job) # Add job to scheduler queue
print(scheduler)

scheduler.add_job('{}_2'.format(desc['job_name']), job) # Add job to scheduler queue
scheduler.add_submitted('submitted_job_2', job) # Add job to scheduler queue
scheduler.add_failed('failed_job_2', job) # Add job to scheduler queue
print(scheduler)