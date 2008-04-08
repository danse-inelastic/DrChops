#!/usr/bin/env python


def convert(old, new):
    import pickle as p
    q,e,s,s1= p.load( open(old) )
    import histogram as h
    spe = h.histogram(
        'S(phi,E)',
        [ ('phi', q),
          ('E', e),
          ],
        data = s.T, errors = s1.T )
    p.dump( spe,  open(new, 'w' ) )
    return


def main():
    import sys
    old = sys.argv[1]
    new = sys.argv[2]
    convert(old, new)
    return

if __name__ == '__main__': main()

