from pymtl import *
from ram import ram

CLK_HALF_PERIOD = 5
CLK_PERIOD = CLK_HALF_PERIOD * 2

DATA_WIDTH = 8
ADDR_WIDTH = 10

def test_bench():

    # Local signals
    test_bench.cycle_ctr     = Bits(32)
    test_bench.output_data   = Bits(280)
    test_bench.half_word_out = Bits(16)
    test_bench.byte_out      = Bits(8)

    test_bench.we_a = Bits(1)
    test_bench.we_b = Bits(1)

    test_bench.data_a = Bits(DATA_WIDTH)
    test_bench.data_b = Bits(DATA_WIDTH)
    test_bench.addr_a = Bits(ADDR_WIDTH)
    test_bench.addr_b = Bits(ADDR_WIDTH)
    test_bench.q_a    = Bits(DATA_WIDTH)
    test_bench.q_b    = Bits(DATA_WIDTH)

    # Device under test
    test_bench.model = ram()
    test_bench.model.elaborate()
    test_bench.model.DATA_WIDTH = DATA_WIDTH
    test_bench.model.ADDR_WIDTH = ADDR_WIDTH
    test_bench.model.we_a = test_bench.we_a
    test_bench.model.we_b = test_bench.we_b
    test_bench.model.data_a = test_bench.data_a
    test_bench.model.data_b = test_bench.data_b
    test_bench.model.addr_a = test_bench.addr_a
    test_bench.model.addr_b = test_bench.addr_b
    test_bench.model.q_a = test_bench.q_a
    test_bench.model.q_b = test_bench.q_b

    # For simulation
    test_bench.sim = SimulationTool(test_bench.model)
    test_bench.sim.reset()

    # For verilog translation
    #vModel = ram()
    #translated = TranslationTool(vModel)

    def delay(cycles = 1):
        for _ in range(cycles):
            test_bench.sim.cycle()
            test_bench.cycle_ctr.value += 1

    def init():
        test_bench.we_a.value = 0
        test_bench.we_b.value = 0
        test_bench.cycle_ctr.value = 0

    # Write bytes and half words
    def write_ab(address, data):
        test_bench.model.addr_a.value = address
        test_bench.model.addr_b.value = address + 1
        test_bench.model.data_a.value = data[8 : 16]
        test_bench.model.data_b.value = data[0 :  8]
        test_bench.model.we_a.value = 1
        test_bench.model.we_b.value = 1

        delay()

        test_bench.model.we_a.value = 0
        test_bench.model.we_b.value = 0

    def write_a(address, data):
        test_bench.model.addr_a.value = address
        test_bench.model.data_a.value = data
        test_bench.model.we_a.value = 1

        delay()

        test_bench.model.we_a.value = 0

    def write_b(address, data):
        test_bench.model.addr_b.value = address
        test_bench.model.data_b.value = data
        test_bench.model.we_b.value = 1

        delay()

        test_bench.model.we_b.value = 0

    # Read bytes and half words
    def read_ab(address):
        test_bench.model.addr_a.value = address
        test_bench.model.addr_b.value = address + 1

        delay()

        test_bench.half_word_out.value[8 : 16] = test_bench.model.q_a
        test_bench.half_word_out.value[0 :  8] = test_bench.model.q_b

    def read_a(address):
        test_bench.model.addr_a.value = address

        delay()

        test_bench.byte_out.value[0 : 8] = test_bench.model.q_a

    def read_b(address):
        test_bench.model.addr_b.value = address

        delay()

        test_bench.byte_out.value[0 : 8] = test_bench.model.q_b


    # Write and read blocks of 280 bits
    def write_block(data):
        write_ab(0,  data[264 : 280])
        write_ab(2,  data[248 : 264])
        write_ab(4,  data[232 : 248])
        write_ab(6,  data[216 : 232])
        write_ab(8,  data[200 : 216])
        write_ab(10, data[184 : 200])
        write_ab(12, data[168 : 184])
        write_ab(14, data[152 : 168])
        write_ab(16, data[136 : 152])
        write_ab(18, data[120 : 136])
        write_ab(20, data[104 : 120])
        write_ab(22, data[88  : 104])
        write_ab(24, data[72  :  88])
        write_ab(26, data[56  :  72])
        write_ab(28, data[40  :  56])
        write_ab(30, data[24  :  40])
        write_a (32, data[16  :  24])
        write_a (33, data[8   :  16])
        write_b (34, data[0   :   8])

    def read_block():
        read_a (0)
        test_bench.output_data.value[272 : 280] = test_bench.byte_out
        read_a (1)
        test_bench.output_data.value[264 : 272] = test_bench.byte_out
        read_b (2)
        test_bench.output_data.value[256 : 264] = test_bench.byte_out
        read_ab(3)
        test_bench.output_data.value[240 : 256] = test_bench.half_word_out
        read_ab(5)
        test_bench.output_data.value[224 : 240] = test_bench.half_word_out
        read_ab(7)
        test_bench.output_data.value[208 : 224] = test_bench.half_word_out
        read_ab(9)
        test_bench.output_data.value[192 : 208] = test_bench.half_word_out
        read_ab(11)
        test_bench.output_data.value[176 : 192] = test_bench.half_word_out
        read_ab(13)
        test_bench.output_data.value[160 : 176] = test_bench.half_word_out
        read_ab(15)
        test_bench.output_data.value[144 : 160] = test_bench.half_word_out
        read_ab(17)
        test_bench.output_data.value[128 : 144] = test_bench.half_word_out
        read_ab(19)
        test_bench.output_data.value[112 : 128] = test_bench.half_word_out
        read_ab(21)
        test_bench.output_data.value[96  : 112] = test_bench.half_word_out
        read_ab(23)
        test_bench.output_data.value[80  :  96] = test_bench.half_word_out
        read_ab(25)
        test_bench.output_data.value[64  :  80] = test_bench.half_word_out
        read_ab(27)
        test_bench.output_data.value[48  :  64] = test_bench.half_word_out
        read_ab(29)
        test_bench.output_data.value[32  :  48] = test_bench.half_word_out
        read_ab(31)
        test_bench.output_data.value[16  :  32] = test_bench.half_word_out
        read_ab(33)
        test_bench.output_data.value[0   :  16] = test_bench.half_word_out


    # Run the test
    print ""
    print "*** Starting RAM test ***"

    init()
    
    in_data = Bits(280)
    in_data.value = 0x546869732052414d206d6f64756c652063616e207265616420616e642077726974652e

    # Write the data to RAM
    write_block(in_data)

    # Read the data from RAM
    read_block()

    # Compare the results
    if in_data == test_bench.output_data:
        print "Test Successful"
    else:
        print "Recieved 0x%x" % test_bench.output_data
        print "Expected 0x%x" % in_data

    print "*** RAM test finished ***"
    print "\nSimulation took %d clock cycles." % test_bench.cycle_ctr
























