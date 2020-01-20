import os
import time

class Job():
    def __init__(self, name, description={}, queue=1):
        '''
        
        :param name             Name of job 
        :param description      A dictionary containing arguments of the job
                                NOTE: Excludes logs (log, stderr, stdout) which are saved to
                                      /logs/name/ by default. Input files are fetched from
                                      /data/name/inputs/ and output files are saved to
                                      /data/name/outputs/
        :param queue            Number of jobs to queue
        '''

        if not os.path.exists('logs/' + name):
            os.mkdir('logs/' + name)
        
        self.created_at           = time.time()
        self.updated_at           = time.time()
        self.status               = None

        self.name                 = name
        self.description          = description
        self.queue                = queue