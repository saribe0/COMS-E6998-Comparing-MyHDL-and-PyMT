from myhdl import *
from time import time
from ram import ram

def bench():

	# Constants

	CLK_HALF_PERIOD = 5
	CLK_PERIOD = CLK_HALF_PERIOD * 2

	DATA_WIDTH = 8
	ADDR_WIDTH = 10

	# Signals

	cycle_ctr 	  = Signal(intbv()[32 :])
	output_data   = Signal(intbv()[280:])
	half_word_out = Signal(intbv()[16 :])
	byte_out 	  = Signal(intbv()[8  :])

	clk  = Signal(bool())
	we_a = Signal(bool())
	we_b = Signal(bool())

	data_a = Signal(intbv()[DATA_WIDTH: ])
	data_b = Signal(intbv()[DATA_WIDTH: ])

	addr_a = Signal(intbv()[ADDR_WIDTH: ])
	addr_b = Signal(intbv()[ADDR_WIDTH: ])

	q_a    = Signal(intbv()[DATA_WIDTH: ])
	q_b    = Signal(intbv()[DATA_WIDTH: ])

	# Device Under Test

	# Pure python simulation
	dut = ram(clk, data_a, data_b, addr_a, addr_b, we_a, we_b, q_a, q_b)

	# Generate verilog during simulation
	# dut = toVerilog(ram, clk, data_a, data_b, addr_a, addr_b, we_a, we_b, q_a, q_b)

	#dut.DATA_WIDTH = DATA_WIDTH
	#dut.ADDR_WIDTH = ADDR_WIDTH


	# Clk Generation
	@always(delay(CLK_HALF_PERIOD))
	def clk_gen():
		clk.next = not clk

	# Cycle Counter
	@instance
	def monitor():
		while True:
			yield delay(CLK_PERIOD)
			cycle_ctr.next[:] = cycle_ctr + 1


	# Initialization
	def init():
		clk.next  = 0
		we_a.next = 0
		we_b.next = 0
		cycle_ctr.next[:] = 0


	# Write half words and bytes
	def write_ab(address, data):
		addr_a.next[:] = address
		addr_b.next[:] = address + 1
		data_a.next[:] = data[16: 8]
		data_b.next[:] = data[8 : 0]
		we_a.next = 1
		we_b.next = 1
 
		yield delay(CLK_PERIOD)

		we_a.next = 0
		we_b.next = 0

	def write_a(address, data):
		addr_a.next[:] = address
		data_a.next[:] = data
		we_a.next = 1

		yield delay(CLK_PERIOD)

		we_a.next = 0

	def write_b(address, data):
		addr_b.next[:] = address
		data_b.next[:] = data
		we_b.next = 1

		yield delay(CLK_PERIOD)

		we_b.next = 0

	# Read half words and bytes
	def read_ab(address):
		addr_a.next[:] = address
		addr_b.next[:] = address + 1
		yield delay(CLK_PERIOD)

		half_word_out.val[16: 8] = q_a
		half_word_out.val[8 : 0] = q_b

	def read_a(address):
		addr_a.next[:] = address
		yield delay(CLK_PERIOD)

		byte_out.val[:] = q_a

	def read_b(address):
		addr_b.next[:] = address
		yield delay(CLK_PERIOD)

		byte_out.val[:] = q_b

	# Write a block of 280 bits to RAM
	def write_block(data):
		yield write_ab(0,  data[280 : 264])
		yield write_ab(2,  data[264 : 248])
		yield write_ab(4,  data[248 : 232])
		yield write_ab(6,  data[232 : 216])
		yield write_ab(8,  data[216 : 200])
		yield write_ab(10, data[200 : 184])
		yield write_ab(12, data[184 : 168])
		yield write_ab(14, data[168 : 152])
		yield write_ab(16, data[152 : 136])
		yield write_ab(18, data[136 : 120])
		yield write_ab(20, data[120 : 104])
		yield write_ab(22, data[104 :  88])
		yield write_ab(24, data[88  :  72])
		yield write_ab(26, data[72  :  56])
		yield write_ab(28, data[56  :  40])
		yield write_ab(30, data[40  :  24])
		yield write_a (32, data[24  :  16])
		yield write_a (33, data[16  :   8])
		yield write_b (34, data[8   :   0])

	# Read a block of 280 bits from RAM
	def read_block():
		yield read_a (0)
		output_data.next[280 : 272] = byte_out
		yield read_a (1)
		output_data.next[272 : 264] = byte_out
		yield read_b (2)
		output_data.next[264 : 256] = byte_out
		yield read_ab(3)
		output_data.next[256 : 240] = half_word_out
		yield read_ab(5)
		output_data.next[240 : 224] = half_word_out
		yield read_ab(7)
		output_data.next[224 : 208] = half_word_out
		yield read_ab(9)
		output_data.next[208 : 192] = half_word_out
		yield read_ab(11)
		output_data.next[192 : 176] = half_word_out
		yield read_ab(13)
		output_data.next[176 : 160] = half_word_out
		yield read_ab(15)
		output_data.next[160 : 144] = half_word_out
		yield read_ab(17)
		output_data.next[144 : 128] = half_word_out
		yield read_ab(19)
		output_data.next[128 : 112] = half_word_out
		yield read_ab(21)
		output_data.next[112 :  96] = half_word_out
		yield read_ab(23)
		output_data.next[96  :  80] = half_word_out
		yield read_ab(25)
		output_data.next[80  :  64] = half_word_out
		yield read_ab(27)
		output_data.next[64  :  48] = half_word_out
		yield read_ab(29)
		output_data.next[48  :  32] = half_word_out
		yield read_ab(31)
		output_data.next[32  :  16] = half_word_out
		yield read_ab(33)
		output_data.next[16  :   0] = half_word_out

	# The actual test
	@instance
	def ram_test():

		print "*** Starting RAM test ***"

		init()

		in_data = intbv()[280: ]
		in_data[:] = 0x546869732052414d206d6f64756c652063616e207265616420616e642077726974652e

		# Write the data to ram
		yield write_block(in_data)

		# Read the data form the ram
		yield read_block()

		yield delay(CLK_PERIOD)

		# Compare the results
		if in_data == output_data:
			print "Test Successful"
		else:
			print "Recieved 0x%x" % output_data
			print "Expected 0x%x" % in_data

		# Finish the test
		print "*** RAM test finished ***"
		print "\nSimulation took %d clock cycles." % cycle_ctr
		raise StopSimulation

	return dut, ram_test, clk_gen, monitor

def test_bench():
	start = time()
	tb = bench()
	sim = Simulation(tb)
	sim.run()
	print time() - start

# For generating a waveform
#tb = traceSignals(bench)
#sim = Simulation(tb)
#sim.run()



