class Parser:
    '''
    Parses Condor log file to get the status of a job
    '''

    def __init__(self, log_file):
        self.log_file = log_file
    
    def read(self):
        with open(self.log_file, 'r') as f:
            for line in f:
                print(line)