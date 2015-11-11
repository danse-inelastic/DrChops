# ------------- Modify these -------------
set ( SRC_FILES 
  Ipix2Ixy.cc
  IpixE2IphiE.cc
  Itof2IE_batch.cc
  Universal1DRebinner.cc
  Zt2Zxy.cc
  physics.cc
  readPixelPositions.cc
  )

set ( INC_FILES
  _macros.h
  Event2QE.h
  Event2QE.icc
  Functor.h
  Histogrammer.h
  Ipix2Ixy.h
  Ipix2Ixy.icc
  IpixE2IphiE.h
  IpixE2IphiE.icc
  Itof2IE.h
  Itof2IE_batch.h
  Itof2IE_batch.icc
  ReverseIterator.h
  Universal1DRebinner.h
  Universal1DRebinner.icc
  Zt2Zxy.h
  Zt2Zxy.icc
  events2iqe.h
  exception.h
  findCellIndex.h
  physics.h
  readPixelPositions.h
  solidangle_qe.h solidangle_qe.icc
  tof2E.h
  )

set ( EXPORT_HEADERS ${INC_FILES} )
# ----------------------------------------

# defines
add_definitions(-DUSE_DANSE_NAMESPACE )

# include python headers
include_directories( ${PYTHON_INCLUDE_DIRS} )
include_directories( ${DEPLOYMENT_PREFIX}/include )

# export headers from this project
foreach (header ${EXPORT_HEADERS})
  configure_file(
    "${header}"
    "${CMAKE_CURRENT_BINARY_DIR}/include/${PROJECT_NAME}/${header}"
    )
endforeach (header)

# compile shared lib
add_library ( ${LIB_NAME} SHARED ${SRC_FILES} ${INC_FILES} )

# install headers
install (
  DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME})
# install shared lib
install (TARGETS ${LIB_NAME}
  LIBRARY DESTINATION ${INSTALL_LIB_DIR}
  )
