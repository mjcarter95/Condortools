import os
import time
from collections import OrderedDict

from .utils import Utils
from .logger import Logger

'''
------ TO DO -------
1. Handle jobs with children (i.e. num_jobs > 1)
'''

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
        
        self._name        = name
        self._description = description or OrderedDict()
        self._num_jobs    = int(num_jobs)
        self._updated_at  = time.time()
        self._status      = 'idle'

        self._description['job_name'] = name

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
    
    def check_status(self):
        return self.utils.job_status()

    def build_submit_file(self):
        job_dir = '{}/jobs/{}'.format(self.utils.cwd, self.name)

        with open('{}/{}.sub'.format(job_dir, self.name), 'w') as f:
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
        description_file = '{0}/jobs/{1}/{1}.sub'.format(self.utils.cwd, self.name)
        self.utils.job_submit(description_file, test_submit=test_submit)

        self._updated_at = time.time()

    def build_submit(self, queue=None):
        self.build_submit_file()
        self.submit(queue=queue)

        self._updated_at = time.time()
    
    def wait(self):
        self.utils.job_wait(self.description['log'])

    def remove(self):

        self._updated_at = time.time()

    def _list_attributes(self):
        attribute_list = []

        for key in self.description:
            attribute_list.append('{} = {}'.format(key, self.description[key]))

        return attribute_list