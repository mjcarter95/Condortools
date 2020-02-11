    # 'universe': 'vanilla',
    # 'should_transfer_files': 'YES',
    # 'when_to_transfer_output': 'ON_EXIT',
    # 'executable': 'submit_sum.bat',
    # 'arguments': 'sum.py $(PROCESS)  input.json output.json python_3.7.4',
    # 'transfer_input_files': 'input$(PROCESS).json,sum.py,/opt1/condor/apps/python/python_3.7.4.zip,/opt1/condor/apps/matlab/index.exe,/opt1/condor/apps/matlab/unindex.exe',
    # 'transfer_output_files': 'output$(PROCESS).json',
    # # 'Rank': '(machine == "slot1@WSTC-028.livad.liv.ac.uk")',
    # 'request_cpus': 1,
    # 'requirements': '(Arch=="X86_64") && (OpSys=="WINDOWS")'

from collections import OrderedDict

class Templates:
    '''
    '''

    def __init__(self):
        pass

    @property
    def base(self):
        base = OrderedDict()
        base['job_name'] = ''
        base['universe'] = ''
        base['executable'] = ''

        base['notification'] = 'NEVER' # UoL Condor requirement
        return base

    @property
    def vanilla(self):
        vanilla = self.base
        vanilla['universe'] = 'vanilla'
        return vanilla