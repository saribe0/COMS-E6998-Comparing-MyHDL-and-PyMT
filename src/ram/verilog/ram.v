// This code is modified from Altera's Design Guide. A copy of the specific chapter
// of the guide can be found here: http://people.ece.cornell.edu/land/courses/ece5760/DE1_SOC/HDL_style_qts_qii51007.pdf

module true_dual_port_ram_single_clock (
	input [(DATA_WIDTH-1):0] data_a, data_b,
	input [(ADDR_WIDTH-1):0] addr_a, addr_b,
	input we_a, we_b, clk,
	output reg [(DATA_WIDTH-1):0] q_a, q_b);

	// Parameters are set to declare a 1KB RAM
	parameter DATA_WIDTH = 8;
	parameter ADDR_WIDTH = 10;

	// Declare the RAM variable
	reg [DATA_WIDTH-1:0] ram[2**ADDR_WIDTH-1:0];

	always @ (posedge clk) begin // Port A

		if (we_a) begin
			ram[addr_a] := data_a;
			q_a <= data_a;
		end 
		else
			q_a <= ram[addr_a];
	end

	always @ (posedge clk) begin // Port b
		
		if (we_b) begin
			ram[addr_b] := data_b;
			q_b <= data_b;
		end
		else
			q_b <= ram[addr_b];
	end
endmodule