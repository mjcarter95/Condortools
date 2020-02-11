import os

class Utils:
    def __init__(self, working_dir=os.getcwd()):
        self._cwd = working_dir
    
    @property
    def cwd(self):
        return self._cwd
    
    @cwd.setter
    def cwd(self, cwd):
        self._cwd = cwd
    
    def create_directory(self, dir):
        if not os.path.isdir('{}/{}'.format(self.cwd, dir)):
            os.mkdir('{}/{}'.format(self.cwd, dir))

    def submit(self, executable, args):
        return