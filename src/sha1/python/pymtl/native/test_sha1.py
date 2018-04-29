from pymtl import *
from sha1 import sha1

DEBUG_CORE = 0
DEBUG_TOP  = 1

CLK_HALF_PERIOD = 5
CLK_PERIOD = CLK_HALF_PERIOD * 2

ADDR_NAME0       = 0 # 8'h00
ADDR_NAME1       = 1 # 8'h01
ADDR_VERSION     = 2 # 8'h02

ADDR_CTRL        = 8 # 8'h08
CTRL_INIT_BIT    = 0
CTRL_NEXT_BIT    = 1
CTRL_INIT_VALUE  = 1 # 8'h01
CTRL_NEXT_VALUE  = 2 # 8'h02

ADDR_STATUS      = 9 # 8'h09
STATUS_READY_BIT = 0
STATUS_VALID_BIT = 1

ADDR_BLOCK0    = 16 # 8'h10
ADDR_BLOCK1    = 17 # 8'h11
ADDR_BLOCK2    = 18 # 8'h12
ADDR_BLOCK3    = 19 # 8'h13
ADDR_BLOCK4    = 20 # 8'h14
ADDR_BLOCK5    = 21 # 8'h15
ADDR_BLOCK6    = 22 # 8'h16
ADDR_BLOCK7    = 23 # 8'h17
ADDR_BLOCK8    = 24 # 8'h18
ADDR_BLOCK9    = 25 # 8'h19
ADDR_BLOCK10   = 26 # 8'h1a
ADDR_BLOCK11   = 27 # 8'h1b
ADDR_BLOCK12   = 28 # 8'h1c
ADDR_BLOCK13   = 29 # 8'h1d
ADDR_BLOCK14   = 30 # 8'h1e
ADDR_BLOCK15   = 31 # 8'h1f

ADDR_DIGEST0   = 32 # 8'h20
ADDR_DIGEST1   = 33 # 8'h21
ADDR_DIGEST2   = 34 # 8'h22
ADDR_DIGEST3   = 35 # 8'h23
ADDR_DIGEST4   = 36 # 8'h24


