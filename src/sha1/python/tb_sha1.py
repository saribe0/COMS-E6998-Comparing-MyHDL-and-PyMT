from myhdl import *
from sha1 import sha1

def bench():

	##----------------------------------------------------------------
	## Internal constant and parameter definitions.
	##----------------------------------------------------------------

	DEBUG_CORE = 0
	DEBUG_TOP  = 0

	CLK_HALF_PERIOD = 5
	CLK_PERIOD = CLK_HALF_PERIOD * 2

	ADDR_NAME0       = intbv(0, min = 0, max = 255) # 8'h00
	ADDR_NAME1       = intbv(1, min = 0, max = 255) # 8'h01
	ADDR_VERSION     = intbv(2, min = 0, max = 255) # 8'h02

	ADDR_CTRL        = intbv(8, min = 0, max = 255) # 8'h08
	CTRL_INIT_BIT    = 0
	CTRL_NEXT_BIT    = 1
	CTRL_INIT_VALUE  = intbv(1, min = 0, max = 255) # 8'h01
	CTRL_NEXT_VALUE  = intbv(2, min = 0, max = 255) # 8'h02

	ADDR_STATUS      = intbv(9, min = 0, max = 255) # 8'h09
	STATUS_READY_BIT = 0
	STATUS_VALID_BIT = 1

	ADDR_BLOCK0    = intbv(16, min = 0, max = 255) # 8'h10
	ADDR_BLOCK1    = intbv(17, min = 0, max = 255) # 8'h11
	ADDR_BLOCK2    = intbv(18, min = 0, max = 255) # 8'h12
	ADDR_BLOCK3    = intbv(19, min = 0, max = 255) # 8'h13
	ADDR_BLOCK4    = intbv(20, min = 0, max = 255) # 8'h14
	ADDR_BLOCK5    = intbv(21, min = 0, max = 255) # 8'h15
	ADDR_BLOCK6    = intbv(22, min = 0, max = 255) # 8'h16
	ADDR_BLOCK7    = intbv(23, min = 0, max = 255) # 8'h17
	ADDR_BLOCK8    = intbv(24, min = 0, max = 255) # 8'h18
	ADDR_BLOCK9    = intbv(25, min = 0, max = 255) # 8'h19
	ADDR_BLOCK10   = intbv(26, min = 0, max = 255) # 8'h1a
	ADDR_BLOCK11   = intbv(27, min = 0, max = 255) # 8'h1b
	ADDR_BLOCK12   = intbv(28, min = 0, max = 255) # 8'h1c
	ADDR_BLOCK13   = intbv(29, min = 0, max = 255) # 8'h1d
	ADDR_BLOCK14   = intbv(30, min = 0, max = 255) # 8'h1e
	ADDR_BLOCK15   = intbv(31, min = 0, max = 255) # 8'h1f

	ADDR_DIGEST0   = intbv(32, min = 0, max = 255) # 8'h20
	ADDR_DIGEST1   = intbv(33, min = 0, max = 255) # 8'h21
	ADDR_DIGEST2   = intbv(34, min = 0, max = 255) # 8'h22
	ADDR_DIGEST3   = intbv(35, min = 0, max = 255) # 8'h23
	ADDR_DIGEST4   = intbv(36, min = 0, max = 255) # 8'h24


	##----------------------------------------------------------------
	## Register and Wire declarations.
	##----------------------------------------------------------------
	cycle_ctr = Signal(intbv(0)[32:0]) 		# reg [31 : 0] cycle_ctr;
	error_ctr = Signal(intbv(0)[32:0]) 		# reg [31 : 0] error_ctr;
	tc_ctr    = Signal(intbv(0)[32:0]) 		# reg [31 : 0] tc_ctr;

	tb_clk	  		= Signal(bool(0)) 			# reg           tb_clk;
	tb_reset_n		= Signal(bool(0)) 			# reg           tb_reset_n;
	tb_cs 			= Signal(bool(0)) 			# reg           tb_cs;
	tb_write_read 	= Signal(bool(0)) 			# reg           tb_write_read;
	tb_address 		= Signal(intbv(0)[8:]) 	# reg [7 : 0]   tb_address;
	tb_data_in		= Signal(intbv(0)[32:]) 	# reg [31 : 0]  tb_data_in;
	tb_data_out 	= Signal(intbv(0)[32:]) 	# wire [31 : 0] tb_data_out;
	tb_error 	= Signal(bool())

	read_data	= Signal(intbv(0)[32:]) 	# reg [31 : 0]  read_data;
	digest_data = Signal(intbv(0)[160:]) 	# reg [159 : 0] digest_data;


	##----------------------------------------------------------------
	## Device Under Test.
	##----------------------------------------------------------------
	
	dut = sha1(tb_clk, tb_reset_n, tb_cs, tb_write_read, tb_address, tb_data_in, tb_data_out, tb_error)

	
	##----------------------------------------------------------------
	## clk_gen
	##
	## Clock generator process.
	##----------------------------------------------------------------
	@always(delay(CLK_HALF_PERIOD))
	def clk_gen():
		tb_clk.next = not tb_clk


	##----------------------------------------------------------------
	## sys_monitor
	##----------------------------------------------------------------
	@instance
	def sys_monitor():
		while True:
			if (DEBUG_CORE):
				dump_core_state()

			if (DEBUG_TOP):
				dump_top_state()

			yield delay(CLOCK_PERIOD)

			cycle_ctr.next[:] = cycle_ctr + 1


	##----------------------------------------------------------------
	## dump_top_state()
	##
	## Dump state of the the top of the dut.
	##----------------------------------------------------------------------------UNSURE TODO: FIX 
	'''
	@instance
	def dump_top_state():
		print "State of top"
		print "-------------"
		print "Inputs and outputs:"
		print "cs      = 0x%01x,  we         = 0x%01x", dut.cs, dut.we
		print "address = 0x%02x, write_data = 0x%08x", dut.address, dut.write_data
		print "error   = 0x%01x,  read_data  = 0x%08x", dut.error, dut.read_data
		print ""

		print "Control and status flags:"
		print "init = 0x%01x, next = 0x%01x, ready = 0x%01x",
		dut.init_reg, dut.next_reg, dut.ready_reg
		print ""

		print "block registers:"
		print "block0  = 0x%08x, block1  = 0x%08x, block2  = 0x%08x,  block3  = 0x%08x",
		dut.block_reg[00], dut.block_reg[01], dut.block_reg[02], dut.block_reg[03]
		print "block4  = 0x%08x, block5  = 0x%08x, block6  = 0x%08x,  block7  = 0x%08x",
		dut.block_reg[04], dut.block_reg[05], dut.block_reg[06], dut.block_reg[07]
		print "block8  = 0x%08x, block9  = 0x%08x, block10 = 0x%08x,  block11 = 0x%08x",
		dut.block_reg[08], dut.block_reg[09], dut.block_reg[10], dut.block_reg[11]
		print "block12 = 0x%08x, block13 = 0x%08x, block14 = 0x%08x,  block15 = 0x%08x",
		dut.block_reg[12], dut.block_reg[13], dut.block_reg[14], dut.block_reg[15]
		print ""

		print "Digest registers:"
		print "digest_reg  = 0x%040x", dut.digest_reg
		print ""
	'''

	##----------------------------------------------------------------
	## dump_core_state()
	##
	## Dump the state of the core inside the dut.
	##----------------------------------------------------------------------------UNSURE TODO: FIX 
	'''
	@instance
	def dump_core_state():
		print "State of core"
		print "-------------"
		print "Inputs and outputs:"
		print "init   = 0x%01x, next  = 0x%01x",
		dut.core.init, dut.core.next
		print "block  = 0x%0128x", dut.core.block

		print "ready  = 0x%01x, valid = 0x%01x",
		dut.core.ready, dut.core.digest_valid
		print "digest = 0x%040x", dut.core.digest
		print "H0_reg = 0x%08x, H1_reg = 0x%08x, H2_reg = 0x%08x, H3_reg = 0x%08x, H4_reg = 0x%08x",
		dut.core.H0_reg, dut.core.H1_reg, dut.core.H2_reg, dut.core.H3_reg, dut.core.H4_reg
		print ""

		print "Control signals and counter:"
		print "sha1_ctrl_reg = 0x%01x", dut.core.sha1_ctrl_reg
		print "digest_init   = 0x%01x, digest_update = 0x%01x",
		dut.core.digest_init, dut.core.digest_update
		print "state_init    = 0x%01x, state_update  = 0x%01x",
		dut.core.state_init, dut.core.state_update
		print "first_block   = 0x%01x, ready_flag    = 0x%01x, w_init        = 0x%01x",
		dut.core.first_block, dut.core.ready_flag, dut.core.w_init
		print "round_ctr_inc = 0x%01x, round_ctr_rst = 0x%01x, round_ctr_reg = 0x%02x",
		dut.core.round_ctr_inc, dut.core.round_ctr_rst, dut.core.round_ctr_reg
		print ""

		print "State registers:"
		print "a_reg = 0x%08x, b_reg = 0x%08x, c_reg = 0x%08x, d_reg = 0x%08x, e_reg = 0x%08x",
		dut.core.a_reg, dut.core.b_reg, dut.core.c_reg, dut.core.d_reg,  dut.core.e_reg
		print "a_new = 0x%08x, b_new = 0x%08x, c_new = 0x%08x, d_new = 0x%08x, e_new = 0x%08x",
		dut.core.a_new, dut.core.b_new, dut.core.c_new, dut.core.d_new, dut.core.e_new
		print ""

		print "State update values:"
		print "f = 0x%08x, k = 0x%08x, t = 0x%08x, w = 0x%08x,",
		dut.core.state_logic.f, dut.core.state_logic.k, dut.core.state_logic.t, dut.core.w
		print ""
	'''


	##----------------------------------------------------------------
	## reset_dut()
	##----------------------------------------------------------------
	'''
	@instance
	def reset_dut():
		tb_reset_n.next = 0;
		yield delay(4 * CLK_HALF_PERIOD)
		tb_reset_n.next = 1;
	'''

	##----------------------------------------------------------------
	## init_sim()
	##
	## Initialize all counters and testbed functionality as well
	## as setting the DUT inputs to defined values.
	##---------------------------------------------------------------
	def init_sim():
		cycle_ctr.next[:] = 0
		error_ctr.next[:] = 0
		tc_ctr.next[:] 	  = 0

		tb_clk.next  	  = 0
		tb_reset_n.next	  = 0
		tb_cs.next   	  = 0
		tb_write_read.next	= 0
		tb_address.next[:]	= 0
		tb_data_in.next[:]	= 0

	'''
	##----------------------------------------------------------------
	## display_test_result()
	##
	## Display the accumulated test results.
	##----------------------------------------------------------------
	def display_test_result():
		if (error_ctr == 0):
			print "*** All %d test cases completed successfully." % int(tc_ctr)
		else:
			print "*** %d test cases completed." % int(tc_ctr)
			print "*** %d errors detected during testing." % int(error_ctr)
	


	##----------------------------------------------------------------
	## wait_ready()
	##
	## Wait for the ready flag in the dut to be set.
	## (Actually we wait for either ready or valid to be set.)
	##
	## Note: It is the callers responsibility to call the function
	## when the dut is actively processing and will in fact at some
	## point set the flag.
	##----------------------------------------------------------------
	def wait_ready():
		read_data.next[:] =0

		while read_data == 0:
			read_word(ADDR_STATUS)


	##----------------------------------------------------------------
	## read_word()
	##
	## Read a data word from the given address in the DUT.
	## the word read will be available in the global variable
	## read_data.
	##----------------------------------------------------------------
	def read_word(address):
		tb_address[:] = address
		tb_cs = 1
		tb_write_read = 0

		yield delay(CLOCK_PERIOD)

		read_data[:] = tb_data_out
		tb_cs = 0
'''
		'''
		if DEBUG_TOP:
			print "*** Reading 0x%08x from 0x%02x.", read_data, address
			print ""
		'''
