import os

from .utils import Utils

class Scheduler:
    '''

    '''

    def __init__(self, retry=True):
        '''
        '''

        self.utils = Utils()
        self.utils.create_directory('jobs')

        self._retry = retry
        self._job_queue = {}
        self._submitted_queue = {}
        self._failed_queue = {}

    def __str__(self):
        return '\nqueued_jobs: {}, submitted_jobs: {}, failed_jobs: {}'.format(len(self._job_queue), len(self._submitted_queue), len(self._failed_queue))

    def __repr__(self):
        return '\nScheduler(queued_jobs={}, submitted_jobs={}, failed_jobs={})'.format(len(self._job_queue), len(self._submitted_queue), len(self._failed_queue))

    @property
    def job_queue(self):
        return self._job_queue

    @property
    def submitted_queue(self):
        return self._submitted_queue

    @property
    def failed_queue(self):
        return self._failed_queue
    
    def add_job(self, job_name, job):
        self._job_queue[job_name] = job

    def add_submitted(self, job_name, job):
        self._submitted_queue[job_name] = job

    def add_failed(self, job_name, job):
        self._failed_queue[job_name] = job

    def watch_jobs(self):
        return
    
    def resubmit(self):
        return