import sys
sys.path.append('../..')
import condortools

parser = condortools.Parser('log.log')
parser.read()