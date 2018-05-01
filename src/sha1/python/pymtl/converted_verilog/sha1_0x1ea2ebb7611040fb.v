//-----------------------------------------------------------------------------
// sha1_0x1ea2ebb7611040fb
//-----------------------------------------------------------------------------
// dump-vcd: False
// verilator-xinit: zeros
`default_nettype none
module sha1
(
  input  wire [   7:0] address,
  input  wire          clk,
  input  wire [   0:0] cs,
  output reg  [   0:0] error,
  output reg  [  31:0] read_data,
  input  wire [   0:0] reset,
  input  wire [   0:0] reset_n,
  input  wire [   0:0] we,
  input  wire [  31:0] write_data
);

  // wire declarations
  wire   [   0:0] core_ready;
  wire   [   0:0] core_digest_valid;
  wire   [ 159:0] core_digest;
  wire   [  31:0] block_reg$000;
  wire   [  31:0] block_reg$001;
  wire   [  31:0] block_reg$002;
  wire   [  31:0] block_reg$003;
  wire   [  31:0] block_reg$004;
  wire   [  31:0] block_reg$005;
  wire   [  31:0] block_reg$006;
  wire   [  31:0] block_reg$007;
  wire   [  31:0] block_reg$008;
  wire   [  31:0] block_reg$009;
  wire   [  31:0] block_reg$010;
  wire   [  31:0] block_reg$011;
  wire   [  31:0] block_reg$012;
  wire   [  31:0] block_reg$013;
  wire   [  31:0] block_reg$014;
  wire   [  31:0] block_reg$015;


  // register declarations
  reg    [   0:0] block_we;
  reg    [ 511:0] core_block;
  reg    [ 159:0] digest_reg;
  reg    [   0:0] digest_valid_reg;
  reg    [   0:0] init_new;
  reg    [   0:0] init_reg;
  reg    [   0:0] next_new;
  reg    [   0:0] next_reg;
  reg    [  15:0] offset__2;
  reg    [   0:0] ready_reg;
  reg    [   0:0] tmp_error;
  reg    [  31:0] tmp_read_data;

  // localparam declarations
  localparam ADDR_BLOCK0 = 16;
  localparam ADDR_BLOCK15 = 31;
  localparam ADDR_CTRL = 8;
  localparam ADDR_DIGEST0 = 32;
  localparam ADDR_DIGEST4 = 36;
  localparam ADDR_NAME0 = 0;
  localparam ADDR_NAME1 = 1;
  localparam ADDR_STATUS = 9;
  localparam ADDR_VERSION = 2;
  localparam CORE_NAME0 = 1936220465;
  localparam CORE_NAME1 = 538976288;
  localparam CORE_VERSION = 808334896;
  localparam CTRL_INIT_BIT = 0;
  localparam CTRL_NEXT_BIT = 1;

  // loop variable declarations
  integer ii;

  // core temporaries
  wire   [   0:0] core$clk;
  wire   [   0:0] core$init;
  wire   [   0:0] core$next_in;
  wire   [   0:0] core$reset;
  wire   [   0:0] core$reset_n;
  wire   [ 511:0] core$block;
  wire   [   0:0] core$ready;
  wire   [ 159:0] core$digest;
  wire   [   0:0] core$digest_valid;

  sha1_core_0x187abc469c6b3e24 core
  (
    .clk          ( core$clk ),
    .init         ( core$init ),
    .next_in      ( core$next_in ),
    .reset        ( core$reset ),
    .reset_n      ( core$reset_n ),
    .block        ( core$block ),
    .ready        ( core$ready ),
    .digest       ( core$digest ),
    .digest_valid ( core$digest_valid )
  );

  // signal connections
  assign core$block        = core_block;
  assign core$clk          = clk;
  assign core$init         = init_reg;
  assign core$next_in      = next_reg;
  assign core$reset        = reset;
  assign core$reset_n      = reset_n;
  assign core_digest       = core$digest;
  assign core_digest_valid = core$digest_valid;
  assign core_ready        = core$ready;

  // array declarations
  reg    [  31:0] block_reg[0:15];
  assign block_reg$000 = block_reg[  0];
  assign block_reg$001 = block_reg[  1];
  assign block_reg$002 = block_reg[  2];
  assign block_reg$003 = block_reg[  3];
  assign block_reg$004 = block_reg[  4];
  assign block_reg$005 = block_reg[  5];
  assign block_reg$006 = block_reg[  6];
  assign block_reg$007 = block_reg[  7];
  assign block_reg$008 = block_reg[  8];
  assign block_reg$009 = block_reg[  9];
  assign block_reg$010 = block_reg[ 10];
  assign block_reg$011 = block_reg[ 11];
  assign block_reg$012 = block_reg[ 12];
  assign block_reg$013 = block_reg[ 13];
  assign block_reg$014 = block_reg[ 14];
  assign block_reg$015 = block_reg[ 15];

  // PYMTL SOURCE:
  //
  // @s.tick_rtl
  // def reg_update():
  //             if not s.reset_n:
  //                 s.init_reg.next = 0
  //                 s.next_reg.next = 0
  //                 s.ready_reg.next = 0
  //                 s.digest_reg.next = 0
  //                 s.digest_valid_reg.next = 0
  // 		
  //                 for ii in range(16):
  //                     s.block_reg[ii].next = 0
  //
  //             else:
  //                 s.ready_reg.next = s.core_ready
  //                 s.digest_valid_reg.next = s.core_digest_valid
  //                 s.init_reg.next = s.init_new
  //                 s.next_reg.next = s.next_new
  //
  //                 if s.block_we:
  //                     s.block_reg[s.address[0:4]].next = s.write_data
  //
  //                 if s.core_digest_valid:
  //                     s.digest_reg.next = s.core_digest

  // logic for reg_update()
  always @ (posedge clk) begin
    if (!reset_n) begin
      init_reg <= 0;
      next_reg <= 0;
      ready_reg <= 0;
      digest_reg <= 0;
      digest_valid_reg <= 0;
      for (ii=0; ii < 16; ii=ii+1)
      begin
        block_reg[ii] <= 0;
      end
    end
    else begin
      ready_reg <= core_ready;
      digest_valid_reg <= core_digest_valid;
      init_reg <= init_new;
      next_reg <= next_new;
      if (block_we) begin
        block_reg[address[(4)-1:0]] <= write_data;
      end
      else begin
      end
      if (core_digest_valid) begin
        digest_reg <= core_digest;
      end
      else begin
      end
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def logic():
  //             s.core_block.value = concat(s.block_reg[0], s.block_reg[1], s.block_reg[2], s.block_reg[3], 
  //                                         s.block_reg[4], s.block_reg[5], s.block_reg[6], s.block_reg[7], 
  //                                         s.block_reg[8], s.block_reg[9], s.block_reg[10], s.block_reg[11], 
  //                                         s.block_reg[12], s.block_reg[13], s.block_reg[14], s.block_reg[15])
  //             s.read_data.value = s.tmp_read_data
  //             s.error.value = s.tmp_error

  // logic for logic()
  always @ (*) begin
    core_block = { block_reg[0],block_reg[1],block_reg[2],block_reg[3],block_reg[4],block_reg[5],block_reg[6],block_reg[7],block_reg[8],block_reg[9],block_reg[10],block_reg[11],block_reg[12],block_reg[13],block_reg[14],block_reg[15] };
    read_data = tmp_read_data;
    error = tmp_error;
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def api():
  //             s.init_new.value = 0
  //             s.next_new.value = 0
  //             s.block_we.value = 0
  //             s.tmp_read_data.value = 0
  //             s.tmp_error.value = 0
  // 	    offset = Bits(16)
  //
  //             if s.cs:
  //
  //                 if s.we:
  //
  //                     if s.address >= ADDR_BLOCK0 and s.address <= ADDR_BLOCK15:
  //                         s.block_we.value = 1
  //
  //                     if s.address == ADDR_CTRL:
  //                         s.init_new.value = s.write_data[CTRL_INIT_BIT]
  //                         s.next_new.value = s.write_data[CTRL_NEXT_BIT]
  //
  //                 else:
  //
  //                     if s.address >= ADDR_BLOCK0 and s.address <= ADDR_BLOCK15:
  //                         s.tmp_read_data.value = s.block_reg[s.address[0:4]]
  //
  //                     if s.address >= ADDR_DIGEST0 and s.address <= ADDR_DIGEST4:
  //                         offset = (4 - (s.address - ADDR_DIGEST0)) * 32
  //                         s.tmp_read_data.value = s.digest_reg[offset : offset + 32]
  //
  //                     if s.address == ADDR_NAME0:
  //                         s.tmp_read_data.value = CORE_NAME0
  //
  //                     elif s.address == ADDR_NAME1:
  //                         s.tmp_read_data.value = CORE_NAME1
  //
  //                     elif s.address == ADDR_VERSION:
  //                         s.tmp_read_data.value = CORE_VERSION
  //
  //                     elif s.address == ADDR_CTRL:
  //                         s.tmp_read_data.value = concat(Bits(30, 0), s.next_reg, s.init_reg)
  //
  //                     elif s.address == ADDR_STATUS:
  //                         s.tmp_read_data.value = concat(Bits(30, 0), s.digest_valid_reg, s.ready_reg)
  //
  //                     else:
  //                         s.tmp_error.value = 1

  // logic for api()
  always @ (*) begin
    init_new = 0;
    next_new = 0;
    block_we = 0;
    tmp_read_data = 0;
    tmp_error = 0;
    offset__2 = 16'd0;
    if (cs) begin
      if (we) begin
        if (((address >= ADDR_BLOCK0)&&(address <= ADDR_BLOCK15))) begin
          block_we = 1;
        end
        else begin
        end
        if ((address == ADDR_CTRL)) begin
          init_new = write_data[CTRL_INIT_BIT];
          next_new = write_data[CTRL_NEXT_BIT];
        end
        else begin
        end
      end
      else begin
        if (((address >= ADDR_BLOCK0)&&(address <= ADDR_BLOCK15))) begin
          tmp_read_data = block_reg[address[(4)-1:0]];
        end
        else begin
        end
        if (((address >= ADDR_DIGEST0)&&(address <= ADDR_DIGEST4))) begin
          offset__2 = ((4-(address-ADDR_DIGEST0))*32);
          tmp_read_data = digest_reg[offset__2 +: 32];
        end
        else begin
        end
        if ((address == ADDR_NAME0)) begin
          tmp_read_data = CORE_NAME0;
        end
        else begin
          if ((address == ADDR_NAME1)) begin
            tmp_read_data = CORE_NAME1;
          end
          else begin
            if ((address == ADDR_VERSION)) begin
              tmp_read_data = CORE_VERSION;
            end
            else begin
              if ((address == ADDR_CTRL)) begin
                tmp_read_data = { 30'd0,next_reg,init_reg };
              end
              else begin
                if ((address == ADDR_STATUS)) begin
                  tmp_read_data = { 30'd0,digest_valid_reg,ready_reg };
                end
                else begin
                  tmp_error = 1;
                end
              end
            end
          end
        end
      end
    end
    else begin
    end
  end


endmodule // sha1_0x1ea2ebb7611040fb
`default_nettype wire

