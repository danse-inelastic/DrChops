

def empty_id( id ):
    return id in [None, 'None', '']


def new_id( director ):
    token = director.idd.token()
    uniquename = '%s' % (token.locator,)
    return uniquename
    

arcs_run_root = '/ARCS-DAS-FS'
def find_arcs_run_dir( runno ):
    import os
    cmd = 'find %s -name ARCS_%s' % (arcs_run_root, runno)
    p = os.popen( cmd )
    lines = p.readlines()
    if len(lines) != 1: return None
    return lines[0].strip()

