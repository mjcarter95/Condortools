import os
import time

class Job:
    def __init__(self, name, arguments=None, num_jobs=1):
        '''
        Class representation of a job in HTCondor

        :param name         Name of the job
        :param description  A description of the job, provided as either a dictionary or template object.
                            If empty, it is assumed that the job description file is already provided in
                            the job directory.
        '''

        self.name       = name
        self.arguments  = arguments
        self.num_jobs   = num_jobs

        # Properties for tracking job information
        self.status     = None
        self.created_at = time.time()
        self.updated_at = time.time()

        # Ensure that job and log directories exist
        # if not os.
    
    def build_submit_file(self):
        return

    def submit(self, queue=None):
        return

    def build_submit(self, queue=None):
        self.build_submit_file()
        self.submit(queue=queue)

    def remove(self):
        return
    
    def status(self):
        '''
        Returns the current status of a job
        '''
        return self.status
