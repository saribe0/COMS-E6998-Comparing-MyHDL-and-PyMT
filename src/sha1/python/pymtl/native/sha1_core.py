from pymtl import *
from sha1_w_mem import sha1_w_mem

class sha1_core( Model ):

	H0_0 = 0x67452301 	# intbv(1732584193)[32:] 	# 320x67452301
	H0_1 = 0xefcdab89 	# intbv(4023233417)[32:] 	# 320xefcdab89
	H0_2 = 0x98badcfe 	# intbv(2562383102)[32:] 	# 320x98badcfe
	H0_3 = 0x10325476 	# intbv(271733878)[32:] 	# 320x10325476
	H0_4 = 0xc3d2e1f0  	# intbv(3285377520)[32:] 	# 320xc3d2e1f0

	SHA1_ROUNDS = 79

	CTRL_IDLE   = 0
	CTRL_ROUNDS = 1
	CTRL_DONE   = 2

	# Constructor
	def __init__( s ):

		s.init 	  = InPort (Bits(1))
		s.next 	  = InPort (Bits(1))

		s.block 	 = InPort (Bits(512))
		s.ready 	 = OutPort(Bits(1))
		s.digest     = OutPort(Bits(160))
		s.digest_valid	 = OutPort(Bits(1))

		s.a_reg	= Wire(Bits(32))
		s.a_new	= Wire(Bits(32))
		s.b_reg	= Wire(Bits(32))
		s.b_new	= Wire(Bits(32))
		s.c_reg	= Wire(Bits(32))
		s.c_new	= Wire(Bits(32))
		s.d_reg	= Wire(Bits(32))
		s.d_new	= Wire(Bits(32))
		s.e_reg	= Wire(Bits(32))
		s.e_new	= Wire(Bits(32))
		s.a_e_we 	= Wire(Bits(1))

		s.H0_reg	= Wire(Bits(32))
		s.H0_new	= Wire(Bits(32))
		s.H1_reg	= Wire(Bits(32))
		s.H1_new	= Wire(Bits(32))
		s.H2_reg	= Wire(Bits(32))
		s.H2_new	= Wire(Bits(32))
		s.H3_reg	= Wire(Bits(32))
		s.H3_new	= Wire(Bits(32))
		s.H4_reg	= Wire(Bits(32))
		s.H4_new	= Wire(Bits(32))
		s.H_we		= Wire(Bits(1))

		s.round_ctr_reg = Wire(Bits(7))
		s.round_ctr_new = Wire(Bits(7))
		s.round_ctr_we  = Wire(Bits(1))
		s.round_ctr_inc = Wire(Bits(1))
		s.round_ctr_rst = Wire(Bits(1))

		s.digest_valid_reg = Wire(Bits(1))
		s.digest_valid_new = Wire(Bits(1))
		s.digest_valid_we  = Wire(Bits(1))

		s.sha1_ctrl_reg = Wire(Bits(2))
		s.sha1_ctrl_new = Wire(Bits(2))
		s.sha1_ctrl_we  = Wire(Bits(1))

		s.digest_init	= Wire(Bits(1))
		s.digest_update	= Wire(Bits(1))
		s.state_init	= Wire(Bits(1))
		s.state_update	= Wire(Bits(1))
		s.first_block	= Wire(Bits(1))
		s.ready_flag	= Wire(Bits(1))
		s.w_init		= Wire(Bits(1))
		s.w_next		= Wire(Bits(1))
		s.w 			= Wire(Bits(32))


		# Intantiate the memories
		s.w_mem_inst = sha1_w_mem()
		s.connect(s.block, s.w_mem_inst.block)
		s.connect(s.w_init, s.w_mem_inst.init)
		s.connect(s.w_next, s.w_mem_inst.next)
		s.connect(s.w, s.w_mem_inst.w)


		@s.combinational
		def logic():
			s.ready.value = s.ready_flag
			s.digest.value = concat(s.H0_reg, s.H1_reg, s.H2_reg, s.H3_reg, s.H4_reg)
			s.digest_valid.value = s.digest_valid_reg


		@s.tick_rtl
		def reg_update():
			if not s.reset_n:
				s.a_reg.next            = 0
				s.b_reg.next            = 0
				s.c_reg.next            = 0
				s.d_reg.next            = 0
				s.e_reg.next            = 0
				s.H0_reg.next           = 0
				s.H1_reg.next           = 0
				s.H2_reg.next           = 0
				s.H3_reg.next           = 0
				s.H4_reg.next           = 0
				s.digest_valid_reg.next = 0
				s.round_ctr_reg.next    = 0
				s.sha1_ctrl_reg.next    = CTRL_IDLE

			else:
				if s.a_e_we:
					s.a_reg.next = s.a_new
					s.b_reg.next = s.b_new
					s.c_reg.next = s.c_new
					s.d_reg.next = s.d_new
					s.e_reg.next = s.e_new

				if H_we:
					s.H0_reg.next = s.H0_new
					s.H1_reg.next = s.H1_new
					s.H2_reg.next = s.H2_new
					s.H3_reg.next = s.H3_new
					s.H4_reg.next = s.H4_new

				if s.round_ctr_we:
					s.round_ctr_reg.next = s.round_ctr_new

				if s.digest_valid_we:
					s.digest_valid_reg.next = s.digest_valid_new

				if s.sha1_ctrl_we:
					s.sha1_ctrl_reg.next = s.sha1_ctrl_new


		@s.combinational
		def digest_logic():
			s.H0_new.value = 0
			s.H1_new.value = 0
			s.H2_new.value = 0
			s.H3_new.value = 0
			s.H4_new.value = 0
			s.H_we.value = 0

			if s.digest_init:
				s.H0_new.value = H0_0
				s.H1_new.value = H0_1
				s.H2_new.value = H0_2
				s.H3_new.value = H0_3
				s.H4_new.value = H0_4
				s.H_we.value = 1

			if s.digest_update:
				s.H0_new.value = s.H0_reg + s.a_reg
				s.H1_new.value = s.H1_reg + s.b_reg
				s.H2_new.value = s.H2_reg + s.c_reg
				s.H3_new.value = s.H3_reg + s.d_reg
				s.H4_new.value = s.H4_reg + s.e_reg
				s.H_we.value = 1


		@s.combinational
		def state_logic():
			a5 = Bits(32)
			f  = Bits(32)
			k  = Bits(32)
			t  = Bits(32)

			a5 = 0
			f = 0
			k = 0
			t = 0
			s.a_new.value = 0
			s.b_new.value = 0
			s.c_new.value = 0
			s.d_new.value = 0
			s.e_new.value = 0
			s.a_e_we.value = 0

			if s.state_init:
				if s.first_block:
					s.a_new.value = H0_0
					s.b_new.value = H0_1
					s.c_new.value = H0_2
					s.d_new.value = H0_3
					s.e_new.value = H0_4
					s.a_e_we.value = 1
				else:
					s.a_new.value = s.H0_reg
					s.b_new.value = s.H1_reg
					s.c_new.value = s.H2_reg
					s.d_new.value = s.H3_reg
					s.e_new.value = s.H4_reg
					s.a_e_we.value = 1

			if s.state_update:
				if s.round_ctr_reg <= 19:
					k = 0x5a827999
					f = ((s.b_reg & s.c_reg) ^ (~s.b_reg & s.d_reg))

				elif ((s.round_ctr_reg >= 20) and (s.round_ctr_reg <= 39)):
					k = 0x6ed9eba1
					f = s.b_reg ^ s.c_reg ^ s.d_reg

				elif ((s.round_ctr_reg >= 40) and (s.round_ctr_reg <= 59)):
					k = 0x8f1bbcdc
			  		f = ((s.b_reg | s.c_reg) ^ (s.b_reg | s.d_reg) ^ (s.c_reg | s.d_reg))

			  	elif (s.round_ctr_reg >= 60):
			  		k = 0xca62c1d6
					f = s.b_reg ^ s.c_reg ^ s.d_reg

				a5 = concat(s.a_reg[27 : 0], s.a_reg[32 : 27])
				t = a5 + s.e_reg + f + k + s.w

				s.a_new.value  = t
				s.b_new.value  = s.a_reg
				s.c_new.value  = concat(s.b_reg[2 : 0], s.b_reg[32 : 2])
				s.d_new.value  = s.c_reg
				s.e_new.value  = s.d_reg
				s.a_e_we.value = 1


		@s.combinational
		def round_ctr():
			s.round_ctr_new.value = 0
			s.round_ctr_we.value = 0

			if s.round_ctr_rst:
				s.round_ctr_new.value = 0
				s.round_ctr_we.value = 1

			if s.round_ctr_inc:
				s.round_ctr_new.value = s.round_ctr_reg + 1
				s.round_ctr_we.value = 1


		@s.combinational
		def sha1_ctrl_fsm():
			s.digest_init.value      = 0
			s.digest_update.value    = 0
			s.state_init.value       = 0
			s.state_update.value     = 0
			s.first_block.value      = 0
			s.ready_flag.value       = 0
			s.w_init.value           = 0
			s.w_next.value           = 0
			s.round_ctr_inc.value    = 0
			s.round_ctr_rst.value    = 0
			s.digest_valid_new.value = 0
			s.digest_valid_we.value  = 0
			s.sha1_ctrl_new.value    = CTRL_IDLE
			s.sha1_ctrl_we.value     = 0

			if s.sha1_ctrl_reg == CTRL_IDLE:

				s.ready_flag.value = 1

				if s.init:
					s.digest_init.value      = 1
					s.w_init.value           = 1
					s.state_init.value       = 1
					s.first_block.value      = 1
					s.round_ctr_rst.value    = 1
					s.digest_valid_new.value = 0
					s.digest_valid_we.value  = 1
					s.sha1_ctrl_new.value    = CTRL_ROUNDS
					s.sha1_ctrl_we.value     = 1

				if s.next:
					s.w_init.value           = 1
					s.state_init.value       = 1
					s.round_ctr_rst.value    = 1
					s.digest_valid_new.value = 0
					s.digest_valid_we.value  = 1
					s.sha1_ctrl_new.value    = CTRL_ROUNDS
					s.sha1_ctrl_we.value     = 1

			elif s.sha1_ctrl_reg == CTRL_ROUNDS:
				s.state_update.value = 1
				s.round_ctr_inc.value = 1
				s.w_next.value = 1

				if s.round_ctr_reg.value == SHA1_ROUNDS:
					s.sha1_ctrl_new.value = CTRL_DONE
					s.sha1_ctrl_we.value = 1

			elif s.sha1_ctrl_reg == CTRL_DONE:
				s.digest_update.value = 1
				s.digest_valid_new.value = 1
				s.digest_valid_we.value = 1
				s.sha1_ctrl_new.value = CTRL_IDLE
				s.sha1_ctrl_we.value = 1









