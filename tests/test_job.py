from collections import OrderedDict

import sys
sys.path.append('..')
from condortools import Job

desc = OrderedDict()
desc['job_name'] = 'predict_update'
desc['universe'] = 'vanilla'

job = Job(desc['job_name'], desc, num_jobs=5)

print(job)
print(job.name)
print(job.build_submit_file_string())

job.update_status()
print(job.children)
print(job.status)