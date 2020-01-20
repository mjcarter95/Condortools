import os
import re
import time
import subprocess
from condortools.jobs import job
from collections import deque

class Scheduler:
    def __init__(self, retry=False):
        self.retry = retry

        self.job_queue       = deque([]) # Queue of jobs to be submitted
        self.built_jobs      = deque([])
        self.submitted_jobs  = deque([])
        self.failed_jobs     = deque([])

        # Check if logs directory exists
        if not os.path.exists('jobs'):
            os.mkdir('jobs')
    
    def add_job(self, name, description={}, queue=1):
        '''
        Add job to queue
        '''

        name = re.sub('[^A-Za-z0-9]', '', name).lower()
        _job = job.Job(name, description=description, queue=1)
        self.job_queue.append(_job)

        print('Job "{0}" successfully added to queue'.format(name))

    def build_submit_files(self):
        '''
        Build job submission file
        '''

        ignored_arguments = ['initialdir', 'output', 'error', 'log', 'notifications', 'queue']

        while self.job_queue:
            job = self.job_queue.popleft()

            try:
                with open('jobs/' + job.name + '/' + job.name + '.sub', "w") as f:
                    for key in job.description.keys():
                        if key in ignored_arguments:
                            continue

                        f.write('{0} = {1}\n'.format(key, job.description[key]))
                    
                    f.write('initialdir = jobs/{0}\n'.format(job.name))
                    f.write('output = logs/out$(PROCESS).log\n')
                    f.write('error = logs/err$(PROCESS).log\n')
                    f.write('log = logs/log$(PROCESS).log\n')
                    f.write('notifications = none\n') # Has to be set to none for UoL Condor
                    f.write('queue {0}\n\n'.format(job.queue))

                job.status = 'built'
                job.updated_at = time.time()
                self.built_jobs.append(job)

            except Exception as e:
                print('Error occurred whilst building job "{0}"\n{1}\n'.format(job.name, e))
                self.failed_jobs.append(job)

    def submit(self):
        '''
        Submit jobs in the queue
        '''

        if not self.built_jobs:
            return
        elif len(self.built_jobs) == 1:
            job = self.built_jobs.popleft()

            try:
                print("lol")
            except Exception as e:
                print('Error occurred whilst submitting job "{0}"\n{1}\n'.format(job.name, e))
                self.failed_jobs.append(job)

            job.updated_at = time.time()
            job.status = 'submitted'
            self.submitted_jobs.append(job)

        else:
            temp_submitted_jobs = deque(self.built_jobs)

            # Build multi submit file
            with open('jobs/multi_submit.sub', 'w') as f:
                while self.built_jobs:
                    job = self.built_jobs.popleft()

                    with open('jobs/' + job.name + '/' + job.name + '.sub') as job_description:
                        f.write(job_description.read())
                    
                    temp_submitted_jobs.append(job)
    
    def remove_job(self):
        return
    
    def watch_jobs(self):
        return

