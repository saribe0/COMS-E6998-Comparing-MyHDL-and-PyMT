########################################
## Quartus Script to Create a Project ##
########################################

if {[info exists env(FAMILY)]} {
    set FAMILY $env(FAMILY)
    puts "INFO: Synthesizing for ${FAMILY}"
} else {
    puts "ERROR: Missing device family definition"
    exit -1
}

if {[info exists env(TOP)]} {
    set TOP $env(TOP)
    puts "INFO: Creating a project for ${TOP}"
} else {
    puts "ERROR: Missing top level design definition"
    exit -1
}

if {[info exists env(SOURCE_FILES)]} {
    set SOURCE_FILES $env(SOURCE_FILES)
} else {
    puts "ERROR: Source files not defined"
    exit -1
}

# Enter the build path
file mkdir $env(BUILD_PATH)
cd $env(BUILD_PATH)

# Create the project
project_new -family ${FAMILY} ${TOP} -overwrite

# Set the number of processors if it's defined
if {[info exists env(NUM_PROCESSORS)]} {
    set fo [open ${TOP}.qsf a]
    puts $fo "\nset_global_assignment -name NUM_PARALLEL_PROCESSORS $env(NUM_PROCESSORS)"
    close $fo
}

# Execute synthesis
qexec "quartus_map ${TOP} ${SOURCE_FILES}"

# Fit the design
qexec "quartus_fit ${TOP}"

# Analyze timing
qexec "quartus_sta ${TOP}"

