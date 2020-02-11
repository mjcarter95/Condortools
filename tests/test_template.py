from collections import OrderedDict

# Import relevant Condortools modules
import sys
sys.path.append('..')
from condortools import Job, Templates

desc = Templates().vanilla # Use the base vanilla description file
print('\n{}'.format(desc))

# Update some job description parameters
desc['job_name'] = 'predict_update'
desc['executable'] = 'predict_update.py'
print('\n{}'.format(desc))

job = Job(desc['job_name'], desc['executable'], desc)

print(job)
print(job.name)