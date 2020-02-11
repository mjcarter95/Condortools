import sys
sys.path.append('..')
import condortools

parser = condortools.Parser('log/log.log')
parser.read()