import os

from copy import deepcopy
from collections import deque
from time import time, sleep

from .utils import Utils


class Scheduler:
    '''

    '''

    def __init__(self, policy=0, retry=True):
        '''
        '''

        self.utils = Utils()
        self.utils.create_directory('jobs')

        self._retry = retry
        self._policy = policy
        self._job_queue = deque()
        self._submitted_queue = deque()
        self._completed_queue = deque()
        self._failed_queue = deque()

    def __str__(self):
        return '\nqueued_jobs: {}, submitted_jobs: {}, completed jobs: {}, failed_jobs: {}'.format(len(self._job_queue),
                                                                                                   len(self._submitted_queue),
                                                                                                   len(self._completed_queue),
                                                                                                   len(self._failed_queue))

    def __repr__(self):
        return '\nScheduler(queued_jobs={}, submitted_jobs={}, completed jobs: {}, failed_jobs={})'.format(len(self._job_queue),
                                                                                                   len(self._submitted_queue),
                                                                                                   len(self._completed_queue),
                                                                                                   len(self._failed_queue))

    @property
    def job_queue(self):
        return self._job_queue

    @property
    def submitted_queue(self):
        return self._submitted_queue

    @property
    def failed_queue(self):
        return self._failed_queue

    @property
    def policies(self, id):
        return self._policy
    
    @property
    def policy(self):
        return self._policy
    
    @policy.setter
    def policy(self, policy_id):
        self._policy = policy_id
    
    def add_job(self, job_name, job):
        self._job_queue.append((job_name, job))

    def add_submitted(self, job_name, job):
        self._submitted_queue.append((job_name, job))

    def add_completed(self, job_name, job):
        self._completed_queue.append((job_name, job))

    def add_failed(self, job_name, job):
        self._failed_queue.append((job_name, job))

    def submit_jobs(self, test_submit=False):
        if len(self._job_queue) == 0:
            print("Oops, the job queue is empty!")
        elif len(self._job_queue) == 1:
            job_tuple = self._job_queue.pop()
            job_name = job_tuple[0]
            job = job_tuple[1]
            job_description = '{0}/jobs/{1}/{1}.sub'.format(self.utils.cwd, job_name)
            try:
                job.build_submit()
                self.add_submitted(job_name, job)
            except Exception as e:
                print(e)
                self.add_job(job_name, job)
        else:
            temp_job_queue = deepcopy(self._job_queue)
            temp_submitted_queue = deepcopy(self._submitted_queue)
            submit_file = '{}/jobs/multi_submit.sub'.format(self.utils.cwd)
            with open(submit_file, 'w') as f:
                while len(self._job_queue) > 0:
                    job_tuple = self._job_queue.pop()
                    job_name = job_tuple[0]
                    job = job_tuple[1]
                    submit_string = job.build_submit_file_string()
                    f.write('{}\n'.format(submit_string))
            try:
                self.utils.job_submit(submit_file)
            except Exception as e:
                print(e)
                self._job_queue = temp_job_queue
                self._submitted_queue = temp_submitted_queue

    def watch_jobs(self, freq=None):
        if len(self._submitted_queue) == 0:
            return
        while len(self._submitted_queue) > 0:
            job_tuple = self._submitted_queue.pop()
            job_name = job_tuple[0]
            job = job_tuple[1]
            job.update_status()
            if job.status == 'complete':
                self.add_completed(job_name, job)
                continue
            elif job.status == 'error':
                self.add_failed(job_name, job)
                continue
            else:
                self.add_submitted(job_name, job)
            if freq is not None:
                sleep(freq)

    def resubmit(self):
        return