import sys
sys.path.append('..')
import condortools

# Instantiate parser
log_file = 'log/log.log'
parser = condortools.Parser(log_file)

print(parser.event_code(1)) # Test event codes

latest_event = parser.parse_latest_event()
print(latest_event)

print(parser.parse_log_file())