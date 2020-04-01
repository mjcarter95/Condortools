import os

from copy import deepcopy

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
        self._job_queue[job_name] = job

    def add_submitted(self, job_name, job):
        self._submitted_queue[job_name] = job

    def add_failed(self, job_name, job):
        self._failed_queue[job_name] = job

    def submit_jobs(self, test_submit=False):
        if not self._job_queue:
            return
        elif len(self._job_queue) == 1:
            job_name = list(self._job_queue)[0]
            job = list(self._job_queue.values())[0]
            job_description = '{0}/jobs/{1}/{1}.sub'.format(self.utils.cwd, job_name)
            print(job_description)
            try:
                self.utils.job_submit(job_description, test_submit)
                del self._job_queue[job_name]
                self._submitted_queue[job_name] = job
            except Exception as e:
                print(e)
        else:
            temp_job_queue = deepcopy(self._job_queue)
            temp_submitted_queue = deepcopy(self._submitted_queue)
            
            submit_file = '{}/jobs/multi_submit.sub'.format(self.utils.cwd)

            with open(submit_file, 'w') as f:
                for job in list(self._job_queue.keys()):
                    submit_string = self._job_queue[job].build_submit_file_string()
                    f.write('%s' % submit_string)
                    self._submitted_queue[job] = self._job_queue[job]
                    del self._job_queue[job]

            try:
                self.utils.job_submit(submit_file)
            except Exception as e:
                self._job_queue = temp_job_queue
                self._submitted_queue = temp_submitted_queue
                print(e)

    def watch_jobs(self):
        return
    
    def resubmit(self):
        return