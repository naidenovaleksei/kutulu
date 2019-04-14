import sys
from subprocess import Popen, PIPE

class PipeCommunicator():
    def __init__( self, script_name ):
        self.p = Popen(
            [ sys.executable or 'python', script_name ], 
            stdin=PIPE, stdout=PIPE,
            bufsize=0
        )
        self.closed = False

    def push( self, data, answer=True ):
        pipe_stdin = self.p.stdin
        pipe_stdout = self.p.stdout
        answers = []
        for data_chunk in data:
            for line in data_chunk:
                bytes_line = bytes( str(line), 'ascii' )
                pipe_stdin.write(bytes_line + b'\n')
                pipe_stdin.flush()
            if answer:
                answer = pipe_stdout.readline().decode('ascii').strip()
                answers.append( answer )
        return answers

    def close( self ):
        self.p.kill()
        self.p = None
        self.closed = True