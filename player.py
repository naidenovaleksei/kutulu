from pipe_communicator import PipeCommunicator


class BasePlayer:
    def step( self, world_data: dict ):
        pass


class PipePlayer:
    def __init__( self, script_name ):
        self.comm = PipeCommunicator( script_name )
    
    def init( self, world_data ):
        data_list = [
            [ world_data['width'], world_data['height'] ] 
            + world_data['map_grid']
            + [ ' '.join( map(str, world_data['const']) ) ]
        ]
        self.comm.push(data_list, answer=False)


    def step( self, world_data: dict ):
        data_list = [ world_data['entities'] ]
        answers = self.comm.push(data_list)
        return answers[-1]
    
    def finish( self ):
        self.comm.close()