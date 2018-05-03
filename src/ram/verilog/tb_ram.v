// Written to test the ram module

`timescale 1ns / 1ns
module tb_ram();

	localparam DATA_WIDTH = 8;
	localparam ADDR_WIDTH = 10;
	parameter CLK_HALF_PERIOD = 5;
	parameter CLK_PERIOD = CLK_HALF_PERIOD * 2;

	// Testbench registers
	reg [31 : 0] cycle_ctr;
	reg [279: 0] output_data;
	reg [15 : 0] half_word_out;
	reg [7  : 0] byte_out;

	// Clocks and enables
	reg clk;
	reg we_a;
	reg we_b;

	// Data lines
	reg [(DATA_WIDTH-1):0] data_a;
	reg [(DATA_WIDTH-1):0] data_b;

	// Address lines
	reg [(ADDR_WIDTH-1):0] addr_a;
	reg [(ADDR_WIDTH-1):0] addr_b;

	// Output wires
	wire [(DATA_WIDTH-1):0] q_a;
	wire [(DATA_WIDTH-1):0] q_b;


	// Device under test
	ram #(
			.DATA_WIDTH(DATA_WIDTH), 
			.ADDR_WIDTH(ADDR_WIDTH)) dut(
			.clk(clk),
			.we_a(we_a),
			.we_b(we_b),
			.data_a(data_a),
			.data_b(data_b),
			.addr_a(addr_a),
			.addr_b(addr_b),
			.q_a(q_a),
			.q_b(q_b)
		);


	// Clock generation
	always
	begin : clk_gen
		#CLK_HALF_PERIOD clk = !clk;
	end // clk_gen

	// Cycle counter
	always
	begin: monitor
		#(CLK_PERIOD);
		cycle_ctr = cycle_ctr + 1;
	end // cycle_ctr

	// Reset
	task init;
		begin
			clk = 0;
			we_a = 0;
			we_b = 0;
			cycle_ctr = 32'h00000000;

		end
	endtask


	task write_ab(input [(ADDR_WIDTH-1) : 0] address, input [(DATA_WIDTH*2 -1) : 0]data);
		begin
			addr_a = address;
			addr_b = address + 10'b1;
			data_a = data[15 : 8];
			data_b = data[7  : 0];
			we_a = 1;
			we_b = 1;

			#(CLK_PERIOD);

			we_a = 0;
			we_b = 0;
		end
	endtask

	task write_a(input [(ADDR_WIDTH-1) : 0] address, input [(DATA_WIDTH -1) : 0]data);
		begin
			addr_a = address;
			data_a = data[7 : 0];
			we_a = 1;

			#(CLK_PERIOD);

			we_a = 0;
		end
	endtask

	task write_b(input [(ADDR_WIDTH-1) : 0] address, input [(DATA_WIDTH -1) : 0]data);
		begin
			addr_b = address;
			data_b = data[7 : 0];
			we_b = 1;

			#(CLK_PERIOD);

			we_b = 0;
		end
	endtask

	task write_block(input[279 : 0] data);
		begin
			write_ab(10'h00, data[279 : 264]);
			write_ab(10'h02, data[263 : 248]);
			write_ab(10'h04, data[247 : 232]);
			write_ab(10'h06, data[231 : 216]);
			write_ab(10'h08, data[215 : 200]);
			write_ab(10'h10, data[199 : 184]);
			write_ab(10'h12, data[183 : 168]);
			write_ab(10'h14, data[167 : 152]);
			write_ab(10'h16, data[151 : 136]);
			write_ab(10'h18, data[135 : 120]);
			write_ab(10'h20, data[119 : 104]);
			write_ab(10'h22, data[103 :  88]);
			write_ab(10'h24, data[87  :  72]);
			write_ab(10'h26, data[71  :  56]);
			write_ab(10'h28, data[55  :  40]);
			write_ab(10'h30, data[39  :  24]);
			write_a (10'h32, data[23  :  16]);
			write_a (10'h33, data[15  :   8]);
			write_b (10'h34, data[7   :   0]);
		end
	endtask

	task read_ab(input [(ADDR_WIDTH-1) : 0] address);
		begin
			addr_a = address;
			addr_b = address + 10'b1;

			#(CLK_PERIOD);

			half_word_out[15 : 8] = q_a;
			half_word_out[7  : 0] = q_b;
		end
	endtask

	task read_a(input [(ADDR_WIDTH-1) : 0] address);
		begin
			addr_a = address;

			#(CLK_PERIOD);

			byte_out = q_a;
		end
	endtask

	task read_b(input [(ADDR_WIDTH-1) : 0] address);
		begin
			addr_b = address;

			#(CLK_PERIOD);

			byte_out = q_b;
		end
	endtask

	task read_block;
		begin
			read_a (10'h00);
			output_data[279 : 272] = byte_out;
			read_a (10'h01);
			output_data[272 : 264] = byte_out;
			read_b (10'h02);
			output_data[263 : 256] = byte_out;
			read_ab(10'h03);
			output_data[255 : 240] = half_word_out;
			read_ab(10'h05);
			output_data[239 : 224] = half_word_out;
			read_ab(10'h07);
			output_data[223 : 208] = half_word_out;
			read_ab(10'h09);
			output_data[207 : 192] = half_word_out;
			read_ab(10'h11);
			output_data[191 : 176] = half_word_out;
			read_ab(10'h13);
			output_data[175 : 160] = half_word_out;
			read_ab(10'h15);
			output_data[159 : 144] = half_word_out;
			read_ab(10'h17);
			output_data[143 : 128] = half_word_out;
			read_ab(10'h19);
			output_data[127 : 112] = half_word_out;
			read_ab(10'h21);
			output_data[111 :  96] = half_word_out;
			read_ab(10'h23);
			output_data[95  :  80] = half_word_out;
			read_ab(10'h25);
			output_data[79  :  64] = half_word_out;
			read_ab(10'h27);
			output_data[63  :  48] = half_word_out;
			read_ab(10'h29);
			output_data[47  :  32] = half_word_out;
			read_ab(10'h31);
			output_data[31  :  16] = half_word_out;
			read_ab(10'h33);
			output_data[15  :   0] = half_word_out;
		end
	endtask


	// Simple test to write "This RAM module can read and write." to 
	// ram and read it back
	initial
		begin : ram_test
			
			reg [279: 0] in_data;

			$display("*** Starting RAM test ***");

			init();
		
			in_data = 280'h546869732052414d206d6f64756c652063616e207265616420616e642077726974652e;

			// Write the data to RAM
			write_block(in_data);

			// Read the data from the RAM
			read_block();

			// Compare the results
			if (in_data == output_data)
			begin
				$display("Test Successful");
			end
			else 
			begin
				$display("Recieved 0x%070x", output_data);
				$display("Expected 0x%070x", in_data);
			end

			$display("*** RAM test finished ***");
			$finish;

		end
	endmodule	

































