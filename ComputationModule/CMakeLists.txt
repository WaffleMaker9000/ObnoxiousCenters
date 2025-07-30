cmake_minimum_required(VERSION 3.10)
project(ComputationModule)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable debug symbols
set(CMAKE_BUILD_TYPE Debug)

# Add source files
set(SOURCES
    src/main.cpp
    src/solver.cpp
    src/sort.cpp
)

# Add header files
set(HEADERS
    src/solver.h
    src/sort.h
)

# Create executable
add_executable(compModule ${SOURCES} ${HEADERS})

# Add include directories
target_include_directories(compModule PRIVATE src)

# Set output directory
set_target_properties(compModule
    PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
