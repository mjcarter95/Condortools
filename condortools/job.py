import os
import time

from collections import OrderedDict

from .utils import Utils
from .logger import Logger
from .parser import Parser


class Job:
    def __init__(self, name, description=None, num_jobs=1):
        '''
        Class representation of a job in HTCondor

        :param name         Name of the job
        :param description  A description of the job, provided as either a dictionary or template object.
                            If empty, it is assumed that the job description file is already provided in
                            the job directory.
        '''


        self.utils = Utils()
        self.utils.create_directory('jobs/{}/logs'.format(name))

        if description:
            assert isinstance(description, dict)
        
        self._name = name
        self._job_dir = '{0}/jobs/{1}'.format(self.utils.cwd, self.name)
        self._description = description or OrderedDict()
        self._num_jobs = int(num_jobs)
        self._updated_at = time.time()
        self._status = 'idle'
        self._cluster = None
        self._description['job_name'] = name
        self._children = {}
        for i in range(num_jobs):
            self._children[i] = {
                'updated_at': time.time(),
                'status_code': None,
                'status': 'idle'
            }
        
        if not os.path.exists(self._job_dir):
            os.makedirs(self._job_dir, exist_ok=True)

        self._parser = Parser('{}/logs/log.log'.format(self._job_dir))

    def __str__(self):
        return '\nname: {self.name}, status: {self.status}, description: {list_attr}'.format(self=self, list_attr=self._list_attributes())

    def __repr__(self):
        return '\nJob(name={self.name}, status={self.status}, description={list_attr})'.format(self=self, list_attr=self._list_attributes())
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description
    
    @property
    def num_jobs(self):
        return self._num_jobs

    @property
    def last_updated(self):
        return self._updated_at
    
    @property
    def status(self):
        return self._status

    @property
    def children(self):
        return self._children
    
    def check_status(self):
        return self.utils.job_status()

    def build_submit_file(self):
        with open('{}/{}.sub'.format(self._job_dir, self.name), 'w') as f:
            for key in self.description:
                if self.description[key] is None:
                    continue

                f.write('{} = {}\n'.format(key, self.description[key]))
            
            f.write('queue {}'.format(self.num_jobs))

        self._updated_at = time.time()

    def build_submit_file_string(self):
        submit_string = ''
        for key in self.description:
            if self.description[key] is None:
                continue
            
            submit_string += '{} = {}\n'.format(key, self.description[key])
        
        submit_string += 'queue {}'.format(self.num_jobs)
        return submit_string

    def submit(self, queue=None, test_submit=False):
        description_file = '{0}/{1}.sub'.format(self._job_dir, self.name)
        self.utils.job_submit(description_file, test_submit=test_submit)
        self._updated_at = time.time()

    def build_submit(self, queue=None):
        self.build_submit_file()
        self.submit(queue=queue)
        self._updated_at = time.time()
    
    def wait(self):
        jobdir = self.description['initialdir'].replace('$(job_name)', self.description['job_name'])
        self.utils.job_wait(self.description['log'].replace('$(initialdir)', jobdir))

    def parse_log_file(self):
        self._parser.parse_log_file()
        event_history = self._parser.event_history
        return event_history

    def update_child_statuses(self):
        event_history = self.parse_log_file()
        updated_at = time.time()
        for job_id in event_history.keys():
            self._children[job_id]['updated_at'] = updated_at
            self._children[job_id]['status_code'] = event_history[job_id]['status_code']
            self._children[job_id]['status'] = event_history[job_id]['status']

    def update_job_status(self):
        idle = []
        error = []
        running = []
        for job_id in self._children.keys():
            if self._children[job_id]['status'] == 'idle':
                idle.append(job_id)
            elif self._children[job_id]['status'] == 'running':
                running.append(job_id)
            elif self._children[job_id]['status'] == 'error':
                error.append(job_id)
        if len(idle) > 0:
            self._status = 'idle'
        elif len(running) > 0:
            self._status = 'running'
        elif len(error) > 0:
            self._status = 'error'
        else:
            self._status = 'complete'

    def update_status(self):
        self.update_child_statuses()
        self.update_job_status()

    def remove(self):
        self._updated_at = time.time()

    def _list_attributes(self):
        attribute_list = []

        for key in self.description:
            attribute_list.append('{} = {}'.format(key, self.description[key]))

        return attribute_list