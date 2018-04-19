from myhdl import *
from sha1_w_mem import sha1_w_mem

def sha1_core(clk, reset_n, init, next, block, ready, digest, digest_valid):

	##----------------------------------------------------------------
	## Internal constant and definitions.
	##----------------------------------------------------------------
	H0_0 = 0x67452301 	# intbv(1732584193)[32:] 	# 320x67452301
	H0_1 = 0xefcdab89 	# intbv(4023233417)[32:] 	# 320xefcdab89
	H0_2 = 0x98badcfe 	# intbv(2562383102)[32:] 	# 320x98badcfe
	H0_3 = 0x10325476 	# intbv(271733878)[32:] 	# 320x10325476
	H0_4 = 0xc3d2e1f0  	# intbv(3285377520)[32:] 	# 320xc3d2e1f0

	SHA1_ROUNDS = 79

	CTRL_IDLE   = 0
	CTRL_ROUNDS = 1
	CTRL_DONE   = 2


	##----------------------------------------------------------------
	## Registers including update variables and write enable.
	##----------------------------------------------------------------
	a_reg	= Signal(intbv()[32:])
	a_new	= Signal(intbv()[32:])
	b_reg	= Signal(intbv()[32:])
	b_new	= Signal(intbv()[32:])
	c_reg	= Signal(intbv()[32:])
	c_new	= Signal(intbv()[32:])
	d_reg	= Signal(intbv()[32:])
	d_new	= Signal(intbv()[32:])
	e_reg	= Signal(intbv()[32:])
	e_new	= Signal(intbv()[32:])	
	a_e_we 	= Signal(bool())

	H0_reg	= Signal(modbv()[32:])	
	H0_new	= Signal(modbv()[32:])	
	H1_reg	= Signal(modbv()[32:])	
	H1_new	= Signal(modbv()[32:])	
	H2_reg	= Signal(modbv()[32:])	
	H2_new	= Signal(modbv()[32:])	
	H3_reg	= Signal(modbv()[32:])	
	H3_new	= Signal(modbv()[32:])	
	H4_reg	= Signal(modbv()[32:])	
	H4_new	= Signal(modbv()[32:])	
	H_we	= Signal(bool())

	round_ctr_reg = Signal(modbv()[7:])
	round_ctr_new = Signal(modbv()[7:])
	round_ctr_we  = Signal(bool())
	round_ctr_inc = Signal(bool())
	round_ctr_rst = Signal(bool())

	digest_valid_reg = Signal(bool())
	digest_valid_new = Signal(bool())
	digest_valid_we  = Signal(bool())

	sha1_ctrl_reg = Signal(intbv()[2:])	
	sha1_ctrl_new = Signal(intbv()[2:])	
	sha1_ctrl_we  = Signal(bool())


	##----------------------------------------------------------------
	## Wires.
	##----------------------------------------------------------------
	digest_init	= Signal(bool())
	digest_update	= Signal(bool())
	state_init	= Signal(bool())
	state_update	= Signal(bool())
	first_block	= Signal(bool())
	ready_flag	= Signal(bool())
	w_init		= Signal(bool())
	w_next		= Signal(bool())
	w = Signal(intbv()[32:])


	##----------------------------------------------------------------
	## Module instantiantions.
	##----------------------------------------------------------------
	w_mem_inst = sha1_w_mem(clk, reset_n, block, w_init, w_next, w)


	##----------------------------------------------------------------
	## Concurrent connectivity for ports etc.
	##----------------------------------------------------------------
	@always_comb
	def logic():
		ready.next = ready_flag
		digest.next[160:128] = H0_reg
		digest.next[128: 96] = H1_reg
		digest.next[96 : 64] = H2_reg
		digest.next[64 : 32] = H3_reg
		digest.next[32 :  0] = H4_reg
		digest_valid.next = digest_valid_reg

	##----------------------------------------------------------------
	## reg_update
	## Update functionality for all registers in the core.
	## All registers are positive edge triggered with
	## asynchronous active low reset.
	##----------------------------------------------------------------
	@always(clk.posedge, reset_n.negedge)
	def reg_update():
		if not reset_n:
			a_reg.next[:] = 0 
			b_reg.next[:] = 0 
			c_reg.next[:] = 0 
			d_reg.next[:] = 0 
			e_reg.next[:] = 0 
			H0_reg.next[:] = 0 
			H1_reg.next[:] = 0 
			H2_reg.next[:] = 0 
			H3_reg.next[:] = 0 
			H4_reg.next[:] = 0 
			digest_valid_reg.next = 0
			round_ctr_reg.next[:] = 0
			sha1_ctrl_reg.next[:] = CTRL_IDLE
		else:
			if a_e_we:
				a_reg.next[:] = a_new
				b_reg.next[:] = b_new
				c_reg.next[:] = c_new
				d_reg.next[:] = d_new
				e_reg.next[:] = e_new

			if H_we:
				H0_reg.next[:] = H0_new
				H1_reg.next[:] = H1_new
				H2_reg.next[:] = H2_new
				H3_reg.next[:] = H3_new
				H4_reg.next[:] = H4_new

			if round_ctr_we:
				round_ctr_reg.next[:] = round_ctr_new

			if digest_valid_we:
				digest_valid_reg.next = digest_valid_new

			if sha1_ctrl_we:
				sha1_ctrl_reg.next[:] = sha1_ctrl_new


	##----------------------------------------------------------------
	## digest_logic
	##
	## The logic needed to init as well as update the digest.
	##----------------------------------------------------------------
	#@always(digest_init, digest_update, H0_new, H1_new, H2_new, H3_new, H4_new, H_we, H0_reg, H1_reg, H2_reg, H3_reg, H4_reg, a_reg, b_reg, c_reg, d_reg, e_reg)
	@always(digest_init, digest_update, H0_reg, H1_reg, H2_reg, H3_reg, H4_reg, a_reg, b_reg, c_reg, d_reg, e_reg)
	def digest_logic():
		H0_new.next[:] = 0
		H1_new.next[:] = 0
		H2_new.next[:] = 0
		H3_new.next[:] = 0
		H4_new.next[:] = 0
		H_we.next = 0

		if (digest_init):
			H0_new.next[:] = H0_0
			H1_new.next[:] = H0_1
			H2_new.next[:] = H0_2
			H3_new.next[:] = H0_3
			H4_new.next[:] = H0_4
			H_we.next = 1

		if (digest_update):
			H0_new.next[:] = H0_reg + a_reg
			H1_new.next[:] = H1_reg + b_reg
			H2_new.next[:] = H2_reg + c_reg
			H3_new.next[:] = H3_reg + d_reg
			H4_new.next[:] = H4_reg + e_reg
			H_we.next = 1

	##----------------------------------------------------------------
	## state_logic
	##
	## The logic needed to init as well as update the state during
	## round processing.
	##----------------------------------------------------------------
	#@always(a_new, b_new, c_new, d_new, e_new, a_e_we, state_init, first_block, H0_reg, H1_reg, H2_reg, 
	#	H3_reg, H4_reg, round_ctr_reg, a_reg, b_reg, c_reg, d_reg, e_reg, w, state_update)
	@always(state_init, first_block, H0_reg, H1_reg, H2_reg,
                H3_reg, H4_reg, round_ctr_reg, a_reg, b_reg, c_reg, d_reg, e_reg, w, state_update)
	def state_logic():
		a5 = modbv(0)[32:]
		f  = modbv(0)[32:]
		k  = modbv(0)[32:]
		t  = modbv(0)[32:]

		a_new.next[:] = 0
		b_new.next[:] = 0
		c_new.next[:] = 0
		d_new.next[:] = 0
		e_new.next[:] = 0
		a_e_we.next = 0

		if state_init:
			if first_block:
				a_new.next[:]  = H0_0
				b_new.next[:]  = H0_1
				c_new.next[:]  = H0_2
				d_new.next[:]  = H0_3
				e_new.next[:]  = H0_4
				a_e_we.next = 1
			else:
				a_new.next[:]  = H0_reg
				b_new.next[:]  = H1_reg
				c_new.next[:]  = H2_reg
				d_new.next[:]  = H3_reg
				e_new.next[:]  = H4_reg
				a_e_we.next = 1

		if state_update:
			if round_ctr_reg <= 19:
				k[:] = 0x5a827999
				f[:] =  ((b_reg & c_reg) ^ (~b_reg & d_reg))
			elif ((round_ctr_reg >= 20) and (round_ctr_reg <= 39)):
				k[:] = 0x6ed9eba1
				f[:] = b_reg ^ c_reg ^ d_reg
			elif ((round_ctr_reg >= 40) and (round_ctr_reg <= 59)):
				k[:] = 0x8f1bbcdc
				f[:] = ((b_reg | c_reg) ^ (b_reg | d_reg) ^ (c_reg | d_reg))
			elif round_ctr_reg >= 60:
				k[:] = 0xca62c1d6
				f[:] = b_reg ^ c_reg ^ d_reg

			a5[32:5] = a_reg[27: 0]
			a5[5 :0] = a_reg[32:27]
			t[:] = a5 + e_reg + f + k + w

			a_new.next[:]  = t
			b_new.next[:]  = a_reg
			c_new.next[32:30] = b_reg[2 : 0]
			c_new.next[30: 0] = b_reg[32 : 2]
			d_new.next[:]  = c_reg
			e_new.next[:]  = d_reg
			a_e_we.next = 1


	##----------------------------------------------------------------
	## round_ctr
	##
	## Update logic for the round counter, a monotonically
	## increasing counter with reset.
	##----------------------------------------------------------------
	#@always(round_ctr_new, round_ctr_we, round_ctr_rst, round_ctr_inc, round_ctr_reg)
	@always(round_ctr_rst, round_ctr_inc, round_ctr_reg)
	def round_ctr():
		round_ctr_new.next[:] = 0
		round_ctr_we.next  = 0

		if (round_ctr_rst):
			round_ctr_new.next[:] = 0
			round_ctr_we.next  = 1

		if (round_ctr_inc):
			round_ctr_new.next[:] = round_ctr_reg + 0b1
			round_ctr_we.next  = 1


	##----------------------------------------------------------------
	## sha1_ctrl_fsm
	## Logic for the state machine controlling the core behaviour.
	##----------------------------------------------------------------
	#@always(digest_init, digest_update, state_init, state_update, first_block, ready_flag, w_init, 
	#	w_next, round_ctr_inc, round_ctr_rst, digest_valid_new, digest_valid_we, sha1_ctrl_new, 
	#	sha1_ctrl_we, sha1_ctrl_reg, init, round_ctr_reg, next)
	@always(sha1_ctrl_reg, init, round_ctr_reg, next)
	def sha1_ctrl_fsm():
		digest_init.next      = 0
		digest_update.next    = 0
		state_init.next       = 0
		state_update.next     = 0
		first_block.next      = 0
		ready_flag.next       = 0
		w_init.next           = 0
		w_next.next           = 0
		round_ctr_inc.next    = 0
		round_ctr_rst.next    = 0
		digest_valid_new.next = 0
		digest_valid_we.next  = 0
		sha1_ctrl_new.next[:] = CTRL_IDLE
		sha1_ctrl_we.next     = 0
		if sha1_ctrl_reg == CTRL_IDLE:

			ready_flag.next = 1
			if (init):
				digest_init.next      = 1
				w_init.next           = 1
				state_init.next       = 1
				first_block.next      = 1
				round_ctr_rst.next    = 1
				digest_valid_new.next = 0
				digest_valid_we.next  = 1
				sha1_ctrl_new.next[:] = CTRL_ROUNDS
				sha1_ctrl_we.next     = 1

			if (next):
				w_init.next           = 1
				state_init.next       = 1
				round_ctr_rst.next    = 1
				digest_valid_new.next = 0
				digest_valid_we.next  = 1
				sha1_ctrl_new.next[:]    = CTRL_ROUNDS
				sha1_ctrl_we.next     = 1

		elif sha1_ctrl_reg == CTRL_ROUNDS:
				state_update.next   = 1
				round_ctr_inc.next  = 1
				w_next.next         = 1

				if (round_ctr_reg == SHA1_ROUNDS):
					sha1_ctrl_new.next[:]  = CTRL_DONE
					sha1_ctrl_we.next   = 1


		elif sha1_ctrl_reg == CTRL_DONE:
				digest_update.next     = 1
				digest_valid_new.next  = 1
				digest_valid_we.next   = 1
				sha1_ctrl_new.next[:]     = CTRL_IDLE
				sha1_ctrl_we.next      = 1

		else:
			pass

	return w_mem_inst, logic, reg_update, digest_logic, state_logic, round_ctr, sha1_ctrl_fsm

##======================================================================
## EOF sha1_core.v
##======================================================================
