## \page use_cases_page Use Cases
## There are two different types of use cases for reduction
## framework. One is for developers. For developers, reduction
## framework should be easy to work with and to extend.
## The other type is for users of inelastic reduction application.
## For those users, reduction application should be able to
## transform raw data into S(Q,E).
## These two different scenarios are discussed in the following
## two sections.
##
## \section dev_sec For developers
## \subsection dev_si_sec Stakeholders and Interests
##
##   - developers: wants to follow a procedure so that a new
##     reduction application can be easily constructed with existing
##     building blocks in reduction framework
## 
## \subsection dev_suc_sec Main Success Scenerio
##
##   - developer plans to create a reduction application for an instrument
##   - developer identifies major numerical operations and implement
##     using low level language, and exports interface to python
##   - developer creates instrument factory for the specific instrument
##     using instrument elements in reduction software
##   - developer creates measurement classes for all data formats existed
##     for the specific instrument
##   - developer creates reduction pyre components using exported low-level
##     numerical operations and existing reduction building blocks
##   - developer creates reduction application out of reduction pyre components
##
## \section for_user_sec For Users of Inelastic Reduction Application
##
## \subsection sci_si_sec Stakeholders and Interests
##
##   - scientist: wants to reduce raw data to a histogram, wants to have a plot
##     of the histogram, wants to manipulate the plot a little bit to create
##     a publishable figure, wants to convert reduced data to some form more
##     familiar to him, like 3 col ascii or mslice data files.
##
## \subsection sci_suc_sec Main Success Scenerio
##
##   - Scientist starts the reduction application script
##   - Framework begins application life-cycle
##   - A reduction GUI presents
##   - Scientist clicks the configure button and input parameters needed
##     for reduction
##   - Scientist clicks the run button and reduction runs and a plot
##     is generated for reduced data
##   - Scientist starts histogram GUI to manipulates the reduced data
##   - Scientist improves the look of the plot and saves the plot to a
##     image file
##   - Scientist converts the data to some form more familiar to him
##     by clicking buttons