'''
	##----------------------------------------------------------------
	## write_word()
	##
	## Write the given word to the DUT using the DUT interface.
	##----------------------------------------------------------------
	def write_word(address, word):'''
		'''
		if DEBUG_TOP:
			print "*** Writing 0x%08x to 0x%02x.", word, address
			print ""
		'''
'''		tb_address[:] = address
		tb_data_in[:] = word
		tb_cs = 1
		tb_write_read = 1;

		yield delay(CLOCK_PERIOD)

		tb_cs = 0
		tb_write_read = 0


	##----------------------------------------------------------------
	## write_block()
	##
	## Write the given block to the dut.
	##----------------------------------------------------------------
	def write_block(block):
		write_word(ADDR_BLOCK0,  block[512 : 480])
		write_word(ADDR_BLOCK1,  block[480 : 448])
		write_word(ADDR_BLOCK2,  block[448 : 416])
		write_word(ADDR_BLOCK3,  block[416 : 384])
		write_word(ADDR_BLOCK4,  block[384 : 352])
		write_word(ADDR_BLOCK5,  block[352 : 320])
		write_word(ADDR_BLOCK6,  block[320 : 288])
		write_word(ADDR_BLOCK7,  block[288 : 256])
		write_word(ADDR_BLOCK8,  block[256 : 224])
		write_word(ADDR_BLOCK9,  block[224 : 192])
		write_word(ADDR_BLOCK10, block[192 : 160])
		write_word(ADDR_BLOCK11, block[160 : 128])
		write_word(ADDR_BLOCK12, block[128 :  96])
		write_word(ADDR_BLOCK13, block[96  :  64])
		write_word(ADDR_BLOCK14, block[64  :  32])
		write_word(ADDR_BLOCK15, block[32  :   0])


	##----------------------------------------------------------------
	## check_name_version()
	##
	## Read the name and version from the DUT.
	##----------------------------------------------------------------
	def check_name_version():
		name0 = intbv()[32:]
		name1 = intbv()[32:]
		version = intbv()[32:]

		read_word(ADDR_NAME0)
		name0[:] = read_data
		read_word(ADDR_NAME1)
		name1[:] = read_data
		read_word(ADDR_VERSION)
		version[:] = read_data

		'''
