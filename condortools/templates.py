from collections import OrderedDict

from .utils import Utils

class Templates:
    '''
    '''

    def __init__(self):
        self.utils = Utils()

    @property
    def base(self):
        '''
        Base job description file for UoL Condor
        '''
        base = OrderedDict()
        base['job_name'] = None
        base['universe'] = None
        base['executable'] = None
        base['arguments'] = None
        base['transfer_input_files'] = None
        base['transfer_input_files'] = None
        base['should_transfer_files'] = 'YES'
        base['when_to_transfer_output'] = 'ON_EXIT'
        base['request_cpus'] = 1
        base['requirements'] = '(Arch=="X86_64") && (OpSys=="WINDOWS")'
        base['initialdir'] = '{}/jobs/$(job_name)'.format(self.utils.cwd)
        base['logdir'] = 'logs'
        base['output'] = '$(logdir)/$(job_name)/stdout.$(cluster).log'
        base['output'] = '$(logdir)/$(job_name)/stderr.$(cluster).log'
        base['output'] = '$(logdir)/$(job_name)/log.$(cluster).log'
        base['notification'] = 'never'
        return base

    @property
    def vanilla(self):
        vanilla = self.base
        vanilla['universe'] = 'vanilla'
        return vanilla
    
    @property
    def vanilla_python(self):
        '''
        Base submission file for submitting Python files to UoL Condor

        NOTE: Assumes inputs are labelled from 0 to n (ie input0.dat, input1.dat, ...)
        '''

        vanilla_python = self.vanilla
        vanilla_python['python_file'] = ''
        vanilla_python['executable'] = '{}/helper_files/python_submit.bat'.format(self.utils.module_dir)
        vanilla_python['transfer_input_files'] = 'input$(PROCESS).json, $(python_file), /opt1/condor/apps/python/python_3.7.4.zip, /opt1/condor/apps/matlab/index.exe, /opt1/condor/apps/matlab/unindex.exe'
        vanilla_python['transfer_output_files'] = 'output$(PROCESS).json'
        return vanilla_python