

def newmask( detaxes ):
    mask = H.histogram( 'mask', detaxes, data_type = 'int' )
    return mask


def maskbadtubes( mask, ipdp, lowerlimit = None, upperlimit = None ):
    f = FindBadTube(lowerlimit = lowerlimit, upperlimit = upperlimit)
    f( mask, ipdp )
    return mask


class FindBadTube:

    def __init__(self, lowerlimit=None, upperlimit=None):
        self.lowerlimit = lowerlimit
        self.upperlimit = upperlimit
        return

    def __call__(self, mask, ipdp):
        if self.lowerlimit:
            black = ipdp.I < self.lowerlimit
            mask.I[ black ] = 1

        if self.upperlimit:
            red = ipdp.I > self.upperlimit
            mask.I[ red ] = 1
        return


import histogram as H
