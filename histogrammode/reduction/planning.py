## \page planning_pg Planning Statement
## \section approach_sec Approach
## Since the goal of this reduction software is not for a specific reduction
## task but rather to provide extensible framework in which reduction components
## and reduction applications can be built, we must emphasize much more
## on planniing the structure of this software. The approach we takes is
## to separate functionalities and data structures in layers as cleanly as
## possibe.
##
## \section scope_sec Scope
##
## - In the low-level language we want to only have operations that are numerically intensive.
##   Those numerical operations  should be formalized as abstractly as possible to allow
##   better reusability.
## - In the python level our vision is to provide building blocks of reduction software. 
##   Two data structures need special attention: histogram and instrument. 
##   - Histogram is the fundamental data structure we will use in reduction. 
##    The original experimental data and reduced data can all be represented by 
##    histograms. Python class for histogram should be a container of axes,
##    data, errors, and related meta-data. Numerical operations on histograms 
##    should be easy and fast. Error propagation should be done correctly and 
##    automatically for histograms.
##   - Representation of instrumentation should be easily extensible. 
##    This representation should be able to be used in different ways:
##    in reduction, in simulation, and in creation of visual representation
##    of an instrument. 
##   - In the python level we also want to have methods (operators) to do the real reduction.
##    Those reduction operators take one or more input histograms and transform
##    them to output histograms. We also need operators in python level
##    to handle simple curve fitting, which is commonly useful.
## - In the pyre component level, we want to demonstrate how we can make use
##    of methods in the python level to achieve some specific reduction tasks.
## - In the pyre application level, we want to demonstrate the procedure to
##    assemble pyre components together to create a redution application.
##
## \section roles_drivers_sec Roles & Drivers
##
## - scientist: wants to grab experimental datasets and feed them to reduction application.
##   By specifying some parameters, he should be presented with a nice plot
##   of reduced data. He then can save the data in various forms.
## - framework: wants to handle logging, wants to handle connectivity between
##   reduction pyre components, wants to simplify handling of user configurable items.
## - histogram plotter: wants to plot a histogram
## - reduction application: wants to reduce experimental data to a histogram
## - data readers: wants to read data from hdf5 data file or nexus file or other files
##
## \section risk_sec Risk Mitigation Plan
## - SNS is taking the reduction tasks of all instruments except ARCS, SEQUIOA, and maybe CNCS.
##  Now this framework may only need to fit the need for inelastic group. Or we might want to extend this framework so that it can more easily incorporate the SNS reduction library.
##
## \section phase_sec Phase Plan
