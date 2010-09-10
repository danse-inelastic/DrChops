#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                  Jiao Lin
#                        California Institute of Technology
#                          (C) 2007  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


'''base class for histogrammers that can parallely

limitations:
 * must run on a filesystem that is common to all nodes

'''


import journal
info = journal.info('histogrammer')
warning = journal.warning('ParallelHistogrammer')


from ParallelComponent import ParallelComponent

class ParallelHistogrammer(ParallelComponent):

    def __call__( self, eventdatafiles_or_filename, nevents, *args):
        '''histogram event data in the given list of event data files

        eventdatafiles_or_filename: a list of event data files or one filename string
        nevents: number of total events to histogram. if None, then all events in all files will be histogrammed
        *args: addtional arguments for initializing this histogrammer

        return: a histogram
        '''
        if isinstance(eventdatafiles_or_filename, str):
            eventdatafiles = [eventdatafiles_or_filename]
        else:
            eventdatafiles = eventdatafiles_or_filename
        
        mpiRank = self.mpiRank
        mpiSize = self.mpiSize

        # logging
        if mpiRank == 0:
            info.log( "eventdatafilename = %s" % eventdatafiles )
            pass

        # partition the load
        eventsourcecollection = self._getLoad(eventdatafiles, nevents)
        
        # initialize this histogrammer
        self.setParameters(*args)

        # process 
        for eventsource in eventsourcecollection:
            info.log('node %d: histogramming %s events from %s...' % (mpiRank, eventsource.size, eventsource))
            events = eventsource.getAll()
            h = self._processEvents(events)
            continue
        info.log('node %d: histogramming done' % (mpiRank, ))

        # send the histogram to the master node
        #  mpi comm channel
        tag = 100
        #  some data
        data = h.data().storage().asNumarray()
        shape = data.shape
        datatype = data.dtype
        from numpy import fromstring

        #  send/receive
        if mpiRank > 0:
            info.log( "%s: sending histogram to master node..." % mpiRank )
            s = data.copy().tostring()
            self.mpiSendStr( s, 0, tag )
            info.log( "%s: histogram sent to master node." % mpiRank )
            return

        for i in range(1, mpiSize):
            datastr = self.mpiReceiveStr( i, tag)
            if len(datastr) == 0:
                raise RuntimeError, 'data string received from node %s is empty. tag = %s' %( i, tag ) 
            data = fromstring(datastr, datatype)
            data.shape = shape
            info.log( "received histogram from node %d" % i )
            h.data().storage().asNumarray()[:] += data
            info.log( "added histogram from node %d into that of node 0" % i )
            continue

        # set error bar squares to be equal to counts
        h.errors().storage().asNumarray()[:] = h.data().storage().asNumarray()

        import os
        info.log( "times: %s" % str(os.times()) )
        return h


    def _getLoad(self, eventdatafiles, nevents):
        'figure out how much load this node need to work on'
        mpiSize = self.mpiSize
        mpiRank = self.mpiRank
        
        tag = 700
        if mpiRank == 0:
            eventsource_for_nodes = partition(eventdatafiles, mpiSize, nevents)
            
            # event source collection for master node
            eventsourcecollection = eventsource_for_nodes[0]

            # send event source collection to each node
            for node in range(1, mpiSize):
                # the load for the node
                t = eventsource_for_nodes[node]
                # send
                self.mpiSend(t, node, tag)
                continue
        else:
            # receive partition result from master node
            eventsourcecollection = self.mpiReceive(0, tag)
        return eventsourcecollection
    

    def _readInstrumentInfo(self, ARCSxml, keys=None):
        info.log('reading instrument info')
        mpiRank = self.mpiRank
        mpiSize = self.mpiSize
        if mpiRank == 0:
            from arcseventdata import getinstrumentinfo
            allinfos = getinstrumentinfo(ARCSxml)
            # only keep the necessary ones
            infos = {}
            if keys is None:
                keys = [
                    'detector-system-dimensions',
                    'moderator-sample distance',
                    'pixelID-position mapping binary file',
                    'detector axes',
                    ]
            for k in keys: infos[k] = allinfos[k]
            del allinfos

        #  send/receive
        tag =999
        if mpiRank == 0:
            info.log( "%s: sending infos to all nodes..." % mpiRank )
            for node in range(1, mpiSize):
                self.mpiSend(infos, node, tag)
        else:
            info.log( "%s: receiving infos..." % mpiRank )
            infos = self.mpiReceive(0, tag)
            
        return infos
    

    def _processEventSourceCollection(self, events_collection):
        '''process a list of events. each item is a tuple of (events, nevents)
        '''
        for events, nevents in events_collection:
            self._processEvents(events, nevents)
            continue
        return


    def _processEvents(self, events):
        '''process the given events. the number of events is given as "nevents"

        This method must be called after the method setParameters being called.
        '''
        raise NotImplementedError


    def setParameters(self, *args, **kwds):
        '''initialize this histogrammer with parameters for histogramming.
        the args and kwds really depends on the type of the histogrammer 
        '''
        raise NotImplementedError


    pass # end of ParallelHistogrammer
    


