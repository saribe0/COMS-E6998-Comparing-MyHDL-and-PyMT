// File: SineComputer.v
// Generated by MyHDL 0.9.0
// Date: Tue Mar 13 13:58:40 2018


`timescale 1ns/10ps

module SineComputer (
    cos_z0,
    sin_z0,
    done,
    z0,
    start,
    clock,
    reset
);
// Sine and cosine computer.
// 
// This module computes the sine and cosine of an input angle. The
// floating point numbers are represented as integers by scaling them
// up with a factor corresponding to the number of bits after the point.
// 
// Ports:
// -----
// cos_z0: cosine of the input angle
// sin_z0: sine of the input angle
// done: output flag indicated completion of the computation
// z0: input angle
// start: input that starts the computation on a posedge
// clock: clock input
// reset: reset input

output signed [19:0] cos_z0;
reg signed [19:0] cos_z0;
output signed [19:0] sin_z0;
reg signed [19:0] sin_z0;
output done;
reg done;
input signed [19:0] z0;
input start;
input clock;
input reset;






always @(posedge clock, posedge reset) begin: SINECOMPUTER_PROCESSOR
    reg [5-1:0] i;
    reg [1-1:0] state;
    reg signed [20-1:0] dz;
    reg signed [20-1:0] dx;
    reg signed [20-1:0] dy;
    reg signed [20-1:0] y;
    reg signed [20-1:0] x;
    reg signed [20-1:0] z;
    if (reset) begin
        state = 1'b0;
        cos_z0 <= 1;
        sin_z0 <= 0;
        done <= 1'b0;
        x = 0;
        y = 0;
        z = 0;
        i = 0;
    end
    else begin
        case (state)
            1'b0: begin
                if (start) begin
                    x = 159188;
                    y = 0;
                    z = z0;
                    i = 0;
                    done <= 1'b0;
                    state = 1'b1;
                end
            end
            1'b1: begin
                dx = $signed(y >>> $signed({1'b0, i}));
                dy = $signed(x >>> $signed({1'b0, i}));
                case (i)
                    0: dz = 205887;
                    1: dz = 121542;
                    2: dz = 64220;
                    3: dz = 32599;
                    4: dz = 16363;
                    5: dz = 8189;
                    6: dz = 4096;
                    7: dz = 2048;
                    8: dz = 1024;
                    9: dz = 512;
                    10: dz = 256;
                    11: dz = 128;
                    12: dz = 64;
                    13: dz = 32;
                    14: dz = 16;
                    15: dz = 8;
                    16: dz = 4;
                    17: dz = 2;
                    default: dz = 1;
                endcase
                if ((z >= 0)) begin
                    x = x - dx;
                    y = y + dy;
                    z = z - dz;
                end
                else begin
                    x = x + dx;
                    y = y - dy;
                    z = z + dz;
                end
                if (($signed({1'b0, i}) == (19 - 1))) begin
                    cos_z0 <= x;
                    sin_z0 <= y;
                    state = 1'b0;
                    done <= 1'b1;
                end
                else begin
                    i = i + 1;
                end
            end
        endcase
    end
end

endmodule
