#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                                   Jiao Lin
#                        California Institute of Technology
#                          (C) 2006  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



## \mainpage Data Reduction for Neutron Scattering
##
## First let us define two words here to clear possible confusion. We define
## "reduction software" as a collection of packages that we created for the purpose
## of reducing data; and we define "reduction package" as one particular package in the
## "reduction software".
##
## \section intro_sec Introduction
## 
## reduction is a procedure to transform measured raw histogram to a form which is more easily
## understandable for scientists. This procedure usually consists of conversion of a
## histogram 
## measured in a dimension to another dimension that is more physically meaningful (
## an example of which would be converting time-of-flight to neutron energy ) and/or
## conversion of multidimensional data to lower dimension (an example of which is
## intensity measured in an area detector sometimes can be binned into "rings" in 
## case of powder sample).
##
## \subsection hist_sec Histogram
## To further this discussion, we need to first clearly define what do we mean here by
## "histogram". The result of any measurement is actually a histogram, by which we mean
## we have data in some bins. For example, if we measure a spectrum as a function of
## time-of-flight, we will get an array of counts, while each element in that array represents
## the number of counts measured in a predefined time slot (bin).
## This array of counts can be approximated by
##
##   \f$ \frac{dI}{dx}(x) \Delta x \f$
##
## where \f$\frac{dI}{dx}\f$ is a density function and \f$ \Delta x \f$ is bin size.
## This observation
## forms the base of our design of 
##  <a href="../../../histogram/histogram/html/index.html"> histogram </a>
## classes.
##
## \subsection math_sec A little math
## With a definition of histogram, we now go back to reduction.
## The two conversions mentioned above are two operations that are very common in reduction
## procedure. The first conversion requires 
##
##   \f$ \frac{dI}{dx}(x) \Delta x --> \frac{dI}{dy}(y) \Delta y \f$
##
## where \f$\Delta x\f$ and \f$\Delta y\f$ are bin sizes of the old and new bins.
## This conversion can be easily done if we remember
##
##   \f$ \frac{dI}{dx}(x) dx = \frac{dI}{dy}(y) dy \f$
##
## and if we know the mapping relation between variable x and y
##
##   \f$ y = f(x) \f$ \anchor yfx (1)
##
## The second operation is essentailly
##
##   \f$ \frac{dI}{dx_1 dx_2...dx_n} (x_1,x_2,...,xn) \Delta x_1 \Delta x_2 ... \Delta xn  ->   \frac{dI}{dy_1 dx_3...dx_n} (y_1,x3,...,xn) \Delta y_1 \Delta x3 ... \Delta xn \f$
##
## where \f$y_1\f$ is a function of \f$x_1\f$,\f$x_2\f$:
##
##   \f$ y_1 = f(x_1,x_2) \f$  \anchor y_1fx_1x_2 (2)
##
## And this conversion would need an integration
##
##   \f$ \int_{f(x_1,x_2)=y} dx_1 dx_2 \frac{dI}{dx_1 dx_2...dx_n} (x_1,x_2,...,xn)  ->  dy_1 \frac{dI}{dy_1 dx_3...dx_n} (y_1,x3,...,xn) \f$
##
## These two operations are computation intensive and are implemented in c++ layer and exported
## to python.
##
## \subsection instr_sec Instrument 
## Having dealt with all the "hard" math, we are back with "simple" stuff (They are simple
## in math, but not as simple in other aspects).
##
## To do operations mentioned in \ref math_sec, we need to know the relations like
## \ref yfx "(1)" and \ref  y_1fx_1x_2 "(2)".
## For example, in direct-geometry time-of-flight instrument,
## to convert time of flight to neutron energy, we need to know the length
## of the flight path, and the time at which neutron hit the sample.
## The positions of sample and detectors are clearly necessary inputs for reduction
## procedure. Therefore, we need information of the instrument in which the
## to-be-reduced histogram is measured. The 
##  <a href="../../../instrument/instrument/html/index.html"> instrument </a>
## deals with this problem.
##
## \subsection measurement_sec Measurement
## Now we introduce a little more complexity. A successful measurement usually consists of
## several runs:
##  - a run for the sample you are interested in
##  - a run for the empty sample can
##  - a run to calibrate detector efficiency
##
## Each run results in one or more histograms (one main dataset,
## plus other accompanying datasets, like beam 
## monitor dataset).
##
## We build the 
##  <a href="../../../measurement/measurement/html/index.html"> measurement </a>
## package to handle these. It will provide all histograms needed in the reduction
## procedure.
##
## \section Design_sec Design
## As mentioned in the \ref intro_sec, several packages are involved in our reduction
## software. There are four "central" packages:
##
##  - <a href="../../../histogram/histogram/html/index.html"> histogram </a>: fundamental data structure
##  - <a href="../../../instrument/instrument/html/index.html"> instrument </a>: instrument information
##  - <a href="../../../measurement/measurement/html/index.html"> measurement </a>: provide histograms
##  - <a href="../../../reduction/reduction/html/index.html"> reduction </a>: reduction methods
##
## And there are other supporting packages:
##
##  - <a href="../../../nx5/nx5/html/index.html"> nx5 </a>: "nexus" readers/(writers) based on hdf5fs
##  - <a href="../../../hdf5fs/hdf5fs/html/index.html"> hdf5fs </a>: a tool to create/read/write hdf5 files by treating a hdf5 file as a
##            filesystem with trees of directories and files
##  - <a href="../../../stdVector/stdVector/html/index.html"> stdVector </a>: python binding to c++ std::vector template
##  - <a href="../../../array_kluge/array_kluge/html/index.html"> array_kluge </a>: tools to manipulate c arrays
##
## Relationship among those packages can be illustrated by the following package diagram
##
## \image html reduction-package-diagram.png
##
## \subsection design_issues_sec Design issues
##
## \subsubsection error_prop_sec Error propagation
##
## Reduction components always propagate errors. Error propagtion happens in
## all histogram operatorions like + - * /
##
## IMPORTANT POINT: The error arrays in histograms are always assumed to contain
## the squares of errors. That's because constantly squaring and square-rooting
## data is not only redundant, it will thrash your numerical precision. It is
## up to the user (which may be other programmers) to take square roots as
## appropriate (for instance, when plotting an intermediate result, or writing
## a final result to disk).
##
## \section redpkg_sec reduction package
## This section is about the particular reduction package inside the reduction software.
##
## The reduction package is carefully separated to several layers to ensure a clean design.
##
## "c/c++" layer is responsible for intensive computations only feasible to be implemented
## in low level language. For example, this layer includes a class ERebinAllInOne to
## rebin data in tof bins to data in evenly-spaced energy bins.
##
## "python vector compatible" layer vectorCompat is the joint point between c++ and python.
## All c++ codes are implemented to deal with "vector"-like objects, e.g., energy bins.
## The vectorCompat python package accepts vector arguments and call the corresponding
## c++ methods to do the real work. This layer separate other python layers from c++ codes and
## python bindings.
##
## "python histogram compatible" layer histCompat allows developers to deal with objects with
## more physics meanings. This layer is built on top of the vectorCompat layer. A
## <a href="../../../histogram/histogram/html/index.html"> histogram </a>
## is an object consisting of axes and datasets and meta data. In the histCompat layer,
## histograms are our focus. Classes in this layer  take histograms instead of vectors
## as arguments,
## and implementations of those classes decompose histograms to vectors and call the
## corresponding methods in the vectorCompat layer.
##
## "pyre vector compatible" layer pyreVC wraps classes in vectorCompat layer to pyre components.
## There should not be many of this kind of components because we should be dealing
## more with histograms in the pyre layer
##
## "pyre histogram compatible" layer pyreHC wraps classes in histCompat layer to
## pyre components.
##
## "pyre" layer reduction.pyre makes use of pyre components in pyreVC and pyreHC and implement
## classes that are more high-level. The pyreVC and pyreHC layers are more concerned
## with low-level operations like "rebin to evenly-spaced energy bins" and
## "fit a curve to gaussian and find the center". The pyre layer is more concerned
## with "calculate calibration constants out of calibration data" and
## "reduce I(det, pix, tof) to S(phi,E)
##
## This layered structure may be illustrated by the following figure (it is far from complete,
## and only shows a part of the whole structure):
##
## \image html reduction-package-layers.png
##
## \section apps_sec reduction applications
## reduction components in this package is assembled together to create reduction applications.
## Details of them are in reduction.applications.
##
## \section contact_sec Contact
## This reduction software is developed by the DANSE/INS development team.
## Please contact Jiao Lin (linjiao@caltech.edu) for any questions.
##
## \section ack_sec Acknowledgement
## This software is supported by DOE Grant No DE-FG02-01ER45950
##


def copyright():
    return "reduction pyre module: Copyright (c) 1998-2004 Michael A.G. Aivazis";


# version
__id__ = "$Id: __init__.py 1256 2007-05-07 23:09:08Z linjiao $"

#  End of file 
