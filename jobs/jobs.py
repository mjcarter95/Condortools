import os
import subprocess
from os.path import dirname, abspath

class Job:
    '''
    '''

    def __init__(self, name, executable, n_jobs, universe, _input, _output):
        if name == None or executable == None:
            raise ValueError()

        self.name = name
        self.executable = executable
        self.n_jobs = n_jobs
        self.universe = universe
        self.input = _input
        self.output = _output

    def create_submit_file(self):
        '''
        '''

        print(dirname(dirname(abspath(__file__))))

        try:
            if not os.path.exists('logs'):
                os.makedirs('logs')

            with open(self.name, 'w') as f:
                f.write("python_script        = %s\n" % (self.executable))
                f.write("python_version       = python_3.7.4\n")
                f.write("indexed_input_files  = %s\n" % (self.input))
                f.write("indexed_output_files = %s\n" % (self.output))
                f.write("total_jobs           = %s\n" % (self.n_jobs))
                # f.write("indexed_log          = logs/log.log\n")
                f.write("log                  = logs/log.log\n")
                f.write("indexed_stdout       = logs/out.log\n")
                f.write("indexed_stderr       = logs/err.log")
            
            print("Created submit file for job: %s" % (self.name))

        except Exception as e:
            print("An error occurred when generating the submit file\n%s" % e)

    def submit(self):
        '''
        '''

        try:
            print("Submitting %d job(s) (submit file: %s)" % (self.n_jobs, self.name))
            subprocess.call(['python_submit', self.name])

        except Exception as e:
            print("Error:\n%s" % e)

    def remove(self):
        return
    
    def wait(self):
        '''
        '''

        try:
            print("Waiting for all jobs to complete")
            subprocess.call(['condor_wait', 'logs/log.log'])

        except Exception as e:
            print("Error:\n%s" % (e))

        return