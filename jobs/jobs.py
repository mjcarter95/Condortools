import os
import subprocess

class Job:
    '''

    '''

    def __init__(self, name, executable, n_jobs, universe, input_, output, log='log.txt'):
        if name == None or executable == None:
            raise ValueError()

        self.name = name
        self.executable = executable
        self.n_jobs = n_jobs
        self.universe = universe
        self.input_ = input_
        self.output = output
        self.log = log

    def create_submit_file(self):
        '''

        '''

        try:
            with open(self.name, 'w') as f:
                f.write("python_script        = %s\n" % (self.executable))
                f.write("indexed_input_files  = %s\n" % ("input.dat"))
                f.write("indexed_output_files = %s\n" % ("output.dat"))
                f.write("log                  = %s\n" % (self.log))
                f.write("total_jobs           = %s\n" % (self.n_jobs))
                f.write("python_version       = python_3.7.4")
            
            print("Created submit file for job: %s" % (self.name))

        except:
            print("Oshi")

        return

    def submit(self):
        '''

        '''

        try:
            print("Submitting %d job(s) (submit file: %s)" % (self.n_jobs, self.name))
            subprocess.call(['python_submit', self.name])

        except Exception as e:
            print("Error:\n%s" % (e))

        return

    def remove(self):
        return
    
    def wait(self):
        '''

        '''

        try:
            print("Waiting for all jobs to complete")
            subprocess.call(['condor_wait', self.log])
            print("All jobs are complete")

        except Exception as e:
            print("Error:\n%s" % (e))

        return