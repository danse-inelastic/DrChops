// -*- C++ -*-
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//                                   Jiao Lin
//                      California Institute of Technology
//                        (C) 2007  All Rights Reserved
//
// {LicenseText}
//
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//


#ifndef DANSE_REDUCTION_UNIVERSAL1DREBINNER_H
#define DANSE_REDUCTION_UNIVERSAL1DREBINNER_H


#include "Functor.h"


namespace DANSE {

  namespace Reduction {
    
    /// Computes the overlap matrix and multiplies it in one step for each pixel.
    /// This 1D universal rebinner can rebin a 1D histogram I(x) from
    /// one set of bins to another set of bins.
    /// The usefulness of this rebinner is probably best illustrated by 
    /// an example. Suppose we want to rebin I(tof) to I(E).
    /// The original data is a histogram I(tof) with tof bins evenly spaced
    /// in tof axis. To rebin this histogram to I(E), what we can do is
    ///
    /// 1. compute E bin boundaries corresponding to tof bin boundaries.
    ///    The E bin boundaries are not evenly distributed in E axis.
    ///    The histogram on this unevenly-spaced E bins is I'(E)
    /// 2. Now we rebin the I'(E) to I(E), where
    ///    the E bins are evenly spaced. 
    ///
    /// The following docs for this class also use this example to make it 
    /// easier to understand.
    ///
    /// Template parameter:
    ///   InputBinDataType: input axis variable data type (for example: tof's data type)
    ///   InputBinIteratorType: input axis bin iterator (for example: pointer to I(tof)'s tof axis bin boundaries array)
    ///   InputIntensityDataType: input input intensity data type (for example, I(tof)'s intensity array element's data type)
    ///   InputIntensityIteratorType: input intensity iterator (for example: pointer to I(tof)'s intensity data array)
    ///   OutputBinDataType: output axis variable data type( for example: E's data type)
    ///   OutputBinIterator: output axis bin iterator (for example: pointer to I(E)'s E axis bin boundaries array)
    ///   OutputIntensityDataType: output intensity data type (for example: data type of the elements of the I(E)'s intensity data arrays)
    ///   OutputIntensityIteratorType: output intensity iterator (for example: pointer to I(E)'s intensity data array)
    template <
      typename InputBinDataType ,
      typename InputBinIteratorType ,
      typename InputIntensityDataType,
      typename InputIntensityIteratorType,
      typename OutputBinDataType,
      typename OutputBinIteratorType,
      typename OutputIntensityDataType,
      typename OutputIntensityIteratorType
      >  
    class Universal1DRebinner {
      
    public:
      
      /// Parameters:
      ///     inputBBBegin: begin iterator of input bin boundaries (for example, I(tof)'s tof bin boundaries [0])
      ///     inputBBEnd: end iterator of input bin boundaries (for example, I(tof)'s tof bin boundaries [-1])
      ///     inputDataBegin: begin iterator of input intensity array (for example, I(tof)'s I array [0])
      ///     temp_outputBBBegin: begin iterator of temporary output bin boundaries (for example, I'(E)'s energy bin boundaries [0])
      ///     outputBBBegin: begin iterator of output bin boundaries( for example I(E)'s energy bin boundaries [0] )
      ///     outputBBEnd: end iterator of output bin boundaries (for example I(E)'s energy bin boundaries [-1] )
      ///     outputDataBegin: begin iterator of output intensity array (for example, I(E)'s I array [0])
      ///     mapper: functor to map input varaible to output variable (for example, f: tof->E )
      void operator() 
      (InputBinIteratorType inputBBBegin, InputBinIteratorType inputBBEnd,
       InputIntensityIteratorType inputDataBegin,
       OutputBinIteratorType temp_outputBBBegin,
       OutputBinIteratorType outputBBBegin, OutputBinIteratorType outputBBEnd,
       OutputIntensityIteratorType outputDataBegin, 
       Functor<InputBinDataType, OutputBinDataType> & mapper);
      
    }; // end of class Universal1DRebinner
    
  } // Reduction::
} // DANSE::


#define DANSE_REDUCTION_UNIVERSAL1DREBINNER_ICC
#include "Universal1DRebinner.icc"
#undef DANSE_REDUCTION_UNIVERSAL1DREBINNER_ICC


#endif // DANSE_REDUCTION_UNIVERSAL1DREBINNER_H


// version
// $Id: ERebinAllInOne.h 522 2005-07-11 18:45:08Z tim $

// End of file
