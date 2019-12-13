from condortools import common

m = common.Manage()

n_computers, console = m.pool_status()
print(console)
print(n_computers)

available_computers = console[(console['State'] == 'Unclaimed') & (console['Activity'] == 'Idle')]
available_computers = available_computers.sort_values('Mem')

print(available_computers)
print(len(available_computers))