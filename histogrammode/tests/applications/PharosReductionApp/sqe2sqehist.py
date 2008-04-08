#!/usr/bin/env python


def convert(old, new):
    import pickle as p
    q,e,s,s1= p.load( open(old) )
    import histogram as h
    sqe = h.histogram(
        'S(Q,E)',
        [ ('Q', q),
          ('E', e),
          ],
        data = s.T, errors = s1.T )
    p.dump( sqe,  open(new, 'w' ) )
    return


def main():
    import sys
    old = sys.argv[1]
    new = sys.argv[2]
    convert(old, new)
    return

if __name__ == '__main__': main()

