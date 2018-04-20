from myhdl import *
from sha1 import sha1
from time import time

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
	## Device Under Test. Only one of these lines should be uncommented
	##----------------------------------------------------------------
	
	# Uncomment this line for pure python simulation
	dut = sha1(tb_clk, tb_reset_n, tb_cs, tb_write_read, tb_address, tb_data_in, tb_data_out, tb_error)

	# Uncomment this line to generate verilog during simulation
	# dut = toVerilog(sha1, tb_clk, tb_reset_n, tb_cs, tb_write_read, tb_address, tb_data_in, tb_data_out, tb_error)
	
	##----------------------------------------------------------------
	## clk_gen
	##
	## Clock generator process.
	##----------------------------------------------------------------
	@always(delay(CLK_HALF_PERIOD))
	def clk_gen():
		tb_clk.next = not tb_clk
		# print 'clok = %d' %tb_clk


	##----------------------------------------------------------------
	## sys_monitor
	##----------------------------------------------------------------
	@instance
	def sys_monitor():
		while True:
			yield delay(CLK_PERIOD)
			cycle_ctr.next[:] = cycle_ctr + 1



	##----------------------------------------------------------------
	## reset_dut()
	##----------------------------------------------------------------
	def reset_dut():
		tb_reset_n.next = 0;
		yield delay(4 * CLK_HALF_PERIOD)
		tb_reset_n.next = 1;

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

	
	##----------------------------------------------------------------
	## display_test_result()
	##
	## Display the accumulated test results.
	##----------------------------------------------------------------
	def display_test_result():
		if (error_ctr == 0):
			print "*** All %d test cases completed successfully." % int(tc_ctr)
			pass
		else:
			print "*** %d test cases completed." % int(tc_ctr)
			print "*** %d errors detected during testing." % int(error_ctr)
			pass
	

	
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
		read_data.val[:] = 0

		while read_data == 0:
			yield read_word(ADDR_STATUS)

	
	##----------------------------------------------------------------
	## read_word()
	##
	## Read a data word from the given address in the DUT.
	## the word read will be available in the global variable
	## read_data.
	##----------------------------------------------------------------
	def read_word(address):
		tb_address.next[:] = address
		tb_cs.next = 1
		tb_write_read.next = 0
	
		yield delay(CLK_PERIOD)
		
		read_data.val[:] = tb_data_out
		tb_cs.next = 0
		
		if DEBUG_TOP:
			print "*** Reading 0x%x from 0x%x." % (read_data, address)
			print ""
			pass
	
		
	##----------------------------------------------------------------
	## write_word()
	##
	## Write the given word to the DUT using the DUT interface.
	##----------------------------------------------------------------
	def write_word(address, word):
		
		if DEBUG_TOP:
			print "*** Writing 0x%x to 0x%x." % (word, address)
			print ""
			pass
		
		tb_address.next[:] = address
		tb_data_in.next[:] = word
		tb_cs.next = 1
		tb_write_read.next = 1;

		yield delay(CLK_PERIOD)

		tb_cs.next = 0
		tb_write_read.next = 0


	##----------------------------------------------------------------
	## write_block()
	##
	## Write the given block to the dut.
	##----------------------------------------------------------------
	def write_block(block):
		yield write_word(ADDR_BLOCK0,  block[512 : 480])
		yield write_word(ADDR_BLOCK1,  block[480 : 448])
		yield write_word(ADDR_BLOCK2,  block[448 : 416])
		yield write_word(ADDR_BLOCK3,  block[416 : 384])
		yield write_word(ADDR_BLOCK4,  block[384 : 352])
		yield write_word(ADDR_BLOCK5,  block[352 : 320])
		yield write_word(ADDR_BLOCK6,  block[320 : 288])
		yield write_word(ADDR_BLOCK7,  block[288 : 256])
		yield write_word(ADDR_BLOCK8,  block[256 : 224])
		yield write_word(ADDR_BLOCK9,  block[224 : 192])
		yield write_word(ADDR_BLOCK10, block[192 : 160])
		yield write_word(ADDR_BLOCK11, block[160 : 128])
		yield write_word(ADDR_BLOCK12, block[128 :  96])
		yield write_word(ADDR_BLOCK13, block[96  :  64])
		yield write_word(ADDR_BLOCK14, block[64  :  32])
		yield write_word(ADDR_BLOCK15, block[32  :   0])

	
	##----------------------------------------------------------------
	## check_name_version()
	##
	## Read the name and version from the DUT.
	##----------------------------------------------------------------
	def check_name_version():
		name0 = intbv()[32:]
		name1 = intbv()[32:]
		version = intbv()[32:]

		# Get name 0
		yield read_word(ADDR_NAME0)
		name0[:] = read_data
		
		# Get name 1
		yield read_word(ADDR_NAME1)
		name1[:] = read_data
	
		# Get version
		yield read_word(ADDR_VERSION)
		version[:] = read_data

		print "DUT name: %c%c%c%c%c%c%c%c" % (name0[31 : 24], name0[23 : 16], name0[15 : 8], name0[7 : 0], name1[31 : 24], name1[23 : 16], name1[15 : 8], name1[7 : 0])
		print "DUT version: %c%c%c%c" % (version[31 : 24], version[23 : 16], version[15 : 8], version[7 : 0])
		
	
	##----------------------------------------------------------------
	## read_digest()
	##
	## Read the digest in the dut. The resulting digest will be
	## available in the global variable digest_data.
	##----------------------------------------------------------------
	def read_digest():

		yield read_word(ADDR_DIGEST0)
		digest_data.val[160 : 128] = read_data;
		yield read_word(ADDR_DIGEST1)
		digest_data.val[128 :  96] = read_data;
		yield read_word(ADDR_DIGEST2)
		digest_data.val[96  :  64] = read_data;
		yield read_word(ADDR_DIGEST3)
		digest_data.val[64  :  32] = read_data;
		yield read_word(ADDR_DIGEST4)
		digest_data.val[32  :   0] = read_data;


	##----------------------------------------------------------------
	## single_block_test()
	##
	##
	## Perform test of a single block digest.
	##----------------------------------------------------------------
	def single_block_test(block, expected):
		print "*** TC%d - Single block test started." % tc_ctr

		yield write_block(block)
		yield write_word(ADDR_CTRL, CTRL_INIT_VALUE)

		yield delay(2*CLK_PERIOD)

		yield wait_ready()
		yield read_digest()
	
		if (digest_data == expected):
			print "TC%d: OK." % tc_ctr
			pass
		else:
			print "TC%d: ERROR." % tc_ctr
			print "TC%d: Expected: 0x%x" % (tc_ctr, expected)
			print "TC%d: Got:      0x%x" % (tc_ctr, digest_data)
			error_ctr.next[:] = error_ctr + 1;
		
		print "*** TC%d - Single block test done." % tc_ctr
		tc_ctr.next[:] = tc_ctr + 1;

	
	##----------------------------------------------------------------
	## double_block_test()
	##
	##
	## Perform test of a double block digest. Note that we check
	## the digests for both the first and final block.
	##----------------------------------------------------------------
	def double_block_test(block0, expected0, block1, expected1):

		print "*** TC%d - Double block test started." % tc_ctr

		## First block
		yield write_block(block0)
		yield write_word(ADDR_CTRL, CTRL_INIT_VALUE)

		yield delay(2*CLK_PERIOD)

		yield wait_ready()
		yield read_digest()

		if (digest_data == expected0):
			print "TC%d first block: OK." % tc_ctr
			pass
		else:
			print "TC%d: ERROR in first digest" % tc_ctr
			print "TC%d: Expected: 0x%x", (tc_ctr, expected0)
			print "TC%d: Got:      0x%x", (tc_ctr, digest_data)
			error_ctr.next[:] = error_ctr + 1;

		## Final block
		yield write_block(block1)
		yield write_word(ADDR_CTRL, CTRL_NEXT_VALUE)

		yield delay(2*CLK_PERIOD)

		yield wait_ready()
		yield read_digest()

		if (digest_data == expected1):
			print "TC%d final block: OK." % tc_ctr
			pass
		else:
			print "TC%d: ERROR in final digest"% tc_ctr
			print "TC%d: Expected: 0x%040x" % (tc_ctr, expected1)
			print "TC%d: Got:      0x%040x" % (tc_ctr, digest_data)
			error_ctr.next[:] = error_ctr + 1;

		print "*** TC%d - Double block test done." % tc_ctr
		tc_ctr.next[:] = tc_ctr + 1;
	

	##----------------------------------------------------------------
	## sha1_test
	## The main test functionality.
	##
	## Test cases taken from:
	## http:##csrc.nist.gov/groups/ST/toolkit/documents/Examples/SHA_All.pdf
	##----------------------------------------------------------------
	@instance
	def check():
		print ""
		print "   -- Testbench for sha1 started --"

		# Initialize the system
		init_sim()

		# Reset
		yield reset_dut()

		# Check name and version
		yield check_name_version()
		
		# Prepare test variables
		tc1 = intbv()[512:]
	        res1 = intbv()[160:]
        	tc2_1 = intbv()[512:]
	        res2_1 = intbv()[160:]
        	tc2_2 = intbv()[512:]
	        res2_2 = intbv()[160:]
		
		########### TEST 1 ##########
		tc1[:]  = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018
		res1[:] = 0xa9993e364706816aba3e25717850c26c9cd0d89d
		yield single_block_test(tc1, res1)	

		## TC2: Double block message.
	        ## "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
		tc2_1[:] = 0x6162636462636465636465666465666765666768666768696768696A68696A6B696A6B6C6A6B6C6D6B6C6D6E6C6D6E6F6D6E6F706E6F70718000000000000000
        	res2_1[:] = 0xF4286818C37B27AE0408F581846771484A566572
        	tc2_2[:] = 0x1C0
        	res2_2[:] = 0x84983E441C3BD26EBAAE4AA1F95129E5E54670F1
        	yield double_block_test(tc2_1, res2_1, tc2_2, res2_2)
		
                # Display results and finish up
		yield delay(CLK_PERIOD)
		display_test_result()
		print "*** Simulation done. ***"

		print "\nSimulation took %d clock cycles." % cycle_ctr
		raise StopSimulation

	return dut, check, clk_gen, sys_monitor

#======================================================================
## EOF tb_sha1.v
##======================================================================


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