def partition(files, n, ntotal=None):
    '''partition the given event files into n parts. each part roughly have the
    same number of events. 

    ntotal: optional. total number of events. defaults to the total number of events in 
            all the event files.

    return: a list of EventSource(EventsFromFile) instances
    '''
    import arcseventdata, math
    nevents_array = [arcseventdata.getnumberofevents(f) for f in files]
    if ntotal is None:
        ntotal = sum(nevents_array)
    nevents_per_node = int(math.ceil(ntotal*1./n))
    nfiles = len(files)
    
    ret = []; cursor = 0; fileno = 0; ntotal_allocated = 0
    for i in range(n):
        # a new event collection for node i
        ec = EventSourceCollection(); ret.append(ec)
        # 
        if ntotal - ntotal_allocated > nevents_per_node:
            nevents_for_this_node = nevents_per_node
        else:
            nevents_for_this_node = ntotal - ntotal_allocated
        ntotal_allocated += nevents_for_this_node

        # continue adding events to the collection until it has enough events
        while ec.nevents < nevents_for_this_node and fileno < nfiles:
            # the current event file
            filename = files[fileno]
            # the total # of events in the file
            n = nevents_array[fileno]
            # if the events left in the file is not enough or just enough
            if n-cursor <= nevents_for_this_node - ec.nevents:
                # we need to add all the left to the collection
                events = EventsFromFile(filename, cursor, n)
                ec.append( events )
                # and set the cursor and the fileno
                cursor = 0; fileno += 1
                continue
            else:
                # otherwise we need to add a chunk in the file to collection
                chunksize = nevents_for_this_node - ec.nevents
                events = EventsFromFile(filename, cursor, cursor+chunksize)
                ec.append( events )
                # increment cursor
                cursor += chunksize
                # and move on to the next node
                break
        
        continue

    return ret


class Events:

    '''data object wraps a c pointer to an events array

    ptr: the c pointer
    n: number of events
    source: the origin of the events. an instance of EventSource
    '''

    def __init__(self, ptr, n, source):
        '''
        '''
        self.ptr = ptr
        self.n = n
        self.source = source
        return



class EventSource(object):
    
    '''abstract base class of event source
    '''
    
    size = None

    def getAll(self):
        "get all events"
        raise NotImplementedError
    
    pass


class EventsFromFile:
    
    '''an event source that comes from a event data file
    '''

    def __init__(self, filename, start, end):
        self.filename = filename
        self.start = start
        self.end = end
        self.size = self.end-self.start
        return


    def getAll(self):
        import arcseventdata
        ptr, n = arcseventdata.readevents(self.filename, self.size, self.start)
        return Events(ptr, n, self)


    def __repr__(self):
        return '%s [%s:%s]' % (self.filename, self.start, self.end)
        


class EventSourceCollection(list):

    def __init__(self):
        super(EventSourceCollection, self).__init__()
        self.nevents = 0
        return
        

    def append(self, eventsource):
        self.nevents += eventsource.size
        super(EventSourceCollection, self).append(eventsource)
        return
    
    pass # end of EventSourceCollection
        


# version
__id__ = "$Id$"

#  End of file 
