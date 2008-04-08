## \page vision_page Vision Statement
## \section rev_sec Major Revisions
##
##  - Inception draft (10/16/06) Jiao Lin First draft
##
## \section intro_sec Introduction 
##
## Reduction is the first thing and sometimes the best thing we do with raw data
## In every experiment. We would like to reduce raw experimental data to a form
## that is easily understandable by people (usually histograms with axes with physical units).
## Every research group might have its own
## ad-hoc reduction software built from fortran/C/IDL/Igor/...
## The goal
## of this reduction software is to provide 
## a flexible, extensible framework for reduction of neutron 
## scattering data.
##
## The goal here is not to simply create a reduction application for a special instrument or
## a special type of instrument, (although it is one of the goals), but mainly to create a
## reduction framework that can be easily extended to support various types of basic 
## reduction procedures. This idea of extensibility should be tested through supporting a few
## instruments.
##
## \section scope_sec Scope
## We define the scope of this reduction software to be
##  - to provide building blocks for developers to create his own reduction components
##    and reduction applications.
##  - to provide an example reduction application so that a process of adapting
##    this reduction software to a new instrument is clear and easy to follow.
##  - The example reduction application will have full capability of
##    reducing inelastic neutron scattering data to S(Q,E) where Q is
##    a scalar. Some manipulations of plots of S(Q,E) will also be
##    provided. The reduction application also generates mslice data files
##    so that single-crystal data can be reduced by exporting mslice
##    data files and analyzing them with
##    <a href="http://www.isis.rl.ac.uk/excitations/mslice/">mslice</a>.
##
##

