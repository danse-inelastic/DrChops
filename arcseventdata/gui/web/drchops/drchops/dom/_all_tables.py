
main = [
    'Measurement',
    'VanadiumReduction',
    ]

tablemodules = \
             main


tables = []
for t in tablemodules:
    exec 'from %s import %s as table' % (t, t) in locals()
    tables.append( table )
    continue


def children( base ):
    'find child tables of given base'
    r = []
    for table in tables:
        if issubclass( table, base ): r.append( table )
        continue
    return r
