// This code is modified from Altera's Design Guide. A copy of the specific chapter
// of the guide can be found here: http://people.ece.cornell.edu/land/courses/ece5760/DE1_SOC/HDL_style_qts_qii51007.pdf

module ram (data_a,
 	    data_b,
	    addr_a,
	    addr_b,
	    we_a,
	    we_b,
            clk,
	    q_a,
	    q_b
	);


	parameter DATA_WIDTH = 8;
        parameter ADDR_WIDTH = 10;

	input wire [(DATA_WIDTH-1):0] data_a;
	input wire [(DATA_WIDTH-1):0] data_b;
	input wire [(ADDR_WIDTH-1):0] addr_a; 
	input wire [(ADDR_WIDTH-1):0] addr_b;
	input wire we_a, we_b, clk;
	output reg [(DATA_WIDTH-1):0] q_a, q_b;
	

	// Declare the RAM variable
	reg [DATA_WIDTH-1:0] ram[2**ADDR_WIDTH-1:0];

	always @ (posedge clk) begin // Port A

		if (we_a) begin
			ram[addr_a] = data_a;
			q_a <= data_a;
		end 
		else
			q_a <= ram[addr_a];
	end

	always @ (posedge clk) begin // Port b
		
		if (we_b) begin
			ram[addr_b] = data_b;
			q_b <= data_b;
		end
		else
			q_b <= ram[addr_b];
	end
endmodule
