from condortools.jobs import *

scheduler = scheduler.Scheduler()
description = {
    'universe': 'vanilla',
    'should_transfer_files': 'YES',
    'when_to_transfer_output': 'ON_EXIT',
    'executable': 'submit_sum.bat',
    'arguments': 'sum.py $(PROCESS)  input.json output.json python_3.7.4',
    'transfer_input_files': 'input$(PROCESS).json,sum.py,/opt1/condor/apps/python/python_3.7.4.zip,/opt1/condor/apps/matlab/index.exe,/opt1/condor/apps/matlab/unindex.exe',
    'transfer_output_files': 'output$(PROCESS).json',
    # 'Rank': '(machine == "slot1@WSTC-028.livad.liv.ac.uk")',
    'request_cpus': 1,
    'requirements': '(Arch=="X86_64") && (OpSys=="WINDOWS")'
}

# Test single job submission
# scheduler.add_job('Test Submission', description, 1)
# scheduler.build_submit_files()
# scheduler.submit()

# Test multi job submission
for x in range(0, 5):
    scheduler.add_job('Job %d' % x, description, 1)
scheduler.build_submit_files()
scheduler.submit()



# from common import manage

# m = manage.Manage()
# m.pool_status()

# n_computers, console = m.pool_status()
# print(console)
# print(n_computers)

# available_computers = console[(console['State'] == 'Unclaimed') & (console['Activity'] == 'Idle')]
# available_computers = available_computers.sort_values('Mem')

# print(available_computers)
# print(len(available_computers))