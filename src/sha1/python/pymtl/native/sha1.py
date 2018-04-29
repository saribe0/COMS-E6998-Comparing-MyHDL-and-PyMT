from pymtl import *
from sha1_core import sha1_core

class sha1( Model ):

    # Constructor
    def __init__( s ):

        ADDR_NAME0       = 0x00  #intbv(0)[8:] # 8'h00;
        ADDR_NAME1       = 0x01  #intbv(1)[8:] # 8'h01;
        ADDR_VERSION     = 0x02  #intbv(2)[8:] # 8'h02;

        ADDR_CTRL        = 0x08  #intbv(8)[8:] # 8'h08;
        CTRL_INIT_BIT    = 0
        CTRL_NEXT_BIT    = 1

        ADDR_STATUS      = 0x09  #intbv(9)[8:] # 8'h09;
        STATUS_READY_BIT = 0
        STATUS_VALID_BIT = 1

        ADDR_BLOCK0    = 0x10    #intbv(16)[8:] # 8'h10;
        ADDR_BLOCK15   = 0x1f    #intbv(31)[8:] # 8'h1f;

        ADDR_DIGEST0   = 0x20    #intbv(32)[8:] # 8'h20;
        ADDR_DIGEST4   = 0x24    #intbv(36)[8:] # 8'h24;

        CORE_NAME0     = 0x73686131  #intbv(1936220465)[32:] # 32'h73686131; ## "sha1"
        CORE_NAME1     = 0x20202020  #intbv(538976288)[32:]  # 32'h20202020; ## "    "
        CORE_VERSION   = 0x302e3630  #intbv(808334896)[32:]  # 32'h302e3630; ## "0.60"

        # Port-based interface

        # Clock and reset inherently included
        # s.clk       = InPort (Bits(1))
        s.reset_n = InPort (Bits(1))
        s.cs      = InPort (Bits(1))
        s.we      = InPort (Bits(1))

        s.address    = InPort (Bits(8))
        s.write_data = InPort (Bits(32))
        s.read_data  = OutPort(Bits(32))
        s.error      = OutPort(Bits(1))

        s.init_reg   = Wire(Bits(1))
        s.init_new   = Wire(Bits(1))
        s.next_reg   = Wire(Bits(1))
        s.next_new   = Wire(Bits(1))
        s.ready_reg  = Wire(Bits(1))
        s.block_reg  = [Wire(Bits(32)) for _ in range(16)]
        s.block_we   = Wire(Bits(1))
        s.digest_reg = Wire(Bits(160))
        s.digest_valid_reg = Wire(Bits(1))

        s.core_ready = Wire(Bits(1))
        s.core_block = Wire(Bits(512))
        s.core_digest= Wire(Bits(160))
        s.core_digest_valid = Wire(Bits(1))
        s.tmp_read_data     = Wire(Bits(32))
        s.tmp_error         = Wire(Bits(1))


        # Intantiate the core
        s.core = sha1_core()
        s.connect(s.reset_n, s.core.reset_n)
        s.connect(s.init_reg, s.core.init)
        s.connect(s.next_reg, s.core.next)
        s.connect(s.core_block, s.core.block)
        s.connect(s.core_ready, s.core.ready)
        s.connect(s.core_digest, s.core.digest)
        s.connect(s.core_digest_valid, s.core.digest_valid)


        # Concurrent block
        @s.combinational
        def logic():
            s.core_block.value = concat(s.block_reg[0], s.block_reg[1], s.block_reg[2], s.block_reg[3], 
                                        s.block_reg[4], s.block_reg[5], s.block_reg[6], s.block_reg[7], 
                                        s.block_reg[8], s.block_reg[9], s.block_reg[10], s.block_reg[11], 
                                        s.block_reg[12], s.block_reg[13], s.block_reg[14], s.block_reg[15])
            s.read_data.value = s.tmp_read_data
            s.error.value = s.tmp_error

        @s.tick
        def reg_update():
            if not s.reset_n:
                s.init_reg.next = 0
                s.next_reg.next = 0
                s.ready_reg.next = 0
                s.digest_reg.next = 0
                s.digest_valid_reg.next = 0

            else:
                s.ready_reg.next = s.core_ready
                s.digest_valid_reg.next = s.core_digest_valid
                s.init_reg.next = s.init_new
                s.next_reg.next = s.next_new

                if s.block_we:
                    s.block_reg[s.address[0:4]].next = s.write_data

                if s.core_digest_valid:
                    s.digest_reg.next = s.core_digest

        @s.combinational
        def api():
            s.init_new.value = 0
            s.next_new.value = 0
            s.block_we.value = 0
            s.tmp_read_data.value = 0
            s.tmp_error.value = 0

            if s.cs:

                if s.we:

                    if s.address >= ADDR_BLOCK0 and s.address <= ADDR_BLOCK15:
                        s.block_we.value = 1

                    if s.address == ADDR_CTRL:
                        s.init_new.value = s.write_data[CTRL_INIT_BIT]
                        s.next_new.value = s.write_data[CTRL_NEXT_BIT]

                else:

                    if s.address >= ADDR_BLOCK0 and s.address <= ADDR_BLOCK15:
                        s.tmp_read_data.value = s.block_reg[s.address[0:4]]

                    if s.address >= ADDR_DIGEST0 and s.address <= ADDR_DIGEST4:
                        offset = (4 - (s.address - ADDR_DIGEST0)) * 32
                        s.tmp_read_data.value = s.digest_reg[offset : offset + 32]

                    if s.address == ADDR_NAME0:
                        s.tmp_read_data.value = CORE_NAME0

                    elif s.address == ADDR_NAME1:
                        s.tmp_read_data.value = CORE_NAME1

                    elif s.address == ADDR_VERSION:
                        s.tmp_read_data.value = CORE_VERSION

                    elif s.address == ADDR_CTRL:
                        s.tmp_read_data.value = concat(Bits(30, 0), s.next_reg, s.init_reg)

                    elif s.address == ADDR_STATUS:
                        s.tmp_read_data.value = concat(Bits(30, 0), s.digest_valid_reg, s.ready_reg)

                    else:
                        s.tmp_error.value = 1




