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


#ifndef DANSE_REDUCTION_REVERSEITERATOR_H
#define DANSE_REDUCTION_REVERSEITERATOR_H


namespace DANSE {
  
  /// Create a iterator out of an existing iterator, but the iteration
  /// will be in reversed direction.
  ///
  /// template parameters:
  ///    Iterator: original iterator's type
  ///    ValueType: original iterator's dereference (data) type
  template <typename Iterator, typename ValueType>
  class ReverseIterator {
  public:
    /// default ctor.
    /// Default constructor. The object is not really initialized becuase
    /// it is set to zero.
    ReverseIterator () : m_it(0) {}
    
    /// copy ctor.
    /// Create a copy of existing ReverseIterator object.
    ReverseIterator ( const ReverseIterator< Iterator, ValueType> & rhs ) 
      : m_it ( rhs.m_it ) {}
    
    /// ctor.
    /// Main constructor. Create a reversed iterator out of an existing iterator.
    ReverseIterator (Iterator it) 
      : m_it( it )
    {
    };
    
    // type alias
    typedef ReverseIterator<Iterator, ValueType> mytype;
    
    /// operator = .
    /// assignment
    const mytype & operator= ( const mytype & rhs )
    {
      m_it = rhs.m_it;
      return *this;
    }
    
    /// operator + .
    /// add an offset 
    ReverseIterator<Iterator, ValueType> operator+(int n)
    {
      ReverseIterator ret(m_it - n );
      return ret;
    }
    
    /// operator - .
    /// subtract an offset
    ReverseIterator<Iterator, ValueType> operator-(int n)
    {
      ReverseIterator ret(m_it + n );
      return ret;
    }
    
    /// operator - .
    /// calculate difference (distance) between two iterators
    int operator-(const ReverseIterator & rhs) const
    {
      return rhs.m_it - m_it;
    }
    
    /// operator ++it .
    /// increment the iterator and return the incremented iterator
    ReverseIterator<Iterator, ValueType> & operator++()
    {
      m_it --;
      return *this;
    }
    
    /// operator it++ .
    /// increment the iterator, but return a copy of the original unincremented iterator
    ReverseIterator<Iterator, ValueType> operator++(int)
    {
      ReverseIterator temp(m_it);
      m_it --;
      return temp;
    }
    
    /// opereator --it .
    /// decrement the iterator and return the decremented iterator
    ReverseIterator<Iterator, ValueType> & operator--()
    {
      m_it ++;
      return *this;
    }
    
    /// operator it-- .
    /// decrement the iterator, but return a copy of the origdeal undecremented iterator
    ReverseIterator<Iterator, ValueType> operator--(int)
    {
      ReverseIterator temp(m_it);
      m_it ++;
      return temp;
    }
    
    /// operator * .
    /// dereference.
    ValueType operator*() const
    {
      return *m_it;
    }
    
    /// operator == .
    /// compare two iterators.
    bool operator==(const ReverseIterator & rhs) const
    {
      return (m_it==rhs.m_it);
    }
    
    /// operator != .
    /// compare two iterators.
    bool operator!=(const ReverseIterator & rhs) const
    {
      return !(m_it == rhs.m_it);
    }
    
    /// operator < .
    /// compare two iterators. 
    bool operator<(const ReverseIterator & rhs) const
    {
      return (m_it > rhs.m_it);
    }
    
    /// operator > .
    /// compare two iterators. 
    bool operator>(const ReverseIterator & rhs) const
    {
      return (m_it < rhs.m_it);
    }
    
    /// print this iterator.
    /// This is for implementation of ostream << .
    void print( std::ostream & os ) const
    {
      os << "reverse iterator of " << m_it;
    }
    
  private:
    Iterator m_it;
  };
  
} // DANSE::


/// ostream << ReverseIterator object
template <typename Iterator, typename ValueType>
std::ostream & operator << 
( std::ostream & os, const DANSE::ReverseIterator<Iterator, ValueType> & it)
{
  it.print(os);
  return os;
}

#endif // DANSE_REDUCTION_REVERSEITERATOR_H


// version
// $Id$

// End of file 
