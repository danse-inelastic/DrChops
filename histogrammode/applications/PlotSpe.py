#!/usr/bin/env python

def main():
    import sys
    argc = len(sys.argv)

    if argc == 1:
        sys.argv.append( 'spehist.pkl' )
        pass

    from PlotHist import main
    main()
    return


if __name__ == "__main__": main()
    

