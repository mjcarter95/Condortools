import os
import subprocess

class Utils:
    def __init__(self, working_dir=os.getcwd()):
        self._cwd = working_dir
        self._module_dir = os.path.dirname(os.path.realpath(__file__))
    
    @property
    def cwd(self):
        return self._cwd
    
    @cwd.setter
    def cwd(self, cwd):
        self._cwd = cwd
    
    @property
    def module_dir(self):
        return self._module_dir
    
    def create_directory(self, dir):
        if not os.path.isdir('{}/{}'.format(self.cwd, dir)):
            os.mkdir('{}/{}'.format(self.cwd, dir))

    def remove_directory(self, dir):
        if os.path.isdir('{}/{}'.format(self.cwd, dir)):
            os.rmdir('{}/{}'.format(self.cwd, dir))

    def job_status(self):
        ''' TO DO ONCE LOG PARSER COMPLETE '''
        return

    def job_submit(self, job_description, test_submit=False):
        command = 'condor_submit'

        if test_submit:
            args = ['--no_submit', job_description]
        else:
            args = [job_description]
        
        self._execute(command, args)

    def job_wait(self, log_dir):
        command = 'condor_wait'
        args = [log_dir]
        self._execute(command, args)

    def job_hold(self, job_id):
        command = 'condor_hold'
        args = [job_id]
        self._execute(command, args)

    def job_remove(self, job_id):
        command = 'condor_rm'
        args = [job_id]
        self._execute(command, args)
    
    def _execute(self, command, args):
        '''
        Execute a shell command using subprocess

        :param command the command you want to execute
        :param args    a list of arguments
        '''

        subprocess_args = [command]

        for arg in args:
            subprocess_args.append(str(arg))

        try:
            print('\n[LOGGING] Executing command {}'.format(subprocess_args))
            list_files = subprocess.run(subprocess_args, stdout=subprocess.DEVNULL)

            print('\n[LOGGING] Exit code: {}'.format(list_files.returncode))
        
        except Exception as e:
            print('\n{}'.format(e))