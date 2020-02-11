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

        name = re.sub('[^A-Za-z0-9 ]', '', name).lower().replace(' ', '_')
        _job = job.Job(name, description=description, queue=queue)
        self.job_queue.append(_job)

        print('[condortools] Job "{0}" successfully added to queue'.format(name))

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
                    
                    f.write('initialdir = {0}/jobs/{1}\n'.format(os.getcwd(), job.name))
                    f.write('output = {0}/jobs/{1}/logs/out$(PROCESS).log\n'.format(os.getcwd(), job.name))
                    f.write('error = {0}/jobs/{1}/logs/err$(PROCESS).log\n'.format(os.getcwd(), job.name))
                    f.write('log = {0}/jobs/{1}/logs/log.log\n'.format(os.getcwd(), job.name))
                    f.write('notification = never\n') # Has to be set to never for UoL Condor
                    f.write('queue {0}\n\n'.format(job.queue))

                job.status = 'built'
                job.updated_at = time.time()
                self.built_jobs.append(job)

            except Exception as e:
                print('[condortools] Error occurred whilst building job "{0}"\n{1}\n'.format(job.name, e))
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
                print('[condortools] Submitting job {0}'.format(job.name))
                proc = subprocess.run(['condor_submit', '{0}/jobs/{1}/{1}.sub'.format(os.getcwd(), job.name)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print('[condortools] Error occurred whilst submitting job "{0}"\n{1}\n'.format(job.name, e))
                job.updated_at = time.time()
                job.status = 'failed_submit'
                self.failed_jobs.append(job)
            except Exception as e:
                print('[condortools] Error occurred whilst submitting job "{0}"\n{1}\n'.format(job.name, e))
                job.updated_at = time.time()
                job.status = 'failed_submit'
                self.failed_jobs.append(job)
            else:
                if proc.stderr:
                    print(proc.stdout.decode('utf-8'))
                    print(proc.stderr.decode('utf-8'))
                    job.updated_at = time.time()
                    job.status = 'failed_submit'
                    self.failed_jobs.append(job)
                else:
                    print(proc.stdout.decode('utf-8'))
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
            
            # Submit jobs
            try:
                print('[condortools] Submitting jobs')
                proc = subprocess.run(['condor_submit', '{0}/jobs/multi_submit.sub'.format(os.getcwd())],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print('[condortools] Error occurred whilst submitting jobs\n{0}\n'.format(e))
                updated_at = time.time()
                status = 'failed_submit'
                self.failed_jobs.append(temp_submitted_jobs)
            except Exception as e:
                print('[condortools] Error occurred whilst submitting jobs"\n{0}\n'.format(e))
                updated_at = time.time()
                status = 'failed_submit'
                self.failed_jobs.append(temp_submitted_jobs)
            else:
                if proc.stderr:
                    print(proc.stdout.decode('utf-8'))
                    print(proc.stderr.decode('utf-8'))
                    updated_at = time.time()
                    status = 'failed_submit'
                    self.failed_jobs.append(temp_submitted_jobs)
                else:
                    print(proc.stdout.decode('utf-8'))
                    job.updated_at = time.time()
                    job.status = 'submitted'
                    self.submitted_jobs.append(job)
    
    def build_submit(self):
        '''
        '''

        self.build_submit_files()
        self.submit()

    def remove_job(self):
        return
    
    def watch_jobs(self):
        return

    def wait_job(self, job_name):
        try:
            print("[condortools] Waiting for all jobs to complete")
            subprocess.call(['condor_wait', '{0}/jobs/{1}/logs/log.log'.format(os.getcwd(), job_name)])

        except Exception as e:
            print("Error:\n%s" % (e))