'''		print "DUT name: %c%c%c%c%c%c%c%c",
						 name0[31 : 24], name0[23 : 16], name0[15 : 8], name0[7 : 0],
						 name1[31 : 24], name1[23 : 16], name1[15 : 8], name1[7 : 0]
		print "DUT version: %c%c%c%c",
						 version[31 : 24], version[23 : 16], version[15 : 8], version[7 : 0]'''
		'''

	##----------------------------------------------------------------
	## read_digest()
	##
	## Read the digest in the dut. The resulting digest will be
	## available in the global variable digest_data.
	##----------------------------------------------------------------
	def read_digest():

		read_word(ADDR_DIGEST0)
		digest_data[160 : 128] = read_data;
		read_word(ADDR_DIGEST1)
		digest_data[128 :  96] = read_data;
		read_word(ADDR_DIGEST2)
		digest_data[96  :  64] = read_data;
		read_word(ADDR_DIGEST3)
		digest_data[64  :  32] = read_data;
		read_word(ADDR_DIGEST4)
		digest_data[32  :   0] = read_data;


	##----------------------------------------------------------------
	## single_block_test()
	##
	##
	## Perform test of a single block digest.
	##----------------------------------------------------------------
	def single_block_test(block, expected):
		# print "*** TC%01d - Single block test started.", tc_ctr

		write_block(block)
		write_word(ADDR_CTRL, CTRL_INIT_VALUE)

		yield delay(CLK_PERIOD)

		wait_ready()
		read_digest()

		if (digest_data == expected):
			# print "TC%01d: OK.", tc_ctr
			pass
		else:
			# print "TC%01d: ERROR.", tc_ctr
			# print "TC%01d: Expected: 0x%040x", tc_ctr, expected
			# print "TC%01d: Got:      0x%040x", tc_ctr, digest_data
			error_ctr[:] = error_ctr + 1;
		
		# print "*** TC%01d - Single block test done.", tc_ctr
		tc_ctr[:] = tc_ctr + 1;


	##----------------------------------------------------------------
	## double_block_test()
	##
	##
	## Perform test of a double block digest. Note that we check
	## the digests for both the first and final block.
	##----------------------------------------------------------------
	def double_block_test(block0, expected0, block1, expected1):

		# print "*** TC%01d - Double block test started.", tc_ctr

		## First block
		write_block(block0)
		write_word(ADDR_CTRL, CTRL_INIT_VALUE)

		yield delay(CLOCK_PERIOD)

		wait_ready()
		read_digest()

		if (digest_data == expected0):
			#print "TC%01d first block: OK.", tc_ctr
			pass
		else:
			#print "TC%01d: ERROR in first digest", tc_ctr
			#print "TC%01d: Expected: 0x%040x", tc_ctr, expected0
			#print "TC%01d: Got:      0x%040x", tc_ctr, digest_data
			error_ctr[:] = error_ctr + 1;

		## Final block
		write_block(block1)
		write_word(ADDR_CTRL, CTRL_NEXT_VALUE)

		yield delay(CLOCK_PERIOD)

		wait_ready()
		read_digest()

		if (digest_data == expected1):
			#print "TC%01d final block: OK.", tc_ctr
			pass
		else:
			#print "TC%01d: ERROR in final digest", tc_ctr
			#print "TC%01d: Expected: 0x%040x", tc_ctr, expected1
			#print "TC%01d: Got:      0x%040x", tc_ctr, digest_data
			error_ctr[:] = error_ctr + 1;

		#print "*** TC%01d - Double block test done.", tc_ctr
		tc_ctr[:] = tc_ctr + 1;
	'''

	##----------------------------------------------------------------
	## sha1_test
	## The main test functionality.
	##
	## Test cases taken from:
	## http:##csrc.nist.gov/groups/ST/toolkit/documents/Examples/SHA_All.pdf
	##----------------------------------------------------------------
	@instance
	def check():
		print "   -- Testbench for sha1 started --"

		# Reset
		init_sim()
		tb_reset_n.next = 0;

		# Wait 4 clock ticks
		yield delay(4 * CLK_HALF_PERIOD)

		# Un-enable reset
		tb_reset_n.next = 1;

		# Read version info from the DUT
		name0 = intbv()[32:]
		name1 = intbv()[32:]
		version = intbv()[32:]

		# Read Name 0
		tb_address[:] = ADDR_NAME0
		tb_cs = 1
		tb_write_read = 0
		yield delay(CLOCK_PERIOD)
		name0[:] = tb_data_out
		tb_cs = 0

		# Read Name 1
		tb_address[:] = ADDR_NAME1
		tb_cs = 1
		tb_write_read = 0
		yield delay(CLOCK_PERIOD)
		name1[:] = tb_data_out
		tb_cs = 0

		# Read Version Info
		tb_address[:] = ADDR_VERSION
		tb_cs = 1
		tb_write_read = 0
		yield delay(CLOCK_PERIOD)
		version[:] = tb_data_out
		tb_cs = 0

		yield delay(CLOCK_PERIOD)

		
		print "DUT name: %c%c%c%c%c%c%c%c" % (name0[31 : 24], name0[23 : 16], name0[15 : 8], name0[7 : 0],
						 					  name1[31 : 24], name1[23 : 16], name1[15 : 8], name1[7 : 0])
		print "DUT version: %c%c%c%c" % (version[31 : 24], version[23 : 16], version[15 : 8], version[7 : 0])

	return sha1, check, clk_gen, sys_monitor

	'''
	tc1 = intbv()[512:]
	res1 = intbv()[160:]

	tc2_1 = intbv()[512:]
	res2_1 = intbv()[160:]
	tc2_2 = intbv()[512:]
	res2_2 = intbv()[160:]
	'''
	'''
	print "   -- Testbench for sha1 started --"

	init_sim()
	check_name_version()

	## TC1: Single block message: "abc".
	tc1[:] = 5100431258107249700168418948414140220579695416282740287258808047360864048991964757897370917042356648128214697817844060110735030706394180882420833873559576
	res1[:] = 968236873715988614170569073515315707566766479517
	single_block_test(tc1, res1)

	## TC2: Double block message.
	## "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
	tc2_1[:] = 5100431171898069115163634243358666473761008276522498094073997421077178130866117634074596662252782114592477252990350509598466861911873471821407367712473088
	res2_1[:] = 1393894845993310694499304876646646237122520311154

	tc2_2[:] = 448
	res2_2[:] = 756981919157381189150916787291668349464288325873
	double_block_test(tc2_1, res2_1, tc2_2, res2_2)

	display_test_result()
	print "*** Simulation done. ***"

	return dut, reset_dut, clk_gen, sys_monitor 
	'''
##======================================================================
## EOF tb_sha1.v
##======================================================================


def test_bench():
	tb = bench()
	sim = Simulation(tb)
	sim.run()

bench()