//-----------------------------------------------------------------------------
// sha1_core_0x187abc469c6b3e24
//-----------------------------------------------------------------------------
// dump-vcd: False
// verilator-xinit: zeros
`default_nettype none
module sha1_core_0x187abc469c6b3e24
(
  input  wire [ 511:0] block,
  input  wire [   0:0] clk,
  output reg  [ 159:0] digest,
  output reg  [   0:0] digest_valid,
  input  wire [   0:0] init,
  input  wire [   0:0] next_in,
  output reg  [   0:0] ready,
  input  wire [   0:0] reset,
  input  wire [   0:0] reset_n
);

  // wire declarations
  wire   [  31:0] w;


  // register declarations
  reg    [  31:0] H0_new;
  reg    [  31:0] H0_reg;
  reg    [  31:0] H1_new;
  reg    [  31:0] H1_reg;
  reg    [  31:0] H2_new;
  reg    [  31:0] H2_reg;
  reg    [  31:0] H3_new;
  reg    [  31:0] H3_reg;
  reg    [  31:0] H4_new;
  reg    [  31:0] H4_reg;
  reg    [   0:0] H_we;
  reg    [  31:0] a5__3;
  reg    [   0:0] a_e_we;
  reg    [  31:0] a_new;
  reg    [  31:0] a_reg;
  reg    [  31:0] b_new;
  reg    [  31:0] b_reg;
  reg    [  31:0] c_new;
  reg    [  31:0] c_reg;
  reg    [  31:0] d_new;
  reg    [  31:0] d_reg;
  reg    [   0:0] digest_init;
  reg    [   0:0] digest_update;
  reg    [   0:0] digest_valid_new;
  reg    [   0:0] digest_valid_reg;
  reg    [   0:0] digest_valid_we;
  reg    [  31:0] e_new;
  reg    [  31:0] e_reg;
  reg    [  31:0] f__3;
  reg    [   0:0] first_block;
  reg    [  31:0] k__3;
  reg    [   0:0] ready_flag;
  reg    [   0:0] round_ctr_inc;
  reg    [   6:0] round_ctr_new;
  reg    [   6:0] round_ctr_reg;
  reg    [   0:0] round_ctr_rst;
  reg    [   0:0] round_ctr_we;
  reg    [   1:0] sha1_ctrl_new;
  reg    [   1:0] sha1_ctrl_reg;
  reg    [   0:0] sha1_ctrl_we;
  reg    [   0:0] state_init;
  reg    [   0:0] state_update;
  reg    [  31:0] t__3;
  reg    [   0:0] w_init;
  reg    [   0:0] w_next;

  // localparam declarations
  localparam CTRL_DONE = 2;
  localparam CTRL_IDLE = 0;
  localparam CTRL_ROUNDS = 1;
  localparam H0_0 = 1732584193;
  localparam H0_1 = 4023233417;
  localparam H0_2 = 2562383102;
  localparam H0_3 = 271733878;
  localparam H0_4 = 3285377520;
  localparam SHA1_ROUNDS = 79;

  // w_mem_inst temporaries
  wire   [   0:0] w_mem_inst$clk;
  wire   [   0:0] w_mem_inst$next_in;
  wire   [   0:0] w_mem_inst$init;
  wire   [   0:0] w_mem_inst$reset;
  wire   [   0:0] w_mem_inst$reset_n;
  wire   [ 511:0] w_mem_inst$block;
  wire   [  31:0] w_mem_inst$w;

  sha1_w_mem_0x7b9c5c7418aeb58d w_mem_inst
  (
    .clk     ( w_mem_inst$clk ),
    .next_in ( w_mem_inst$next_in ),
    .init    ( w_mem_inst$init ),
    .reset   ( w_mem_inst$reset ),
    .reset_n ( w_mem_inst$reset_n ),
    .block   ( w_mem_inst$block ),
    .w       ( w_mem_inst$w )
  );

  // signal connections
  assign w                  = w_mem_inst$w;
  assign w_mem_inst$block   = block;
  assign w_mem_inst$clk     = clk;
  assign w_mem_inst$init    = w_init;
  assign w_mem_inst$next_in = w_next;
  assign w_mem_inst$reset   = reset;
  assign w_mem_inst$reset_n = reset_n;


  // PYMTL SOURCE:
  //
  // @s.tick_rtl
  // def reg_update():
  //             if not s.reset_n:
  //                 s.a_reg.next            = 0
  //                 s.b_reg.next            = 0
  //                 s.c_reg.next            = 0
  //                 s.d_reg.next            = 0
  //                 s.e_reg.next            = 0
  //                 s.H0_reg.next           = 0
  //                 s.H1_reg.next           = 0
  //                 s.H2_reg.next           = 0
  //                 s.H3_reg.next           = 0
  //                 s.H4_reg.next           = 0
  //                 s.digest_valid_reg.next = 0
  //                 s.round_ctr_reg.next    = 0
  //                 s.sha1_ctrl_reg.next    = CTRL_IDLE
  //
  //             else:
  //                 if s.a_e_we:
  //                     s.a_reg.next = s.a_new
  //                     s.b_reg.next = s.b_new
  //                     s.c_reg.next = s.c_new
  //                     s.d_reg.next = s.d_new
  //                     s.e_reg.next = s.e_new
  //
  //                 if s.H_we:
  //                     s.H0_reg.next = s.H0_new
  //                     s.H1_reg.next = s.H1_new
  //                     s.H2_reg.next = s.H2_new
  //                     s.H3_reg.next = s.H3_new
  //                     s.H4_reg.next = s.H4_new
  //
  //                 if s.round_ctr_we:
  //                     s.round_ctr_reg.next = s.round_ctr_new
  //
  //                 if s.digest_valid_we:
  //                     s.digest_valid_reg.next = s.digest_valid_new
  //
  //                 if s.sha1_ctrl_we:
  //                     s.sha1_ctrl_reg.next = s.sha1_ctrl_new

  // logic for reg_update()
  always @ (posedge clk) begin
    if (!reset_n) begin
      a_reg <= 0;
      b_reg <= 0;
      c_reg <= 0;
      d_reg <= 0;
      e_reg <= 0;
      H0_reg <= 0;
      H1_reg <= 0;
      H2_reg <= 0;
      H3_reg <= 0;
      H4_reg <= 0;
      digest_valid_reg <= 0;
      round_ctr_reg <= 0;
      sha1_ctrl_reg <= CTRL_IDLE;
    end
    else begin
      if (a_e_we) begin
        a_reg <= a_new;
        b_reg <= b_new;
        c_reg <= c_new;
        d_reg <= d_new;
        e_reg <= e_new;
      end
      else begin
      end
      if (H_we) begin
        H0_reg <= H0_new;
        H1_reg <= H1_new;
        H2_reg <= H2_new;
        H3_reg <= H3_new;
        H4_reg <= H4_new;
      end
      else begin
      end
      if (round_ctr_we) begin
        round_ctr_reg <= round_ctr_new;
      end
      else begin
      end
      if (digest_valid_we) begin
        digest_valid_reg <= digest_valid_new;
      end
      else begin
      end
      if (sha1_ctrl_we) begin
        sha1_ctrl_reg <= sha1_ctrl_new;
      end
      else begin
      end
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def logic():
  //             s.ready.value = s.ready_flag
  //             s.digest.value = concat(s.H0_reg, s.H1_reg, s.H2_reg, s.H3_reg, s.H4_reg)
  //             s.digest_valid.value = s.digest_valid_reg

  // logic for logic()
  always @ (*) begin
    ready = ready_flag;
    digest = { H0_reg,H1_reg,H2_reg,H3_reg,H4_reg };
    digest_valid = digest_valid_reg;
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def digest_logic():
  //             s.H0_new.value = 0
  //             s.H1_new.value = 0
  //             s.H2_new.value = 0
  //             s.H3_new.value = 0
  //             s.H4_new.value = 0
  //             s.H_we.value = 0
  //
  //             if s.digest_init:
  //                 s.H0_new.value = H0_0
  //                 s.H1_new.value = H0_1
  //                 s.H2_new.value = H0_2
  //                 s.H3_new.value = H0_3
  //                 s.H4_new.value = H0_4
  //                 s.H_we.value = 1
  //
  //             if s.digest_update:
  //                 s.H0_new.value = s.H0_reg + s.a_reg
  //                 s.H1_new.value = s.H1_reg + s.b_reg
  //                 s.H2_new.value = s.H2_reg + s.c_reg
  //                 s.H3_new.value = s.H3_reg + s.d_reg
  //                 s.H4_new.value = s.H4_reg + s.e_reg
  //                 s.H_we.value = 1

  // logic for digest_logic()
  always @ (*) begin
    H0_new = 0;
    H1_new = 0;
    H2_new = 0;
    H3_new = 0;
    H4_new = 0;
    H_we = 0;
    if (digest_init) begin
      H0_new = H0_0;
      H1_new = H0_1;
      H2_new = H0_2;
      H3_new = H0_3;
      H4_new = H0_4;
      H_we = 1;
    end
    else begin
    end
    if (digest_update) begin
      H0_new = (H0_reg+a_reg);
      H1_new = (H1_reg+b_reg);
      H2_new = (H2_reg+c_reg);
      H3_new = (H3_reg+d_reg);
      H4_new = (H4_reg+e_reg);
      H_we = 1;
    end
    else begin
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def state_logic():
  //             a5 = Bits(32)
  //             f  = Bits(32)
  //             k  = Bits(32)
  //             t  = Bits(32)
  //
  //             a5 = 0
  //             f = 0
  //             k = 0
  //             t = 0
  //             s.a_new.value = 0
  //             s.b_new.value = 0
  //             s.c_new.value = 0
  //             s.d_new.value = 0
  //             s.e_new.value = 0
  //             s.a_e_we.value = 0
  //
  //             if s.state_init:
  //                 if s.first_block:
  //                     s.a_new.value = H0_0
  //                     s.b_new.value = H0_1
  //                     s.c_new.value = H0_2
  //                     s.d_new.value = H0_3
  //                     s.e_new.value = H0_4
  //                     s.a_e_we.value = 1
  //                 else:
  //                     s.a_new.value = s.H0_reg
  //                     s.b_new.value = s.H1_reg
  //                     s.c_new.value = s.H2_reg
  //                     s.d_new.value = s.H3_reg
  //                     s.e_new.value = s.H4_reg
  //                     s.a_e_we.value = 1
  //
  //             if s.state_update:
  //                 if s.round_ctr_reg <= 19:
  //                     k = 0x5a827999
  //                     f = ((s.b_reg & s.c_reg) ^ (~s.b_reg & s.d_reg))
  //
  //                 elif ((s.round_ctr_reg >= 20) and (s.round_ctr_reg <= 39)):
  //                     k = 0x6ed9eba1
  //                     f = s.b_reg ^ s.c_reg ^ s.d_reg
  //
  //                 elif ((s.round_ctr_reg >= 40) and (s.round_ctr_reg <= 59)):
  //                     k = 0x8f1bbcdc
  //                     f = ((s.b_reg | s.c_reg) ^ (s.b_reg | s.d_reg) ^ (s.c_reg | s.d_reg))
  //
  //                 elif (s.round_ctr_reg >= 60):
  //                     k = 0xca62c1d6
  //                     f = s.b_reg ^ s.c_reg ^ s.d_reg
  //
  //                 a5 = concat(s.a_reg[0 : 27], s.a_reg[27 : 32])
  //                 t = a5 + s.e_reg + f + k + s.w
  //
  //                 s.a_new.value  = t
  //                 s.b_new.value  = s.a_reg
  //                 s.c_new.value  = concat(s.b_reg[0 : 2], s.b_reg[2 : 32])
  //                 s.d_new.value  = s.c_reg
  //                 s.e_new.value  = s.d_reg
  //                 s.a_e_we.value = 1

  // logic for state_logic()
  always @ (*) begin
    a5__3 = 32'd0;
    f__3 = 32'd0;
    k__3 = 32'd0;
    t__3 = 32'd0;
    a5__3 = 0;
    f__3 = 0;
    k__3 = 0;
    t__3 = 0;
    a_new = 0;
    b_new = 0;
    c_new = 0;
    d_new = 0;
    e_new = 0;
    a_e_we = 0;
    if (state_init) begin
      if (first_block) begin
        a_new = H0_0;
        b_new = H0_1;
        c_new = H0_2;
        d_new = H0_3;
        e_new = H0_4;
        a_e_we = 1;
      end
      else begin
        a_new = H0_reg;
        b_new = H1_reg;
        c_new = H2_reg;
        d_new = H3_reg;
        e_new = H4_reg;
        a_e_we = 1;
      end
    end
    else begin
    end
    if (state_update) begin
      if ((round_ctr_reg <= 19)) begin
        k__3 = 1518500249;
        f__3 = ((b_reg&c_reg)^(~b_reg&d_reg));
      end
      else begin
        if (((round_ctr_reg >= 20)&&(round_ctr_reg <= 39))) begin
          k__3 = 1859775393;
          f__3 = ((b_reg^c_reg)^d_reg);
        end
        else begin
          if (((round_ctr_reg >= 40)&&(round_ctr_reg <= 59))) begin
            k__3 = 2400959708;
            f__3 = (((b_reg|c_reg)^(b_reg|d_reg))^(c_reg|d_reg));
          end
          else begin
            if ((round_ctr_reg >= 60)) begin
              k__3 = 3395469782;
              f__3 = ((b_reg^c_reg)^d_reg);
            end
            else begin
            end
          end
        end
      end
      a5__3 = { a_reg[(27)-1:0],a_reg[(32)-1:27] };
      t__3 = ((((a5__3+e_reg)+f__3)+k__3)+w);
      a_new = t__3;
      b_new = a_reg;
      c_new = { b_reg[(2)-1:0],b_reg[(32)-1:2] };
      d_new = c_reg;
      e_new = d_reg;
      a_e_we = 1;
    end
    else begin
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def round_ctr():
  //             s.round_ctr_new.value = 0
  //             s.round_ctr_we.value = 0
  //
  //             if s.round_ctr_rst:
  //                 s.round_ctr_new.value = 0
  //                 s.round_ctr_we.value = 1
  //
  //             if s.round_ctr_inc:
  //                 s.round_ctr_new.value = s.round_ctr_reg + 1
  //                 s.round_ctr_we.value = 1

  // logic for round_ctr()
  always @ (*) begin
    round_ctr_new = 0;
    round_ctr_we = 0;
    if (round_ctr_rst) begin
      round_ctr_new = 0;
      round_ctr_we = 1;
    end
    else begin
    end
    if (round_ctr_inc) begin
      round_ctr_new = (round_ctr_reg+1);
      round_ctr_we = 1;
    end
    else begin
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def sha1_ctrl_fsm():
  //             s.digest_init.value      = 0
  //             s.digest_update.value    = 0
  //             s.state_init.value       = 0
  //             s.state_update.value     = 0
  //             s.first_block.value      = 0
  //             s.ready_flag.value       = 0
  //             s.w_init.value           = 0
  //             s.w_next.value           = 0
  //             s.round_ctr_inc.value    = 0
  //             s.round_ctr_rst.value    = 0
  //             s.digest_valid_new.value = 0
  //             s.digest_valid_we.value  = 0
  //             s.sha1_ctrl_new.value    = CTRL_IDLE
  //             s.sha1_ctrl_we.value     = 0
  //
  //             if (s.sha1_ctrl_reg == CTRL_IDLE):
  //
  //                 s.ready_flag.value = 1
  //
  //                 if s.init:
  //                     s.digest_init.value      = 1
  //                     s.w_init.value           = 1
  //                     s.state_init.value       = 1
  //                     s.first_block.value      = 1
  //                     s.round_ctr_rst.value    = 1
  //                     s.digest_valid_new.value = 0
  //                     s.digest_valid_we.value  = 1
  //                     s.sha1_ctrl_new.value    = CTRL_ROUNDS
  //                     s.sha1_ctrl_we.value     = 1
  //
  //                 if s.next_in:
  //                     s.w_init.value           = 1
  //                     s.state_init.value       = 1
  //                     s.round_ctr_rst.value    = 1
  //                     s.digest_valid_new.value = 0
  //                     s.digest_valid_we.value  = 1
  //                     s.sha1_ctrl_new.value    = CTRL_ROUNDS
  //                     s.sha1_ctrl_we.value     = 1
  //
  //             elif (s.sha1_ctrl_reg == CTRL_ROUNDS):
  //                 s.state_update.value = 1
  //                 s.round_ctr_inc.value = 1
  //                 s.w_next.value = 1
  //
  //                 if (s.round_ctr_reg == SHA1_ROUNDS):
  //                     s.sha1_ctrl_new.value = CTRL_DONE
  //                     s.sha1_ctrl_we.value = 1
  //
  //             elif (s.sha1_ctrl_reg == CTRL_DONE):
  //                 s.digest_update.value = 1
  //                 s.digest_valid_new.value = 1
  //                 s.digest_valid_we.value = 1
  //                 s.sha1_ctrl_new.value = CTRL_IDLE
  //                 s.sha1_ctrl_we.value = 1

  // logic for sha1_ctrl_fsm()
  always @ (*) begin
    digest_init = 0;
    digest_update = 0;
    state_init = 0;
    state_update = 0;
    first_block = 0;
    ready_flag = 0;
    w_init = 0;
    w_next = 0;
    round_ctr_inc = 0;
    round_ctr_rst = 0;
    digest_valid_new = 0;
    digest_valid_we = 0;
    sha1_ctrl_new = CTRL_IDLE;
    sha1_ctrl_we = 0;
    if ((sha1_ctrl_reg == CTRL_IDLE)) begin
      ready_flag = 1;
      if (init) begin
        digest_init = 1;
        w_init = 1;
        state_init = 1;
        first_block = 1;
        round_ctr_rst = 1;
        digest_valid_new = 0;
        digest_valid_we = 1;
        sha1_ctrl_new = CTRL_ROUNDS;
        sha1_ctrl_we = 1;
      end
      else begin
      end
      if (next_in) begin
        w_init = 1;
        state_init = 1;
        round_ctr_rst = 1;
        digest_valid_new = 0;
        digest_valid_we = 1;
        sha1_ctrl_new = CTRL_ROUNDS;
        sha1_ctrl_we = 1;
      end
      else begin
      end
    end
    else begin
      if ((sha1_ctrl_reg == CTRL_ROUNDS)) begin
        state_update = 1;
        round_ctr_inc = 1;
        w_next = 1;
        if ((round_ctr_reg == SHA1_ROUNDS)) begin
          sha1_ctrl_new = CTRL_DONE;
          sha1_ctrl_we = 1;
        end
        else begin
        end
      end
      else begin
        if ((sha1_ctrl_reg == CTRL_DONE)) begin
          digest_update = 1;
          digest_valid_new = 1;
          digest_valid_we = 1;
          sha1_ctrl_new = CTRL_IDLE;
          sha1_ctrl_we = 1;
        end
        else begin
        end
      end
    end
  end


endmodule // sha1_core_0x187abc469c6b3e24
`default_nettype wire

