`timescale 1ns / 1ns
module testbench();
 
  reg  [0:0]  clk;
  reg  [0:0]  reset;
  wire [31:0] out;
  
 
  regi DUT (
    .clk(clk),
    .out(out),
    .reset(reset)
  );
 
  initial begin
	 // Initial values
         clk = 1;
	 reset = 0;
	 
	 #15 reset = 1; 	// Start reset
	 #20 reset = 0; 	// End reset
	 
  end
  
  always #5 clk = ~clk;
 
endmodule
