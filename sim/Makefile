###########################
## FPGA Project Makefile ##
###########################

all: help

## Global Design Variables ##
DESIGN_PATH 	= $(PWD)
SOURCE_PATH 	= $(DESIGN_PATH)/src
BUILD_PATH  	= $(DESIGN_PATH)/prj
SCRIPTS_PATH 	= $(DESIGN_PATH)/scripts
SIMTOP 		= testbench
TOP 		= regi
FAMILY 		= fam

pref 		= --source=
files 		= $(wildcard $(SOURCE_PATH)/*)
SOURCE_FILES 	= $(foreach file, $(files), $(pref)$(file))
export SOURCE_FILES

help:
	@echo " Synthesize and simulate Verilog/VHDL with Quartus and ModelSim "
	@echo " ============================================================== "
	@echo
	@echo " == Synthesis == "
	@echo
	@echo " make syn 		: Synthesize the currently defined design"
	@echo
	@echo " make clean 		: Cleans everything Quartus related"


syn:
	BUILD_PATH=$(BUILD_PATH) TOP=$(TOP) FAMILY=$(FAMILY) quartus_sh -t $(SCRIPTS_PATH)/q_syn.tcl


clean:
	rm *~
	rm $(BUILD_PATH)/*
