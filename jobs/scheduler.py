# -*- coding: utf-8 -*-
import os
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
        if not os.path.exists('logs'):
            os.mkdir('logs')
    
    def add_job(self, name, description={}, queue=1):
        '''
        Add job to queue
        '''

        _job = job.Job(name, description=description, queue=1)
        self.job_queue.append(_job)

        print('Job "%s" successfully added to queue' % name)

    def build_submit_files(self):
        '''
        Build job submission file
        '''

        while self.job_queue:
            job = self.job_queue.popleft()

            try:
                with open(job.name, "w") as f:
                    for key in job.description.keys():
                        f.write(key + ' = ' + job.description[key] + '\n')

                    f.write('indexed_log = logs/%s/log.log\n' % job.name)
                    f.write('indexed_stdout = logs/%s/stdout.log\n' % job.name)
                    f.write('indexed_stderr = logs/%s/stderr.log\n' % job.name)
                    f.write('total_jobs = %d\n' % job.queue)

                job.status = 'built'
                job.updated_at = time.time()
                self.built_jobs.append(job)

            except Exception as e:
                print('Error occurred whilst building job %s\n%s\n' % (job.name, e))
                self.failed_jobs.append(job)
            
            break

    def submit(self):
        '''
        Submit jobs in the queue
        '''

        while self.built_jobs:
            job = self.built_jobs.popleft()
    
    def remove_job(self):
        return
    
    def watch_jobs(self):
        return

