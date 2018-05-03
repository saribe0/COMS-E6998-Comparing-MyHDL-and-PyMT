from myhdl import *

def ram(clk, data_a, data_b, addr_a, addr_b, we_a, we_b, q_a, q_b):

	DATA_WIDTH = 8
	ADDR_WIDTH = 10

	ram = [Signal(intbv()[DATA_WIDTH:]) for _ in range(2**ADDR_WIDTH)]

	@always(clk.posedge)
	def port_a():
		if we_a:
			ram[addr_a].next[:] = data_a
			q_a.next[:] = data_a
		else:
			q_a.next[:] = ram[addr_a]

	@always(clk.posedge)
	def port_b():
		if we_b:
			ram[addr_b].next[:] = data_b
			q_b.next[:] = data_a
		else:
			q_b.next[:] = ram[addr_b]
			