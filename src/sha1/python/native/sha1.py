from myhdl import *
from sha1_core import sha1_core


def sha1(clk, reset_n, cs, we, address, write_data, read_data, error):

	##----------------------------------------------------------------
	## Internal constant and parameter definitions.
	##----------------------------------------------------------------
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


	##----------------------------------------------------------------
	## Registers including update variables and write enable.
	##----------------------------------------------------------------
	init_reg = Signal(bool())
	init_new = Signal(bool())

	next_reg = Signal(bool())
	next_new = Signal(bool())

	ready_reg = Signal(bool())

	block_reg = [Signal(intbv()[32:]) for n in range(16)]
	block_we  = Signal(bool())

	digest_reg = Signal(intbv()[160:])

	digest_valid_reg = Signal(bool())


	##----------------------------------------------------------------
	## Wires.
	##----------------------------------------------------------------
	core_ready = Signal(bool())
	core_block = Signal(intbv()[512:])
	core_digest = Signal(intbv()[160:])
	core_digest_valid = Signal(bool())

	tmp_read_data = Signal(intbv()[32:])
	tmp_error = Signal(bool())


	##----------------------------------------------------------------
	## Concurrent connectivity for ports etc.
	##----------------------------------------------------------------
	@always_comb
	def logic():
		core_block.next[512:480] = block_reg[0]
		core_block.next[480:448] = block_reg[1]
		core_block.next[448:416] = block_reg[2]
		core_block.next[416:384] = block_reg[3]
		core_block.next[384:352] = block_reg[4]
		core_block.next[352:320] = block_reg[5]
		core_block.next[320:288] = block_reg[6]
		core_block.next[288:256] = block_reg[7]
		core_block.next[256:224] = block_reg[8]
		core_block.next[224:192] = block_reg[9]
		core_block.next[192:160] = block_reg[10]
		core_block.next[160:128] = block_reg[11]
		core_block.next[128: 96] = block_reg[12]
		core_block.next[96 : 64] = block_reg[13]
		core_block.next[64 : 32] = block_reg[14]
		core_block.next[32 :  0] = block_reg[15]
		read_data.next[:] = tmp_read_data
		error.next = tmp_error


	##----------------------------------------------------------------
	## core instantiation.
	##----------------------------------------------------------------
	core = sha1_core(clk, reset_n, init_reg, next_reg, core_block, core_ready, core_digest, core_digest_valid)


	##----------------------------------------------------------------
	## reg_update
	## Update functionality for all registers in the core.
	## All registers are positive edge triggered with
	## asynchronous active low reset.
	##----------------------------------------------------------------
	@always(clk.posedge, reset_n.negedge)
	def reg_update():

		if not reset_n:
			init_reg.next = 0
			next_reg.next = 0
			ready_reg.next = 0
			digest_reg.next[:] = 0
			digest_valid_reg.next = 0
		
			for i in range(16):
				block_reg[i].next[:] = 0
		
		else:
			ready_reg.next = core_ready
			digest_valid_reg.next = core_digest_valid
			init_reg.next = init_new
			next_reg.next = next_new
			if block_we:
				block_reg[int(address[4:])].next[:] = write_data

			if core_digest_valid:
				digest_reg.next[:] = core_digest
		
	##----------------------------------------------------------------
	## api
	##
	## The interface command decoding logic.
	##----------------------------------------------------------------
	#@always(init_new, next_new, block_we, tmp_read_data, tmp_error, address, cs, we, write_data, 
	#	block_reg[0], block_reg[1], block_reg[2], block_reg[3], block_reg[4], block_reg[5], 
	#	block_reg[6], block_reg[7], block_reg[8], block_reg[9], block_reg[10], block_reg[11],
        #        block_reg[12], block_reg[13], block_reg[14], block_reg[15], digest_reg, next_reg, init_reg,
	#	digest_valid_reg, ready_reg)
	@always(address, cs, we, write_data, 
                block_reg[0], block_reg[1], block_reg[2], block_reg[3], block_reg[4], block_reg[5], 
                block_reg[6], block_reg[7], block_reg[8], block_reg[9], block_reg[10], block_reg[11],
                block_reg[12], block_reg[13], block_reg[14], block_reg[15], digest_reg, next_reg, init_reg,
                digest_valid_reg, ready_reg)
	def api():
		init_new.next 		= 0
		next_new.next	 	= 0
		block_we.next	 	= 0
		tmp_read_data.next[:] 	= 0
		tmp_error.next    	= 0 
	 	
		if cs:
			# Write
			if we:
				if ((address >= ADDR_BLOCK0) and (address <= ADDR_BLOCK15)):
					block_we.next = 1;
				if (address == ADDR_CTRL):
					init_new.next = write_data[CTRL_INIT_BIT];
					next_new.next = write_data[CTRL_NEXT_BIT];
			# Read
			else:
				if ((address >= ADDR_BLOCK0) and (address <= ADDR_BLOCK15)):
					tmp_read_data.next[:] = block_reg[address[4 : 0]];
				if ((address >= ADDR_DIGEST0) and (address <= ADDR_DIGEST4)):
					if (address == 0x20):
						tmp_read_data.next[:] = digest_reg[160:128]
					if (address == 0x21):
                                                tmp_read_data.next[:] = digest_reg[128: 96]
					if (address == 0x22):
                                                tmp_read_data.next[:] = digest_reg[96 : 64]
					if (address == 0x23):
                                                tmp_read_data.next[:] = digest_reg[64 : 32]
					if (address == 0x24):
                                                tmp_read_data.next[:] = digest_reg[32 :  0];

				if address == ADDR_NAME0:
					tmp_read_data.next[:] = CORE_NAME0
				elif address == ADDR_NAME1:
					tmp_read_data.next[:] = CORE_NAME1
				elif address == ADDR_VERSION:
					tmp_read_data.next[:] = CORE_VERSION
				elif address == ADDR_CTRL:
					tmp_read_data.next[32:2] = 0
					tmp_read_data.next[2 :1] = next_reg
					tmp_read_data.next[1 :0] = init_reg
				elif address == ADDR_STATUS:
					tmp_read_data.next[32:2] = 0
					tmp_read_data.next[2 :1] = digest_valid_reg
					tmp_read_data.next[1 :0] = ready_reg
				else:
					tmp_error.next = 1
		
	return core, api, reg_update, logic
##======================================================================
## EOF sha1.v
##======================================================================
