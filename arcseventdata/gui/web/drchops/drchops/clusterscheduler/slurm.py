# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


import journal
debug = journal.debug( 'slurm' )



class Scheduler:

    outfilename = 'slurm.out'
    errfilename = 'slurm.err'
    
    def __init__(self, launcher, prefix = None, outputstr_maxlen = 2048,
                 partition = None, node = None):
        self.prefix = prefix
        self.launcher = launcher
        self.outputstr_maxlen = outputstr_maxlen
        self.partition = partition
        self.node = node
        return
    
    
    def submit( self, script ):
        cmd = [ 'sbatch' ]
        if self.partition: cmd.append( '-p %s' % self.partition )
        if self.node: cmd.append( '-w %s' % self.node )
        cmd.append( '-o %s' % self.outfilename )
        cmd.append( '-e %s' % self.errfilename )
        cmd.append(script)
        cmd = ' '.join( cmd )
        
        cmds = [cmd]
        
        failed, output, error = self._launch( cmds )
        debug.log( 'output: %s, error: %s' % (output, error) )
        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg

        id = error.split()[-1]
        return id
    

    def status( self, jobid ):
        
        cmds = [ 'scontrol show job %s' % (jobid,) ]
        failed, output, error  = self._launch( cmds )
        if failed:
            line1 = output.split('\n')[0]
            words = line1.split()
            if len(words) == 4 and words[0] == 'Job' and words[2] == 'not' and \
               words[3] == 'found':
                #job already completed?
                from exceptions import UnableToObtainStatus
                raise UnableToObtainStatus

            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg

        report = self._parseStatusStr( output )
        
        state = report['JobState']
        import time
        start_time = report['StartTime']
        ret = {
            'remote_outputfilename': self.outfilename,
            'remote_errorfilename': self.errfilename,
            'state': _state( state ),
            'timeStart': start_time,
            }

        if ret['state'] == 'finished':
            output, error = self._readoutputerror(
                self.outfilename, self.errfilename )
            ret.update(
                { 'exit_code': report['ExitCode'],
                  'timeCompletion': report['EndTime'],
                  'output': output,
                  'error': error,
                  } )
            pass

        return ret


    def _parseStatusStr(self, s):
        d = {}
        for eq in s.split():
            k,v = eq.split( '=' )
            d[k] = v
            continue
        return d


    def _readoutputerror(self, outputfilename, errorfilename ):
        return self._read( outputfilename ), self._read( errorfilename )


    def _read(self, filename):
        'read file in the remote job directory'
        cmds = [ 'tail %r' % (filename,) ]
        failed, output, error = self._launch( cmds )
        if failed:
            msg = "error in executing cmds %s. output: %s, error: %s" % (
                cmds, output, error )
            raise RuntimeError, msg
        maxlen = self.outputstr_maxlen
        return output[-maxlen+1:]


    def _launch(self, cmds):
        if self.prefix: cmds = [ self.prefix ] + cmds
        return self.launcher( ' && '.join( cmds ) )

    pass # end of Scheduler

import os


_states = {
    'COMPLETED': 'finished',
    'RUNNING': 'running',
    'CANCELLED': 'cancelled',
    'Q': 'queued',
    'E': 'exiting', #after having run
    'H': 'onhold',
    'W': 'waiting',
    'S': 'suspend',
    }
    
def _state( state ):
    r = _states.get( state )
    if r: return r
    return 'unknown state: %s' % state


def test():
    from spawn import spawn
    s = Scheduler( spawn, partition = 'arcs', node = 'arcs2' )
    import tempfile
    tmpsh = tempfile.mktemp(dir=os.path.join( os.path.expanduser('~'), 'tmp' ) )
    f = open(tmpsh, 'wt')
    f.write( '#!/usr/bin/env sh\n' )
    f.write( 'ls\n' )
    f.close()
    del f
    jobid = s.submit(tmpsh)
    while 1:
        status = s.status(jobid)
        print status
        if status is None: break
        state = status['state']
        if state == 'finished': break
    return


def main():
    journal.info( 'spawn' ).activate()
    debug.activate()
    test()
    return


if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
 
