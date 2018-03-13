# COMS-E6998-Comparing-MyHDL-and-PyMTL
COMS E6998 FPGAs Then and Now Project: Comparing two python to verilog conversion packages - MyHDL and PyMTL

## MyHDL
#### Notes
* Open source & free
* Primarily developed by a man named Jan Decaluwe
* Last release in 2015
* Can convert to VHDL or Verilog
* Based on Python generators which model hardware
* Includes classes to get generators and connect them
* Built in simulator on Python interpreter
	* Includes waveform tracing through a VCD file
* Subset convertible to VHDL/Verilog
	* Synthesizable subset is less than convertible
	* Restrictions (convertible and synthesizable) only apply to the generator functions themselves. Outside the functions can use whatever Python they'd like
* Makes a lot of bold claims about "Speed" but bases speed in terms of seconds running the same benchmarks across different programs. He does not discuss the accuracy of the simulations (gate, algorithmic, etc) and the benchmarks seem to be constructed by him. 
	* I'm not sure what the benchmarks show aside from the speed to simulate which could vary for a variety of reasons across compilers
	* He says he cannot name commercial simulators legally... This does not make sense
* Can test generators and MyHDL implementation using pytest / py.test
* If test succeeds, conversion to verilog is as easy as wrapping the design (dut) in a toVerilog() function

#### Support
MyHDL has been around for a while and has the following sources of support:
* Discourse: http://discourse.myhdl.org/ (~ days)
* Gitter: https://gitter.im/jandecaluwe/myhdl (Broken)
* Mailing list: https://sourceforge.net/p/myhdl/mailman/ (Replaced by Gitter/Discourse)
* Archived mailing list: http://gmane.org/
* Freenode Channel #myhdl: https://freenode.net/ (Active in 2016, fizzled out early 2017 via https://botbot.me/freenode/myhdl/)
* GitHub: https://github.com/myhdl/myhdl/issues (~ months)
* Commercial support via the creator
	* Consulting and contract work
	* Per project basis
* Stackoverflow (https://stackoverflow.com/questions/tagged/myhdl?sort=newest&pagesize=50) 26 questions over 7 years. A few each year

#### Documentation
* 6 Examples at http://www.myhdl.org/docs/examples/
* Extensive documentation at http://docs.myhdl.org/en/latest/manual/index.html

#### Setup
```
pip install myhdl
```

Though can also install from source (https://github.com/myhdl/myhdl) </br></br>

Co Simulation requires additional steps found in the github under cosimulation/<platform> </br>
* No documentation is there for modelsim though
* Minimal documentation exists for cver and icarus

## PyMTL
#### Notes

#### Support

#### Documentation

#### Setup


## Resources
http://www.myhdl.org/start/overview.html </br>
https://github.com/cornell-brg/pymtl </br>

