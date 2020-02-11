from collections import OrderedDict

import sys
sys.path.append('..')
from condortools import Job

desc = OrderedDict()
desc['job_name'] = 'predict_update'
desc['universe'] = 'vanilla'

job = Job(desc['job_name'], desc)

print(job)
print(job.name)

