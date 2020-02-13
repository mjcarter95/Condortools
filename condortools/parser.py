# https://research.cs.wisc.edu/htcondor/manual/v7.6.2/2_6Managing_Job.html

class Parser:
    '''
    Parses Condor log file to get the status of a job
    '''

    def __init__(self, log_file):
        self._log_file = log_file
    
    @property
    def log_file(self):
        return self._log_file

    def status_code(self, code):
        status_codes = {
            '0': 'idle',
            '1': 'complete'
        }

        return status_codes[code]