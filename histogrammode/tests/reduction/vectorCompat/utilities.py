

def picklog( target ):
    import journal
    return journal.info( target ).log

def compareFPLists( a, b, tol, log ):
    
    if len(a) != len(b):
        log( "array size is different: %s != %s" % (len(a), len(b) ) )
        return False

    ret = True
    
    for a1,b1 in zip(a,b):
        if abs(a1-b1)>tol: log("%s!=%s" % (a1,b1)); ret = False
        continue

    return ret
