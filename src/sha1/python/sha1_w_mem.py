from myhdl import *

def sha1_w_mem(clk, reset_n, block, init, next, w):

	##----------------------------------------------------------------
	## Internal constant and parameter definitions.
	##----------------------------------------------------------------
	SHA1_ROUNDS = 79

	CTRL_IDLE   = 0b0 # intbv(0)[1:]
	CTRL_UPDATE = 0b1 # intbv(1)[1:]

	##----------------------------------------------------------------
	## Registers including update variables and write enable.
	##----------------------------------------------------------------
	w_mem = [Signal(intbv()[32:]) for n in range(16)]
	w_mem00_new = Signal(intbv()[32:])
	w_mem01_new = Signal(intbv()[32:])
	w_mem02_new = Signal(intbv()[32:])
	w_mem03_new = Signal(intbv()[32:])
	w_mem04_new = Signal(intbv()[32:])
	w_mem05_new = Signal(intbv()[32:])
	w_mem06_new = Signal(intbv()[32:])
	w_mem07_new = Signal(intbv()[32:])
	w_mem08_new = Signal(intbv()[32:])
	w_mem09_new = Signal(intbv()[32:])
	w_mem10_new = Signal(intbv()[32:])
	w_mem11_new = Signal(intbv()[32:])
	w_mem12_new = Signal(intbv()[32:])
	w_mem13_new = Signal(intbv()[32:])
	w_mem14_new = Signal(intbv()[32:])
	w_mem15_new = Signal(intbv()[32:])
	w_mem_we    = Signal(bool())

	w_ctr_reg = Signal(modbv()[7:])
	w_ctr_new = Signal(modbv()[7:])
	w_ctr_we  = Signal(bool())
	w_ctr_inc = Signal(bool())
	w_ctr_rst = Signal(bool())

	sha1_w_mem_ctrl_reg = Signal(bool())
	sha1_w_mem_ctrl_new = Signal(bool())
	sha1_w_mem_ctrl_we  = Signal(bool())


	##----------------------------------------------------------------
	## Wires.
	##----------------------------------------------------------------
	w_tmp = Signal(intbv()[32:])
	w_new = Signal(intbv()[32:])


	##----------------------------------------------------------------
	## Concurrent connectivity for ports etc.
	##----------------------------------------------------------------
	@always_comb
	def logic():
		w.next[:] = w_tmp
	

	##----------------------------------------------------------------
	## reg_update
	##
	## Update functionality for all registers in the core.
	## All registers are positive edge triggered with
	## asynchronous active low reset.
	##----------------------------------------------------------------
	@always(clk.posedge, reset_n.negedge)
	def reg_update():

		if not reset_n:
			for i in range(16):
				w_mem[i].next[:] = 0
			sha1_w_mem_ctrl_reg.next = CTRL_IDLE

		else:
			if (w_mem_we):
				w_mem[0].next[:] = w_mem00_new
				w_mem[1].next[:] = w_mem01_new
				w_mem[2].next[:] = w_mem02_new
				w_mem[3].next[:] = w_mem03_new
				w_mem[4].next[:] = w_mem04_new
				w_mem[5].next[:] = w_mem05_new
				w_mem[6].next[:] = w_mem06_new
				w_mem[7].next[:] = w_mem07_new
				w_mem[8].next[:] = w_mem08_new
				w_mem[9].next[:] = w_mem09_new
				w_mem[10].next[:] = w_mem10_new
				w_mem[11].next[:] = w_mem11_new
				w_mem[12].next[:] = w_mem12_new
				w_mem[13].next[:] = w_mem13_new
				w_mem[14].next[:] = w_mem14_new
				w_mem[15].next[:] = w_mem15_new

			if (w_ctr_we):
				w_ctr_reg.next[:] = w_ctr_new

			if (sha1_w_mem_ctrl_we):
				sha1_w_mem_ctrl_reg.next = sha1_w_mem_ctrl_new
	
	##----------------------------------------------------------------
	## select_w
	##
	## W word selection logic. Returns either directly from the
	## memory or the next w value calculated.
	##----------------------------------------------------------------
	@always(w_ctr_reg, w_tmp, w_new, w_mem[0], w_mem[1], w_mem[2], w_mem[3], w_mem[4], w_mem[5], w_mem[6], w_mem[7], 
		w_mem[8], w_mem[9], w_mem[10], w_mem[11], w_mem[12], w_mem[13], w_mem[14], w_mem[15])
	def select_w():
		if (w_ctr_reg < 16):
			w_tmp.next[:] = w_mem[int(w_ctr_reg[4:])]
		else:
			w_tmp.next[:] = w_new


	##----------------------------------------------------------------
	## w_mem_update_logic
	##
	## Update logic for the W memory. This is where the scheduling
	## based on a sliding window is implemented.
	##----------------------------------------------------------------
	@always(w_mem00_new, w_mem01_new, w_mem02_new, w_mem03_new, w_mem04_new,
			w_mem05_new, w_mem06_new, w_mem07_new, w_mem08_new, w_mem09_new, w_mem10_new, w_mem11_new, 
			w_mem12_new, w_mem13_new, w_mem14_new, w_mem15_new, w_mem_we, w_new, init, block, w_ctr_reg,
			w_mem[1], w_mem[2], w_mem[3], w_mem[4], w_mem[5], w_mem[6], w_mem[7],
	                w_mem[8], w_mem[9], w_mem[10], w_mem[11], w_mem[12], w_mem[13], w_mem[14], w_mem[15])
	def w_mem_update_logic():
			
			w_0  = intbv(0)[32:]
			w_2  = intbv(0)[32:]
			w_8  = intbv(0)[32:]
			w_13 = intbv(0)[32:]
			w_16 = intbv(0)[32:]
			
			w_mem00_new.next[:] = 0
			w_mem01_new.next[:] = 0
			w_mem02_new.next[:] = 0
			w_mem03_new.next[:] = 0
			w_mem04_new.next[:] = 0
			w_mem05_new.next[:] = 0
			w_mem06_new.next[:] = 0
			w_mem07_new.next[:] = 0
			w_mem08_new.next[:] = 0
			w_mem09_new.next[:] = 0
			w_mem10_new.next[:] = 0
			w_mem11_new.next[:] = 0
			w_mem12_new.next[:] = 0
			w_mem13_new.next[:] = 0
			w_mem14_new.next[:] = 0
			w_mem15_new.next[:] = 0
			w_mem_we.next  = 0

			w_0[:]   = w_mem[0]
			w_2[:]   = w_mem[2]
			w_8[:]   = w_mem[8]
			w_13[:]  = w_mem[13]
			w_16[:]  = w_13 ^ w_8 ^ w_2 ^ w_0
			w_new.next[32:1] = w_16[31: 0]
			w_new.next[1 :0] = w_16[32:31]
			
			if (init):
					w_mem00_new.next[:] = block[512 : 480]
					w_mem01_new.next[:] = block[480 : 448]
					w_mem02_new.next[:] = block[448 : 416]
					w_mem03_new.next[:] = block[416 : 384]
					w_mem04_new.next[:] = block[384 : 352]
					w_mem05_new.next[:] = block[352 : 320]
					w_mem06_new.next[:] = block[320 : 288]
					w_mem07_new.next[:] = block[288 : 256]
					w_mem08_new.next[:] = block[256 : 224]
					w_mem09_new.next[:] = block[224 : 192]
					w_mem10_new.next[:] = block[192 : 160]
					w_mem11_new.next[:] = block[160 : 128]
					w_mem12_new.next[:] = block[128 :  96]
					w_mem13_new.next[:] = block[96  :  64]
					w_mem14_new.next[:] = block[64  :  32]
					w_mem15_new.next[:] = block[32  :   0]
					w_mem_we.next   = 1

			elif (w_ctr_reg > 15):
					w_mem00_new.next[:] = w_mem[1]
					w_mem01_new.next[:] = w_mem[2]
					w_mem02_new.next[:] = w_mem[3]
					w_mem03_new.next[:] = w_mem[4]
					w_mem04_new.next[:] = w_mem[5]
					w_mem05_new.next[:] = w_mem[6]
					w_mem06_new.next[:] = w_mem[7]
					w_mem07_new.next[:] = w_mem[8]
					w_mem08_new.next[:] = w_mem[9]
					w_mem09_new.next[:] = w_mem[10]
					w_mem10_new.next[:] = w_mem[11]
					w_mem11_new.next[:] = w_mem[12]
					w_mem12_new.next[:] = w_mem[13]
					w_mem13_new.next[:] = w_mem[14]
					w_mem14_new.next[:] = w_mem[15]
					w_mem15_new.next[:] = w_new
					w_mem_we.next    = 1


	##----------------------------------------------------------------
	## w_ctr
	##
	## W schedule adress counter. Counts from 0x10 to 0x3f and
	## is used to expand the block into words.
	##----------------------------------------------------------------
	@always(w_ctr_new, w_ctr_we, w_ctr_rst, w_ctr_inc, w_ctr_reg)
	def w_ctr():
		w_ctr_new.next[:] = 0
		w_ctr_we.next  = 0
		if (w_ctr_rst):
			w_ctr_new.next[:] = 0
			w_ctr_we.next  = 1

		if (w_ctr_inc):
			w_ctr_new.next[:] = w_ctr_reg + 1
			w_ctr_we.next  = 1

	
	##----------------------------------------------------------------
	## sha1_w_mem_fsm
	##
	## Logic for the w shedule FSM.
	##----------------------------------------------------------------
	@always(w_ctr_rst, w_ctr_inc, sha1_w_mem_ctrl_new, sha1_w_mem_ctrl_we, sha1_w_mem_ctrl_reg, init, next, w_ctr_reg, )
	def sha1_w_mem_fsm():
		w_ctr_rst.next           = 0
		w_ctr_inc.next           = 0
		sha1_w_mem_ctrl_new.next = CTRL_IDLE
		sha1_w_mem_ctrl_we.next  = 0
		if sha1_w_mem_ctrl_reg == CTRL_IDLE:
			if (init):
				w_ctr_rst.next           = 1
				sha1_w_mem_ctrl_new.next = CTRL_UPDATE
				sha1_w_mem_ctrl_we.next  = 1

		elif sha1_w_mem_ctrl_reg == CTRL_UPDATE:
			if (next):
				w_ctr_inc.next = 1
			if (w_ctr_reg == SHA1_ROUNDS):
				sha1_w_mem_ctrl_new.next = CTRL_IDLE
				sha1_w_mem_ctrl_we.next  = 1
		else:
			pass
	
	return logic, reg_update, select_w, w_mem_update_logic, w_ctr, sha1_w_mem_fsm

##======================================================================
## sha1_w_mem.v
##======================================================================
