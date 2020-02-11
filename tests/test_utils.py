import sys
sys.path.append('..')
from condortools import Utils

utils = Utils()

print('\nCurrent working directory: {}'.format(utils.cwd))

utils.create_directory('test_dir') # Create a test directory

utils._execute('ls', ['-l'])

