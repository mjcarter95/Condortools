# https://research.cs.wisc.edu/htcondor/manual/v7.6.2/2_6Managing_Job.html
import re


def event_desc(code):
    '''
    Returns a description of
    a given event code
    '''
    event_codes = {
        '000': 'Submitted',
        '001': 'Job Executing',
        '002': 'Error in Executable',
        '003': 'Job was checkpointed',
        '004': 'Job evicted from machine',
        '005': 'Job terminated',
        '006': 'Image size of job updated',
        '007': 'Shadow exception',
        '008': 'Generic log event',
        '009': 'Job aborted',
        '010': 'Job was suspended',
        '011': 'Job was unsuspended',
        '012': 'Job was held',
        '013': 'Job was released'
    }

    if code in event_codes:
        return event_codes[code]
    return


def event_readable(code):
    '''
    Returns a readable description of
    a given event code
    '''
    event_codes = {
        '000': 'idle',
        '001': 'running',
        '002': 'error',
        '003': 'checkpointed',
        '004': 'error',
        '005': 'complete',
        '006': 'running',
        '007': 'error',
        '008': 'running',
        '009': 'error',
        '010': 'error',
        '011': 'running',
        '012': 'error',
        '013': 'running'
    }

    if code in event_codes:
        return event_codes[code]
    return


class Parser:
    '''
    Parses Condor log file
    '''

    def __init__(self, log_file):
        self._log_file = log_file
        self._event_history = None
        self._start_from = 0
    
    @property
    def log_file(self):
        return self._log_file

    @property
    def event_history(self):
        return self._event_history

    def extract_event(self, str):
        submit = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job submitted from host")
        executing = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job executing on host")
        held = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job was held")
        released = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job was released")
        evicted = re.compile("\((\d+\.\d+).*\)\s+(.*)\s+Job was evicted")
        terminated = re.compile("\d\d\d+\s+\((\d+\.\d+).*\)\s+(.*)\s+Job terminated")
        exception = re.compile("\d\d\d+\s+\((\d+\.\d+).*\)\s+(.*)\s+Shadow exception!")
        
        if submit.search(str):
            return submit.search(str)
        elif executing.search(str):
            return executing.search(str)
        elif held.search(str):
            return held.search(str)
        elif released.search(str):
            return released.search(str)
        elif evicted.search(str):
            return evicted.search(str)
        elif terminated.search(str):
            return terminated.search(str)
        elif exception.search(str):
            return exception.search(str)
        return None
    
    def extract_event_details(self, str):
        event_match = re.compile("\d\d\d")
        worker_match = re.compile("\d\d\d.\d\d\d.\d\d\d")
        event_id = event_match.search(str).group()
        (cluster_id,
         worker_id,
         id_) = worker_match.search(str).group().split(".")
        return event_id, cluster_id, worker_id

    def parse_log_file(self):
        event_string = ''
        start_from = self._start_from
        event_dict = {}
        with open(self._log_file, encoding="utf-8") as f:
            for i in range(start_from):
                f.next()
            for i, line in enumerate(f):
                if "..." in line:
                    (event_id,
                     cluster_id,
                     worker_id) = self.extract_event_details(event_string)
                    if not worker_id in event_dict.keys():
                        event_dict[worker_id] = {
                            'cluster_id': cluster_id,
                            'status_code': event_id,
                            'status': event_readable(event_id),
                            'status_description': event_desc(event_id),
                            'status_time': None,
                            'event_history': [],
                            'job_details': {}
                        }
                    else:
                        event_dict[worker_id]['status_code'] = event_id
                        event_dict[worker_id]['status'] = event_readable(event_id)
                        event_dict[worker_id]['status_description'] = event_desc(event_id)
                    event_dict[worker_id]['event_history'].append(event_string)
                    event_string = ''
                    continue
                event_string += line
                self._start_from = i    
        self._event_history = event_dict