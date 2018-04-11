########################################
## Quartus Script to Create a Project ##
########################################

if {[info exists FAMILY]} {
    puts "\nINFO: Synthesizing for ${FAMILY}\n"
} else {
    puts "\nERROR: Missing device family definition\n"
#    exit -1
}

if {[info exists env(TOP)]} {
    set TOP $env(TOP)
    puts "\nINFO: Creating a project for ${TOP}\n"
} else {
    puts "\nERROR: Missing top level design definition\n"
    exit -1
}

if {![info exists BUILD_PATH]} {
    set BUILD_PATH "./prj"
}

# Enter the build path
file mkdir ${BUILD_PATH}
cd ${BUILD_PATH}

puts $env(SOURCE_FILES)

#project_new -family ${DEVICE_FAMILY} ${PROJECT}
project_new ${TOP} -overwrite

qexec "quartus_map ${TOP} $env(SOURCE_FILES)"
