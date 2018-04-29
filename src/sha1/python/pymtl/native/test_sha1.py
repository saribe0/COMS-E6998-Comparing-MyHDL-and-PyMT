from pymtl import *
from sha1 import sha1

DEBUG_CORE = 0
DEBUG_TOP  = 0

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

    tb_reset_n = Wire(Bits(1))

    cycle_ctr = Wire(Bits(32)) 
    error_ctr = Wire(Bits(32))
    tc_ctr    = Wire(Bits(32))

    tb_cs = Wire(Bits(1))
    tb_write_read = Wire(Bits(1))
    tb_address = Wire(Bits(8))
    tb_data_in = Wire(Bits(32))
    tb_data_out = Wire(Bits(32))
    tb_error = Wire(Bits(1))

    read_data = Wire(Bits(32))
    digest_data = Wire(Bits(160))


    model = sha1()
    model.elaborate()
    model.reset_n = tb_reset_n
    model.cs = tb_cs
    model.we = tb_write_read
    model.address = tb_address
    model.write_data = tb_data_in
    model.read_data = tb_data_out
    model.error = tb_error

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
    sim = SimulationTool(model)
    sim.reset()

    def delay(cycles = 1):
        for _ in range(cycles):
            sim.cycle()
            cycle_ctr = cycle_ctr + 1


    def reset_dut():
        tb_reset_n = 0

        delay(4)

        tb_reset_n = 1

    def init_sim():
        cycle_ctr = 0
        error_ctr = 0
        tc_ctr = 0

        tb_reset_n = 0
        tb_cs = 0
        tb_write_read = 0
        tb_address = 0
        tb_data_in = 0

    def display_test_result():
        if (error_ctr == 0):
            print "*** All %d test cases completed successfully." % int(tc_ctr)
            pass
        else:
            print "*** %d test cases completed." % int(tc_ctr)
            print "*** %d errors detected during testing." % int(error_ctr)
            pass

    def wait_ready():
        read_data.value = 0

        while read_data == 0:
            read_word(ADDR_STATUS)

    def read_word(address):
        tb_address.value = address
        tb_cs.value = 1
        tb_write_read.value = 0

        delay()

        read_data.value = tb_data_out
        tb_cs.value = 0


    def write_word(address, word):
        tb_address.value = address
        tb_data_in.value = word
        tb_cs.value = 1
        tb_write_read.value = 1

        delay()

        tb_cs.value = 0
        tb_write_read.value = 0

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
        name0 = Wire(Bits(32))
        name1 = Wire(Bits(32))
        version = Wire(Bits(32))

        read_word(ADDR_NAME0)
        name0.value = read_data

        read_word(ADDR_NAME1)
        name1.value = read_data

        read_word(ADDR_VERSION)
        version.value = read_data

        print "DUT name: %c%c%c%c%c%c%c%c" % (name0[24 : 32], name0[16 : 24], name0[8 : 16], name0[0 : 8], name1[24 : 32], name1[16 : 24], name1[8 : 16], name1[0 : 8])
        print "DUT version: %c%c%c%c" % (version[24 : 32], version[16 : 24], version[8 : 16], version[0 : 8])
    
    def read_digest():

        read_word(ADDR_DIGEST0)
        digest_data.value[128 : 160] = read_data;
        read_word(ADDR_DIGEST1)
        digest_data.value[96  : 128] = read_data;
        read_word(ADDR_DIGEST2)
        digest_data.value[64  :  96] = read_data;
        read_word(ADDR_DIGEST3)
        digest_data.value[32  :  64] = read_data;
        read_word(ADDR_DIGEST4)
        digest_data.value[0   :  32] = read_data;

    def single_block_test(block, expected):

        write_block(block)
        write_word(ADDR_CTRL, CTRL_INIT_VALUE)

        delay(2)

        wait_ready()
        read_digest()

        if (digest_data == expected):
            print "TC%d: OK." % tc_ctr
            pass
        else:
            print "TC%d: ERROR." % tc_ctr
            print "TC%d: Expected: 0x%x" % (tc_ctr, expected)
            print "TC%d: Got:      0x%x" % (tc_ctr, digest_data)
            error_ctr.value = error_ctr + 1;
        
        print "*** TC%d - Single block test done." % tc_ctr
        tc_ctr.value = tc_ctr + 1;

    def double_block_test(block0, expected0, block1, expected1):

        print "*** TC%d - Double block test started." % tc_ctr

        ## First block
        write_block(block0)
        write_word(ADDR_CTRL, CTRL_INIT_VALUE)

        delay(2)

        wait_ready()
        read_digest()

        if (digest_data == expected0):
            print "TC%d first block: OK." % tc_ctr
            pass
        else:
            print "TC%d: ERROR in first digest" % tc_ctr
            print "TC%d: Expected: 0x%x", (tc_ctr, expected0)
            print "TC%d: Got:      0x%x", (tc_ctr, digest_data)
            error_ctr.value = error_ctr + 1;

        ## Final block
        write_block(block1)
        write_word(ADDR_CTRL, CTRL_NEXT_VALUE)

        delay(2)

        wait_ready()
        read_digest()

        if (digest_data == expected1):
            print "TC%d final block: OK." % tc_ctr
            pass
        else:
            print "TC%d: ERROR in final digest"% tc_ctr
            print "TC%d: Expected: 0x%040x" % (tc_ctr, expected1)
            print "TC%d: Got:      0x%040x" % (tc_ctr, digest_data)
            error_ctr.value = error_ctr + 1;

        print "*** TC%d - Double block test done." % tc_ctr
        tc_ctr.value = tc_ctr + 1;


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

    print "\nSimulation took %d clock cycles." % cycle_ctr
    

















