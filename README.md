# COMS-E6998-Comparing-MyHDL-and-PyMTL
COMS E6998 FPGAs Then and Now Project: Comparing two python to verilog conversion packages - MyHDL and PyMTL

## Benchmark Thoughts
* Could use ISCAS '85, ISCAS '89, ITC/ISCAS '99, 74X from http://pld.ttu.ee/~maksim/benchmarks/
* Maybe AES ECB from https://github.com/secworks/aes

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

#### Setup (Assumed a fresh install of Ubuntu 16.04 w/ Python 2.7 and pip installed)
```
pip install myhdl
```

Though can also install from source (https://github.com/myhdl/myhdl) </br></br>

Co Simulation requires additional steps found in the github under cosimulation/<platform> </br>
* No documentation is there for modelsim though
* Minimal documentation exists for cver and icarus

## PyMTL
#### Notes
* Open source and free
* Developed at Cornell
* Last release in 2015 (alpha), no active branches
	* Funding from the National Science Foundation
	* Looks like funding has dried out or contributers have graduated
* PyMTL (or at least a tutorial for it) was developed or senior/grad level course in computer architecture
	* Build a basic multicore cpu and simulate running programs on it
* Uses Verilator for translation to Verilog and Verilog imports
* Unlike MyHDL, PyMTL allows users to integrate new PyMTL code with Verilog though the use of Verilator and wrappers written in PyMTL
	* This is done through using Verilator to compile the verilog to C++ 
	* The PyMTL wrapper serves as a way to include it in other PyMTL files while all the real computation happens in the Verilog file
	* If the Verilog code is more complex, PyMTL has an interface for generating your own wrapper from scratch without using the built in wrapper
* Many of their examples and tutorials followed a C++ flow first and then used PyMTL as the testbench

#### Support
* GitHub: https://github.com/cornell-brg/pymtl/issues (Active until Oct. 2016, nothing since)
* Could not find any other support sites

#### Documentation
* GitHub: https://github.com/cornell-brg/pymtl
* Publication: http://ieeexplore.ieee.org/document/7011395/ 
* Tutorials:
	* https://github.com/cornell-brg/pymtl-tut-hls
	* https://github.com/cornell-ece4750/ece4750-tut3-pymtl
	* https://github.com/cornell-ece5745/ece5745-sec-pymtl-cl
	* http://www.csl.cornell.edu/courses/ece5745/handouts/ece5745-tut-asic-new.pdf
	* http://www.csl.cornell.edu/courses/ece4750/handouts/ece4750-tut3-pymtl.pdf

Documentation is primarily contained in the GitHub repository inside /docs/. It includes two how-tos on how to write pythonic code with PyMTL and how to integrate with existing verilog designs through the use of a wrapper.

#### Setup (Assumed a fresh install of Ubuntu 16.04 w/ Python 2.7 and pip installed
PyMTL seems to be much more challenging to setup as it requires a whole host of libraries:
* Verilator (Verilog translation and imports - must be from source correct version)
	* Newest version is 3.920 (2/2018)
	* Version in documentation is 3.876 ()
* pkg-config (To interface w/ Verilator)
* Python headers - python-dev (Needed for cffi package in order to call C code generated by Verilator)
* libffi - libffi-dev (Needed for cffi package in order to call C code generated by Verilator)
* [Recommended] virtualenv (For virtualized python enviroment)

From the GitHub page this equates to:

```
sudo apt-get install git make autoconf g++ flex bison
mkdir -p ${HOME}/src
cd ${HOME}/src
wget http://www.veripool.org/ftp/verilator-3.876.tgz
tar -xzvf verilator-3.876.tgz
cd verilator-3.876
./configure
make
sudo make install
```
The installation can optionally be verified with:
```
cd $HOME
which verilator
verilator --version
```
Next, install pkg-config:
```
sudo apt-get install pkg-config
```
And verify it can find Verilator:
```
pkg-config --print-variables verilator
```
Next install the other packages (for me, this only added libffi-def as git was installed above and python-dev was already installed):
```
sudo apt-get install git python-dev libffi-dev
```
I chose to use virtualenv as they do in their instructions so that meant:
```
sudo apt-get install python-virtualenv
```
to install and:
```
mkdir ${HOME}/venvs
virtualenv --python=python2.7 ${HOME}/venvs/pymtl
source ${HOME}/venvs/pymtl/bin/activate
```
to check the installation. </br>
</br>
After all the prerequisites, PyMTL is installed like:
```
mkdir -p ${HOME}/vc/git-hub/cornell-brg
cd ${HOME}/vc/git-hub/cornell-brg
git clone https://github.com/cornell-brg/pymtl.git
pip install --editable ./pymtl
```
The installation can then be tested with:
```
mkdir -p ${HOME}/vc/git-hub/cornell-brg/pymtl/build
cd ${HOME}/vc/git-hub/cornell-brg/pymtl/build
py.test .. --test-verilog
deactivate
```

Though this process is much longer than the one for MyHDL, it went fairly smoothly. My main complain is the complexity of the directory structure it builds for the tests. It will be interesting to see how easy it is to actually test and integrate with the library.

## Resources
IP of test Ubuntu Machine: 52.14.155.160
http://www.myhdl.org/start/overview.html </br>
https://github.com/cornell-brg/pymtl </br>