def test_bench():

    test_bench.tb_reset_n = Bits(1)

    test_bench.cycle_ctr = Bits(32, 0) 
    test_bench.error_ctr = Bits(32)
    test_bench.tc_ctr    = Bits(32)

    test_bench.tb_cs = Bits(1)
    test_bench.tb_write_read = Bits(1)
    test_bench.tb_address = Bits(8)
    test_bench.tb_data_in = Bits(32)
    test_bench.tb_data_out = Bits(32)
    test_bench.tb_error = Bits(1)

    test_bench.read_data = Bits(32)
    test_bench.digest_data = Bits(160)


    test_bench.model = sha1()
    test_bench.model.elaborate()
    test_bench.model.reset_n = test_bench.tb_reset_n
    test_bench.model.cs = test_bench.tb_cs
    test_bench.model.we = test_bench.tb_write_read
    test_bench.model.address = test_bench.tb_address
    test_bench.model.write_data = test_bench.tb_data_in
    test_bench.model.read_data = test_bench.tb_data_out
    test_bench.model.error = test_bench.tb_error

    '''
    connect(tb_reset_n, model.reset_n)
    connect(tb_cs, model.cs)
    connect(tb_write_read, model.we)
    connect(tb_address, model.address)
    connect(tb_data_in, model.write_data)
    connect(tb_data_out, model.read_data)
    connect(tb_error, model.error)
    '''

    #   model.elaborate()
    test_bench.sim = SimulationTool(test_bench.model)
    test_bench.sim.reset()

    def delay(cycles = 1):
        for _ in range(cycles):
            test_bench.sim.cycle()
            test_bench.cycle_ctr.value +=  1


    def reset_dut():
	print "*** Toggle reset."
        test_bench.model.reset_n.value = 0

        delay(4)

        test_bench.model.reset_n.value = 1

    def init_sim():
        test_bench.cycle_ctr.value = 0
        test_bench.error_ctr.value = 0
        test_bench.tc_ctr.value = 0

        test_bench.model.reset_n.value = 0
        test_bench.model.cs.value = 0
        test_bench.model.we.value = 0
        test_bench.model.address.value = 0
        test_bench.model.write_data.value = 0

    def display_test_result():
        if (test_bench.error_ctr == 0):
            print "*** All %d test cases completed successfully." % int(test_bench.tc_ctr)
            pass
        else:
            print "*** %d test cases completed." % int(test_bench.tc_ctr)
            print "*** %d errors detected during testing." % int(test_bench.error_ctr)
            pass

    def wait_ready():
        test_bench.read_data.value = 0

        while test_bench.read_data == 0:
            read_word(ADDR_STATUS)

    def read_word(address):
        test_bench.model.address.value = address
        test_bench.model.cs.value = 1
        test_bench.model.we.value = 0

        delay()

        test_bench.read_data.value = test_bench.model.read_data
        test_bench.model.cs.value = 0

	if DEBUG_TOP:
		print "*** Reading 0x%x from 0x%x." % (test_bench.read_data, address)
		print ""

    def write_word(address, word):
	
	if DEBUG_TOP:
                print "*** Writing 0x%x from 0x%x." % (word, address)
                print ""

        test_bench.model.address.value = address
        test_bench.model.write_data.value = word
        test_bench.model.cs.value = 1
        test_bench.model.we.value = 1

        delay()

        test_bench.model.cs.value = 0
        test_bench.model.value = 0

    def write_block(block):
        write_word(ADDR_BLOCK0,  block[480 : 512])
        write_word(ADDR_BLOCK1,  block[448 : 480])
        write_word(ADDR_BLOCK2,  block[416 : 448])
        write_word(ADDR_BLOCK3,  block[384 : 416])
        write_word(ADDR_BLOCK4,  block[352 : 384])
        write_word(ADDR_BLOCK5,  block[320 : 352])
        write_word(ADDR_BLOCK6,  block[288 : 320])
        write_word(ADDR_BLOCK7,  block[256 : 288])
        write_word(ADDR_BLOCK8,  block[224 : 256])
        write_word(ADDR_BLOCK9,  block[192 : 224])
        write_word(ADDR_BLOCK10, block[160 : 192])
        write_word(ADDR_BLOCK11, block[128 : 160])
        write_word(ADDR_BLOCK12, block[96  : 128])
        write_word(ADDR_BLOCK13, block[64  :  96])
        write_word(ADDR_BLOCK14, block[32  :  64])
        write_word(ADDR_BLOCK15, block[0   :  32])

    def check_name_version():
        name0 = Bits(32)
        name1 = Bits(32)
        version = Bits(32)

        read_word(ADDR_NAME0)
        name0.value = test_bench.read_data

        read_word(ADDR_NAME1)
        name1.value = test_bench.read_data

        read_word(ADDR_VERSION)
        version.value = test_bench.read_data

        print "DUT name: %c%c%c%c%c%c%c%c" % (name0[24 : 32], name0[16 : 24], name0[8 : 16], name0[0 : 8], name1[24 : 32], name1[16 : 24], name1[8 : 16], name1[0 : 8])
        print "DUT version: %c%c%c%c" % (version[24 : 32], version[16 : 24], version[8 : 16], version[0 : 8])
    
    def read_digest():

        read_word(ADDR_DIGEST0)
        test_bench.digest_data.value[128 : 160] = test_bench.read_data;
        read_word(ADDR_DIGEST1)
        test_bench.digest_data.value[96  : 128] = test_bench.read_data;
        read_word(ADDR_DIGEST2)
        test_bench.digest_data.value[64  :  96] = test_bench.read_data;
        read_word(ADDR_DIGEST3)
        test_bench.digest_data.value[32  :  64] = test_bench.read_data;
        read_word(ADDR_DIGEST4)
        test_bench.digest_data.value[0   :  32] = test_bench.read_data;

    def single_block_test(block, expected):

        write_block(block)
        write_word(ADDR_CTRL, CTRL_INIT_VALUE)

        delay(2)

        wait_ready()
        read_digest()

        if (test_bench.digest_data == expected):
            print "TC%d: OK." % test_bench.tc_ctr
            pass
        else:
            print "TC%d: ERROR." % test_bench.tc_ctr
            print "TC%d: Expected: 0x%x" % (test_bench.tc_ctr, expected)
            print "TC%d: Got:      0x%x" % (test_bench.tc_ctr, test_bench.digest_data)
            test_bench.error_ctr.value = test_bench.error_ctr + 1;
        
        print "*** TC%d - Single block test done." % test_bench.tc_ctr
        test_bench.tc_ctr.value = test_bench.tc_ctr + 1;

    def double_block_test(block0, expected0, block1, expected1):

        print "*** TC%d - Double block test started." % test_bench.tc_ctr

        ## First block
        write_block(block0)
        write_word(ADDR_CTRL, CTRL_INIT_VALUE)

        delay(2)

        wait_ready()
        read_digest()

        if (test_bench.digest_data == expected0):
            print "TC%d first block: OK." % test_bench.tc_ctr
            pass
        else:
            print "TC%d: ERROR in first digest" % test_bench.tc_ctr
            print "TC%d: Expected: 0x%x" % (test_bench.tc_ctr, expected0)
            print "TC%d: Got:      0x%x" % (test_bench.tc_ctr, test_bench.digest_data)
            test_bench.error_ctr.value = test_bench.error_ctr + 1;

        ## Final block
        write_block(block1)
        write_word(ADDR_CTRL, CTRL_NEXT_VALUE)

        delay(2)

        wait_ready()
        read_digest()

        if (test_bench.digest_data == expected1):
            print "TC%d final block: OK." % test_bench.tc_ctr
            pass
        else:
            print "TC%d: ERROR in final digest"% test_bench.tc_ctr
            print "TC%d: Expected: 0x%x" % (test_bench.tc_ctr, expected1)
            print "TC%d: Got:      0x%x" % (test_bench.tc_ctr, test_bench.digest_data)
            test_bench.error_ctr.value = test_bench.error_ctr + 1;

        print "*** TC%d - Double block test done." % test_bench.tc_ctr
        test_bench.tc_ctr.value += 1;


    # Run the test
    print ""
    print "   -- Testbench for sha1 started --"

    # Initialize the system
    init_sim()

    # Reset
    reset_dut()

    # Check name and version
    check_name_version()
    
    # Prepare test variables
    tc1 = Bits(512)
    res1 = Bits(160)
    tc2_1 = Bits(512)
    res2_1 = Bits(160)
    tc2_2 = Bits(512)
    res2_2 = Bits(160)
    
    ########### TEST 1 ##########
    tc1.value  = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018
    res1.value = 0xa9993e364706816aba3e25717850c26c9cd0d89d
    single_block_test(tc1, res1)    

    ## TC2: Double block message.
    ## "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
    tc2_1.value = 0x6162636462636465636465666465666765666768666768696768696A68696A6B696A6B6C6A6B6C6D6B6C6D6E6C6D6E6F6D6E6F706E6F70718000000000000000
    res2_1.value = 0xF4286818C37B27AE0408F581846771484A566572
    tc2_2.value = 0x1C0
    res2_2.value = 0x84983E441C3BD26EBAAE4AA1F95129E5E54670F1
    double_block_test(tc2_1, res2_1, tc2_2, res2_2)
    
    # Display results and finish up
    delay()
    display_test_result()
    print "*** Simulation done. ***"

    print "\nSimulation took %d clock cycles." % test_bench.cycle_ctr
    

