//-----------------------------------------------------------------------------
// sha1_w_mem_0x7b9c5c7418aeb58d
//-----------------------------------------------------------------------------
// dump-vcd: False
// verilator-xinit: zeros
`default_nettype none
module sha1_w_mem_0x7b9c5c7418aeb58d
(
  input  wire [ 511:0] block,
  input  wire [   0:0] clk,
  input  wire [   0:0] init,
  input  wire [   0:0] next_in,
  input  wire [   0:0] reset,
  input  wire [   0:0] reset_n,
  output reg  [  31:0] w
);

  // wire declarations
  wire   [  31:0] w_mem$000;
  wire   [  31:0] w_mem$001;
  wire   [  31:0] w_mem$002;
  wire   [  31:0] w_mem$003;
  wire   [  31:0] w_mem$004;
  wire   [  31:0] w_mem$005;
  wire   [  31:0] w_mem$006;
  wire   [  31:0] w_mem$007;
  wire   [  31:0] w_mem$008;
  wire   [  31:0] w_mem$009;
  wire   [  31:0] w_mem$010;
  wire   [  31:0] w_mem$011;
  wire   [  31:0] w_mem$012;
  wire   [  31:0] w_mem$013;
  wire   [  31:0] w_mem$014;
  wire   [  31:0] w_mem$015;


  // register declarations
  reg    [   0:0] sha1_w_mem_ctrl_new;
  reg    [   0:0] sha1_w_mem_ctrl_reg;
  reg    [   0:0] sha1_w_mem_ctrl_we;
  reg    [  31:0] w_0__3;
  reg    [  31:0] w_13__3;
  reg    [  31:0] w_16__3;
  reg    [  31:0] w_2__3;
  reg    [  31:0] w_8__3;
  reg    [   0:0] w_ctr_inc;
  reg    [   6:0] w_ctr_new;
  reg    [   6:0] w_ctr_reg;
  reg    [   0:0] w_ctr_rst;
  reg    [   0:0] w_ctr_we;
  reg    [  31:0] w_mem00_new;
  reg    [  31:0] w_mem01_new;
  reg    [  31:0] w_mem02_new;
  reg    [  31:0] w_mem03_new;
  reg    [  31:0] w_mem04_new;
  reg    [  31:0] w_mem05_new;
  reg    [  31:0] w_mem06_new;
  reg    [  31:0] w_mem07_new;
  reg    [  31:0] w_mem08_new;
  reg    [  31:0] w_mem09_new;
  reg    [  31:0] w_mem10_new;
  reg    [  31:0] w_mem11_new;
  reg    [  31:0] w_mem12_new;
  reg    [  31:0] w_mem13_new;
  reg    [  31:0] w_mem14_new;
  reg    [  31:0] w_mem15_new;
  reg    [   0:0] w_mem_we;
  reg    [  31:0] w_new;
  reg    [  31:0] w_tmp;

  // localparam declarations
  localparam CTRL_IDLE = 0;
  localparam CTRL_UPDATE = 1;
  localparam SHA1_ROUNDS = 79;

  // loop variable declarations
  integer ii;


  // array declarations
  reg    [  31:0] w_mem[0:15];
  assign w_mem$000 = w_mem[  0];
  assign w_mem$001 = w_mem[  1];
  assign w_mem$002 = w_mem[  2];
  assign w_mem$003 = w_mem[  3];
  assign w_mem$004 = w_mem[  4];
  assign w_mem$005 = w_mem[  5];
  assign w_mem$006 = w_mem[  6];
  assign w_mem$007 = w_mem[  7];
  assign w_mem$008 = w_mem[  8];
  assign w_mem$009 = w_mem[  9];
  assign w_mem$010 = w_mem[ 10];
  assign w_mem$011 = w_mem[ 11];
  assign w_mem$012 = w_mem[ 12];
  assign w_mem$013 = w_mem[ 13];
  assign w_mem$014 = w_mem[ 14];
  assign w_mem$015 = w_mem[ 15];

  // PYMTL SOURCE:
  //
  // @s.tick_rtl
  // def reg_update():
  //
  //             if not s.reset_n:
  //                 for ii in range(16):
  //                     s.w_mem[ii].next = 0
  // 		s.sha1_w_mem_ctrl_reg.next = CTRL_IDLE
  //             else:
  //                 if s.w_mem_we:
  //                     s.w_mem[0].next  = s.w_mem00_new
  //                     s.w_mem[1].next  = s.w_mem01_new
  //                     s.w_mem[2].next  = s.w_mem02_new
  //                     s.w_mem[3].next  = s.w_mem03_new
  //                     s.w_mem[4].next  = s.w_mem04_new
  //                     s.w_mem[5].next  = s.w_mem05_new
  //                     s.w_mem[6].next  = s.w_mem06_new
  //                     s.w_mem[7].next  = s.w_mem07_new
  //                     s.w_mem[8].next  = s.w_mem08_new
  //                     s.w_mem[9].next  = s.w_mem09_new
  //                     s.w_mem[10].next = s.w_mem10_new
  //                     s.w_mem[11].next = s.w_mem11_new
  //                     s.w_mem[12].next = s.w_mem12_new
  //                     s.w_mem[13].next = s.w_mem13_new
  //                     s.w_mem[14].next = s.w_mem14_new
  //                     s.w_mem[15].next = s.w_mem15_new
  //
  // 	        if s.w_ctr_we:
  //                     s.w_ctr_reg.next = s.w_ctr_new
  //
  //                 if s.sha1_w_mem_ctrl_we:
  //                     s.sha1_w_mem_ctrl_reg.next = s.sha1_w_mem_ctrl_new

  // logic for reg_update()
  always @ (posedge clk) begin
    if (!reset_n) begin
      for (ii=0; ii < 16; ii=ii+1)
      begin
        w_mem[ii] <= 0;
      end
      sha1_w_mem_ctrl_reg <= CTRL_IDLE;
    end
    else begin
      if (w_mem_we) begin
        w_mem[0] <= w_mem00_new;
        w_mem[1] <= w_mem01_new;
        w_mem[2] <= w_mem02_new;
        w_mem[3] <= w_mem03_new;
        w_mem[4] <= w_mem04_new;
        w_mem[5] <= w_mem05_new;
        w_mem[6] <= w_mem06_new;
        w_mem[7] <= w_mem07_new;
        w_mem[8] <= w_mem08_new;
        w_mem[9] <= w_mem09_new;
        w_mem[10] <= w_mem10_new;
        w_mem[11] <= w_mem11_new;
        w_mem[12] <= w_mem12_new;
        w_mem[13] <= w_mem13_new;
        w_mem[14] <= w_mem14_new;
        w_mem[15] <= w_mem15_new;
      end
      else begin
      end
      if (w_ctr_we) begin
        w_ctr_reg <= w_ctr_new;
      end
      else begin
      end
      if (sha1_w_mem_ctrl_we) begin
        sha1_w_mem_ctrl_reg <= sha1_w_mem_ctrl_new;
      end
      else begin
      end
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def logic():
  //             s.w.value = s.w_tmp

  // logic for logic()
  always @ (*) begin
    w = w_tmp;
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def select_w():
  //
  //             if s.w_ctr_reg < 16:
  //                 s.w_tmp.value = s.w_mem[s.w_ctr_reg[0:4]]
  //
  //             else:
  //                 s.w_tmp.value = s.w_new

  // logic for select_w()
  always @ (*) begin
    if ((w_ctr_reg < 16)) begin
      w_tmp = w_mem[w_ctr_reg[(4)-1:0]];
    end
    else begin
      w_tmp = w_new;
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def w_mem_update_logic():
  //             w_0  = Bits(32)
  //             w_2  = Bits(32)
  //             w_8  = Bits(32)
  //             w_13 = Bits(32)
  //             w_16 = Bits(32)
  //
  //             s.w_mem00_new.value = 0
  //             s.w_mem01_new.value = 0
  //             s.w_mem02_new.value = 0
  //             s.w_mem03_new.value = 0
  //             s.w_mem04_new.value = 0
  //             s.w_mem05_new.value = 0
  //             s.w_mem06_new.value = 0
  //             s.w_mem07_new.value = 0
  //             s.w_mem08_new.value = 0
  //             s.w_mem09_new.value = 0
  //             s.w_mem10_new.value = 0
  //             s.w_mem11_new.value = 0
  //             s.w_mem12_new.value = 0
  //             s.w_mem13_new.value = 0
  //             s.w_mem14_new.value = 0
  //             s.w_mem15_new.value = 0
  // 	    s.w_mem_we.value = 0
  //
  //             w_0  = s.w_mem[0].value
  //             w_2  = s.w_mem[2].value
  //             w_8  = s.w_mem[8].value
  //             w_13 = s.w_mem[13].value
  //             w_16 = w_13 ^ w_8 ^ w_2 ^ w_0
  //
  //             s.w_new.value = concat(w_16[0:31], w_16[31:32])
  //
  //             if s.init:
  //
  //                 s.w_mem00_new.value = s.block[480 : 512]
  //                 s.w_mem01_new.value = s.block[448 : 480]
  //                 s.w_mem02_new.value = s.block[416 : 448]
  //                 s.w_mem03_new.value = s.block[384 : 416]
  //                 s.w_mem04_new.value = s.block[352 : 384]
  //                 s.w_mem05_new.value = s.block[320 : 352]
  //                 s.w_mem06_new.value = s.block[288 : 320]
  //                 s.w_mem07_new.value = s.block[256 : 288]
  //                 s.w_mem08_new.value = s.block[224 : 256]
  //                 s.w_mem09_new.value = s.block[192 : 224]
  //                 s.w_mem10_new.value = s.block[160 : 192]
  //                 s.w_mem11_new.value = s.block[128 : 160]
  //                 s.w_mem12_new.value = s.block[96  : 128]
  //                 s.w_mem13_new.value = s.block[64  :  96]
  //                 s.w_mem14_new.value = s.block[32  :  64]
  //                 s.w_mem15_new.value = s.block[0   :  32]
  // 		s.w_mem_we.value = 1
  //
  //             elif s.w_ctr_reg > 15:
  //
  //                 s.w_mem00_new.value = s.w_mem[1]
  //                 s.w_mem01_new.value = s.w_mem[2]
  //                 s.w_mem02_new.value = s.w_mem[3]
  //                 s.w_mem03_new.value = s.w_mem[4]
  //                 s.w_mem04_new.value = s.w_mem[5]
  //                 s.w_mem05_new.value = s.w_mem[6]
  //                 s.w_mem06_new.value = s.w_mem[7]
  //                 s.w_mem07_new.value = s.w_mem[8]
  //                 s.w_mem08_new.value = s.w_mem[9]
  //                 s.w_mem09_new.value = s.w_mem[10]
  //                 s.w_mem10_new.value = s.w_mem[11]
  //                 s.w_mem11_new.value = s.w_mem[12]
  //                 s.w_mem12_new.value = s.w_mem[13]
  //                 s.w_mem13_new.value = s.w_mem[14]
  //                 s.w_mem14_new.value = s.w_mem[15]
  //                 s.w_mem15_new.value = s.w_new
  // 	        s.w_mem_we.value = 1

  // logic for w_mem_update_logic()
  always @ (*) begin
    w_0__3 = 32'd0;
    w_2__3 = 32'd0;
    w_8__3 = 32'd0;
    w_13__3 = 32'd0;
    w_16__3 = 32'd0;
    w_mem00_new = 0;
    w_mem01_new = 0;
    w_mem02_new = 0;
    w_mem03_new = 0;
    w_mem04_new = 0;
    w_mem05_new = 0;
    w_mem06_new = 0;
    w_mem07_new = 0;
    w_mem08_new = 0;
    w_mem09_new = 0;
    w_mem10_new = 0;
    w_mem11_new = 0;
    w_mem12_new = 0;
    w_mem13_new = 0;
    w_mem14_new = 0;
    w_mem15_new = 0;
    w_mem_we = 0;
    w_0__3 = w_mem[0];
    w_2__3 = w_mem[2];
    w_8__3 = w_mem[8];
    w_13__3 = w_mem[13];
    w_16__3 = (((w_13__3^w_8__3)^w_2__3)^w_0__3);
    w_new = { w_16__3[(31)-1:0],w_16__3[(32)-1:31] };
    if (init) begin
      w_mem00_new = block[(512)-1:480];
      w_mem01_new = block[(480)-1:448];
      w_mem02_new = block[(448)-1:416];
      w_mem03_new = block[(416)-1:384];
      w_mem04_new = block[(384)-1:352];
      w_mem05_new = block[(352)-1:320];
      w_mem06_new = block[(320)-1:288];
      w_mem07_new = block[(288)-1:256];
      w_mem08_new = block[(256)-1:224];
      w_mem09_new = block[(224)-1:192];
      w_mem10_new = block[(192)-1:160];
      w_mem11_new = block[(160)-1:128];
      w_mem12_new = block[(128)-1:96];
      w_mem13_new = block[(96)-1:64];
      w_mem14_new = block[(64)-1:32];
      w_mem15_new = block[(32)-1:0];
      w_mem_we = 1;
    end
    else begin
      if ((w_ctr_reg > 15)) begin
        w_mem00_new = w_mem[1];
        w_mem01_new = w_mem[2];
        w_mem02_new = w_mem[3];
        w_mem03_new = w_mem[4];
        w_mem04_new = w_mem[5];
        w_mem05_new = w_mem[6];
        w_mem06_new = w_mem[7];
        w_mem07_new = w_mem[8];
        w_mem08_new = w_mem[9];
        w_mem09_new = w_mem[10];
        w_mem10_new = w_mem[11];
        w_mem11_new = w_mem[12];
        w_mem12_new = w_mem[13];
        w_mem13_new = w_mem[14];
        w_mem14_new = w_mem[15];
        w_mem15_new = w_new;
        w_mem_we = 1;
      end
      else begin
      end
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def w_ctr():
  //             s.w_ctr_new.value = 0
  //             s.w_ctr_we.value = 0
  //
  //             if s.w_ctr_rst:
  //                 s.w_ctr_new.value = 0
  //                 s.w_ctr_we.value = 1
  //
  //             if s.w_ctr_inc:
  //                 s.w_ctr_new.value = s.w_ctr_reg.value + 1
  //                 s.w_ctr_we.value = 1

  // logic for w_ctr()
  always @ (*) begin
    w_ctr_new = 0;
    w_ctr_we = 0;
    if (w_ctr_rst) begin
      w_ctr_new = 0;
      w_ctr_we = 1;
    end
    else begin
    end
    if (w_ctr_inc) begin
      w_ctr_new = (w_ctr_reg+1);
      w_ctr_we = 1;
    end
    else begin
    end
  end

  // PYMTL SOURCE:
  //
  // @s.combinational
  // def sha1_w_mem_fsm():
  //             s.w_ctr_rst.value = 0
  //             s.w_ctr_inc.value = 0
  //             s.sha1_w_mem_ctrl_new.value = CTRL_IDLE
  //             s.sha1_w_mem_ctrl_we.value = 0
  //
  //             if s.sha1_w_mem_ctrl_reg == CTRL_IDLE:
  //
  //                 if s.init:
  //                     s.w_ctr_rst.value = 1
  //                     s.sha1_w_mem_ctrl_new.value = CTRL_UPDATE
  //                     s.sha1_w_mem_ctrl_we.value = 1
  //
  //             elif s.sha1_w_mem_ctrl_reg == CTRL_UPDATE:
  //
  //                 if s.next_in:
  //                     s.w_ctr_inc.value = 1
  //
  //                 if s.w_ctr_reg == SHA1_ROUNDS:
  //                     s.sha1_w_mem_ctrl_new.value = CTRL_IDLE
  //                     s.sha1_w_mem_ctrl_we.value = 1

  // logic for sha1_w_mem_fsm()
  always @ (*) begin
    w_ctr_rst = 0;
    w_ctr_inc = 0;
    sha1_w_mem_ctrl_new = CTRL_IDLE;
    sha1_w_mem_ctrl_we = 0;
    if ((sha1_w_mem_ctrl_reg == CTRL_IDLE)) begin
      if (init) begin
        w_ctr_rst = 1;
        sha1_w_mem_ctrl_new = CTRL_UPDATE;
        sha1_w_mem_ctrl_we = 1;
      end
      else begin
      end
    end
    else begin
      if ((sha1_w_mem_ctrl_reg == CTRL_UPDATE)) begin
        if (next_in) begin
          w_ctr_inc = 1;
        end
        else begin
        end
        if ((w_ctr_reg == SHA1_ROUNDS)) begin
          sha1_w_mem_ctrl_new = CTRL_IDLE;
          sha1_w_mem_ctrl_we = 1;
        end
        else begin
        end
      end
      else begin
      end
    end
  end


endmodule // sha1_w_mem_0x7b9c5c7418aeb58d
`default_nettype wire

