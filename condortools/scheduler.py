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

        self.retry = retry

    def watch_jobs(self):
        return
    
    def naive_wait(self, job):
        try:
            print("[condortools] Waiting for all jobs to complete")
            subprocess.call(['condor_wait', '{0}/jobs/{1}/logs/log.log'.format(os.getcwd(), job_name)])

        except Exception as e:
            print("Error:\n%s" % (e))