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

class testbench( Model ):

	def __init__( s ):

		s.cycle_ctr = Wire(Bits(32)) 
		s.error_ctr = Wire(Bits(32))
		s.tc_ctr    = Wire(Bits(32))

		s.tb_cs = Wire(Bits(1))
		s.tb_write_read = Wire(Bits(1))
		s.tb_address = Wire(Bits(8))
		s.tb_data_in = Wire(Bits(32))
		s.tb_data_out = Wire(Bits(32))
		s.tb_error = Wire(Bits(1))

		s.read_data = Wire(Bits(32))
		s.digest_data = Wire(Bits(160))


		s.sha1 = sha1()
		connect(s.tb_cs, s.sha1.cs)
		connect(s.tb_write_read, s.sha1.we)
		connect(s.tb_address, s.sha1.address)
		connect(s.tb_data_in, s.sha1.write_data)
		connect(s.tb_data_out, s.sha1.read_data)
		connect(s.tb_error, s.sha1.error)


		@s.tick_rtl
		def sys_monitor():
			s.cycle_ctr.next = s.cycle_ctr + 1


		def init_sim():
			s.cycle_ctr.value = 0
			s.error_ctr.value = 0
			s.tc_ctr.value = 0

			s.tb_cs.value = 0
			s.tb_write_read.value = 0
			s.tb_address.value = 0
			s.tb_data_in.value = 0

		def wait_ready():
			s.read_data.value = 0

			while s.read_data == 0:
				read_word(ADDR_STATUS)

		def read_word():
			s.tb_address.next = address
			s.tb_cs.next = 1
			s.tb_write_read.next = 0

			s.read_data = s.tb_data_out




def test_bench():
	sim = SimulationTool( model )
	sim.reset



















