# https://research.cs.wisc.edu/htcondor/manual/v7.6.2/2_6Managing_Job.html
import re
from file_read_backwards import FileReadBackwards

class Parser:
    '''
    Parses Condor log file to get the status of a job
    '''

    def __init__(self, log_file):
        self._log_file = log_file
    
    @property
    def log_file(self):
        return self._log_file

    def event_code(self, code):
        event_codes = {
            0: 'Submitted',
            1: 'Job Executing',
            2: 'Error in Executable',
            4: 'Job was checkpointed',
            5: 'Job evicted from machine',
            6: 'Job terminated',
            7: 'Image size of job updated',
            8: 'Shadow exception',
            9: 'Generic log event',
            11: 'Job aborted',
            12: 'Job was suspended',
            13: 'Job was unsuspended',
            14: 'Job was held',
            15: 'Job was released'
        }

        if code in event_codes:
            return event_codes[code]
        
        return

    def extract_event(self, str):
        executing = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job executing on host")
        held = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job was held")
        released = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job was released")
        evicted = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job was evicted")
        terminated = re.compile("\d\d\d+\s+\((\d+\.\d+).*\)\s+(.*)\s+Job terminated")
        
        if executing.search(str):
            return executing.search(str)
        elif held.search(str):
            return held.search(str)
        elif released.search(str):
            return released.search(str)
        elif evicted.search(str):
            return evicted.search(str)
        elif terminated.search(str):
            return terminated.search(str)
        
        return 0

    def parse_log_file(self):
        event_string = ''

        with open(self._log_file, encoding="utf-8") as f:
            for line in f:
                if line == '...':
                    print(self.extract_event(event_string))
                    # print(event_string)
                    event_string = ''
                    continue
                print(line)
                event_string += line

    def parse_latest_event(self):
        event_string = ''

        with FileReadBackwards(self._log_file, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i > 0 and line == '...':
                    break
                elif i == 0:
                    continue

                event_string += line
        
        return self.extract_event(event_string)

