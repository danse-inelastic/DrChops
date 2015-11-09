# ------------- Modify these -------------
set (SRC_FILES
  __init__.py
  )
# ----------------------------------------

# not needed any more
# setup.py
# set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
# set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
# configure_file("setup.py.in" "setup.py")
# manifest template. need for proper installation
# configure_file("MANIFEST.in" "MANIFEST.in")

# copy all python source over to build directory
foreach (py ${SRC_FILES})
  configure_file(
    "${PROJECT_NAME}/${py}"
    "modules/${PARENT_PATH}/${PROJECT_NAME}/${py}"
    )
endforeach (py)
# message(STATUS "src: ${SRC_PATHS}")

# install
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/modules/
  DESTINATION ${INSTALL_PY_PATH}
  )
