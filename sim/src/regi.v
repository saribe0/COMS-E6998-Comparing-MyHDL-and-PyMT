//-----------------------------------------------------------------------------
// RegIncr_0x7a81360b75b3f561
//-----------------------------------------------------------------------------
// dump-vcd: False
// verilator-xinit: zeros
module regi
(
  input  wire clk,
  output wire [   31:0] out,
  input  wire reset
);

  // wire declarations
  reg   [  31:0] reg_out;




  // PYMTL SOURCE:
  //
  // @s.combinational
  // def block2():
  //       s.out.value = s.reg_out + 1

  // logic for block2()
  always @ (posedge clk) begin
     if (reset) begin
       reg_out <= 0;
     end else begin
	reg_out <= reg_out + 32'd1;
     end
  end

   assign out = reg_out;
   


endmodule // RegIncr_0x7a81360b75b3f561
//`default_nettype wire

