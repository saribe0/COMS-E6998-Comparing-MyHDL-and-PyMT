###########################
## FPGA Project Makefile ##
###########################

all: help

## Global Design Variables ##
DESIGN_PATH 	= $(PWD)
SOURCE_PATH 	= $(DESIGN_PATH)/src
SIM_PATH 	= $(DESIGN_PATH)/sim
SYN_PATH  	= $(DESIGN_PATH)/syn
SCRIPTS_PATH 	= $(DESIGN_PATH)/scripts
SIMTOP 		= tb_sha1
TOP 		= sha1
FAMILY 		= "Cyclone V"
NUM_PROCESSORS  = 2

## Generate list of source files ##
pref 		= --source=
files 		= $(wildcard $(SOURCE_PATH)/*.v)
SOURCE_FILES 	= $(foreach file, $(files), $(pref)$(file))
export SOURCE_FILES

.PHONY: syn clean

help:
	@echo " Synthesize and simulate Verilog/VHDL with Quartus and ModelSim "
	@echo " ============================================================== "
	@echo
	@echo " == Synthesis == "
	@echo
	@echo " make syn 		: Synthesize the currently defined design"
	@echo
	@echo " make clean 		: Cleans everything Quartus related"

sim-compile:
	mkdir -p $(SIM_PATH)
	cd $(SIM_PATH)
	vlib $(SIM_PATH)/WORK
	vmap work $(SIM_PATH)/WORK
	for each in $(wildcard $(SOURCE_PATH)/*.vhd) ; do \
                vcom -quiet $$each ; \
        done
	for each in $(wildcard $(SOURCE_PATH)/*.v) ; do \
		vlog -quiet $$each ; \
	done

sim-gui: sim-compile
	vsim $(SIMTOP)

sim: sim-compile
	vsim -c $(SIMTOP)

syn:
	BUILD_PATH=$(SYN_PATH) TOP=$(TOP) NUM_PROCESSORS=$(NUM_PROCESSORS) FAMILY=$(FAMILY) quartus_sh -t $(SCRIPTS_PATH)/q_syn.tcl

clean:
	-rm *~
	-rm modelsim.ini
	-rm transcript
	-rm $(SOURCE_PATH)/*~
	-rm -rf $(SYN_PATH)
	-rm -rf $(SIM_PATH)
