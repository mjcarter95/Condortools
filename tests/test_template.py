from collections import OrderedDict

# Import relevant Condortools modules
import sys
sys.path.append('..')
from condortools import Job, Templates

desc = Templates().vanilla_python # Use the base vanilla description file

# Update some job description parameters
desc['job_name'] = 'predict_update'
desc['python_file'] = 'predict_update.py'

print('\n-- Start Job Description --\n{}\n-- End Job Description --\n\n'.format(desc))

job = Job(desc['job_name'], desc, 2)
job.build_submit_file()
job.submit()