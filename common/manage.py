import re
import subprocess
import pandas as pd

class Manage:
    '''
    '''

    def __init__(self):
        return
    
    def pool_status(self):
        '''
        '''

        out = subprocess.check_output(['condor_status'])
        out = out.decode("utf-8")
        out = out.split('\n')[2:-7]
        
        for i, x in enumerate(out):
            out[i] = re.sub('[A-Za-z ]+', '', out[i]) 
            out[i] = out[i].split()
        
        # out = pd.DataFrame(out, columns=['Name', 'OpSys', 'Arch', 'State', 'Activity', 'LoadAv', 'Mem', 'ActivityTime'])
        # out = out[(out['State'] == 'Unclaimed') & (out['Activity'] == 'Idle')]

        print(out[0])

        # return console, n_avail