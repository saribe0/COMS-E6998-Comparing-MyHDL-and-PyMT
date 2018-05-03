from pymtl import *

class ram( Model ):

	# Constructor
	def __init__( s ):

		s.DATA_WIDTH = 8
		s.ADDR_WIDTH = 10

		s.data_a = InPort (Bits(s.DATA_WIDTH))
		s.data_b = InPort (Bits(s.DATA_WIDTH))

		s.addr_a = InPort (Bits(s.ADDR_WIDTH))
		s.addr_b = InPort (Bits(s.ADDR_WIDTH))

		s.we_a   = InPort (Bits(1))
		s.we_b   = InPort (Bits(1))

		s.q_a    = OutPort(Bits(s.DATA_WIDTH))
		s.q_b    = OutPort(Bits(s.DATA_WIDTH))

		s.ram = [Wire(Bits(s.DATA_WIDTH)) for _ in range(2**s.ADDR_WIDTH)]

		@s.tick_rtl
		def port_a():
			if s.we_a:
				s.ram[s.addr_a].next = s.data_a
				s.q_a.next 			 = s.data_a
			else:
				s.q_a.next = s.ram[s.addr_a]

		@s.tick_rtl
		def port_b():
			if s.we_b:
				s.ram[s.addr_b].next = s.data_b
				s.q_b.next 			 = s.data_b
			else:
				s.q_b.next = s.ram[s.addr_b]
