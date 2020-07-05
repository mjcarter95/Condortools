import sys
sys.path.append('..')
import condortools

# Instantiate parser
log_file = 'log/log.log'
parser = condortools.Parser(log_file)

parser.parse_log_file()
for key in parser._event_dict.keys():
    print("Worker {}".format(key))
    print("Status {} description {}".format(parser._event_dict[key]['status_code'],
                                            parser._event_dict[key]['status_description']))
    print("\n\n\n")