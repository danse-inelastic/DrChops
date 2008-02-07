
template <typename T>
void deleteArrayPtr( void * vptr )
{
  T * ptr = static_cast<T *>( vptr );
  delete [] ptr;
}
