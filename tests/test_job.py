from collections import OrderedDict

import sys
sys.path.append('..')
from condortools import Job

desc = OrderedDict()
desc['job_name'] = 'predict_update'
desc['universe'] = 'vanilla'
desc['executable'] = 'predict_update.py'

job = Job(desc['job_name'], desc['executable'], desc)

print(job)
print(job.name)