'''
This code is run on the HTCondor worker.

Each worker forms it's own estimate of pi
and writes that to a text file.
'''

import sys
import numpy as np

n_throws = 10000
in_circle = 0.

# Throw the dart n_throws times
x = np.random.uniform(0, 1, n_throws)
y = np.random.uniform(0, 1, n_throws)

# Check if the dart hit the board
for i in range(0, n_throws):
    if((x[i] * x[i]) + (y[i] * y[i]) <= 1):
        in_circle += 1.

# Estimate value of pi
pi_estimate = 4. * in_circle / n_throws

# Write result to output file
with open('output.txt', 'w') as f:
    f.write('{}'.format(pi_estimate))