# Parser
Repeated polling of the HTCondor scheduler should be avoided. This class parses job log files to determine the current status of a job. The parser returns a dictionary where each key refers to the job id.

Returned dictionary structure:

```
event_history = {
    'job_id' = {
        'cluster_id': cluster_id,
        'status_code': event_id,
        'status': numeric status,
        'status_description': readable status,
        'status_time': time,
        'event_history': list of historic events,
        'job_details': additional job details
    }
}
```

## Parsing log files

```
# Instantiate log file
parser = Parser("log.log")

# Parse log file
event_history = parser.parse_log_file()
```