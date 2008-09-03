

def empty_id( id ):
    return id in [None, 'None', '']


def new_id( director ):
    token = director.idd.token()
    uniquename = '%s' % (token.locator,)
    return uniquename
    
