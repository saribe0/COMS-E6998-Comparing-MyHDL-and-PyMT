//-----------------------------------------------------------------------------
// RegIncr_0x7a81360b75b3f561
//-----------------------------------------------------------------------------
// dump-vcd: False
// verilator-xinit: zeros
`default_nettype none
module RegIncr_0x7a81360b75b3f561
(
  input  wire [   0:0] clk,
  input  wire [   7:0] in_,
  output reg  [   7:0] out,
  input  wire [   0:0] reset
);

  // wire declarations
  wire   [   7:0] reg_out;




  // PYMTL SOURCE:
  //
  // @s.combinational
  // def block2():
  //       s.out.value = s.reg_out + 1

  // logic for block2()
  always @ (*) begin
    out = (reg_out+1);
  end


endmodule // RegIncr_0x7a81360b75b3f561
`default_nettype wire

