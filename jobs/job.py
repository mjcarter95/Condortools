import os
import time

class Job():
    def __init__(self, name, description={}, queue=1):
        '''
        
        :param name             Name of job 
        :param description      A dictionary containing arguments of the job
                                NOTE: Excludes logs (log, stderr, stdout) which are saved to
                                      /jobs/name/logs by default. Input files are fetched from
                                      /jobs/name/input_data/ and output files are saved to
                                      /jobs/name/output_data/
        :param queue            Number of jobs to queue
        '''

        if not os.path.exists('jobs/' + name):
            os.mkdir('jobs/' + name)

        if not os.path.exists('jobs/' + name + '/logs'):
            os.mkdir('jobs/' + name + '/logs')


            '''
            NOTE: Can't store input and output data in separate directories. For example,
                  if output listed as /output_data/output$(PROC).json, Condor will try fetch
                  from /output_data/ temp dir on the worker.
            '''
        
        self.created_at           = time.time()
        self.updated_at           = time.time()
        self.status               = None

        self.name                 = name
        self.description          = description
        self.queue                = queue