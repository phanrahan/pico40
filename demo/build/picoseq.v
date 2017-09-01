module Register8CE (input [7:0] I, output [7:0] O, input  CLK, input  CE);
wire  inst0_Q;
wire  inst1_Q;
wire  inst2_Q;
wire  inst3_Q;
wire  inst4_Q;
wire  inst5_Q;
wire  inst6_Q;
wire  inst7_Q;
SB_DFFE inst0 (.C(CLK), .E(CE), .D(I[0]), .Q(inst0_Q));
SB_DFFE inst1 (.C(CLK), .E(CE), .D(I[1]), .Q(inst1_Q));
SB_DFFE inst2 (.C(CLK), .E(CE), .D(I[2]), .Q(inst2_Q));
SB_DFFE inst3 (.C(CLK), .E(CE), .D(I[3]), .Q(inst3_Q));
SB_DFFE inst4 (.C(CLK), .E(CE), .D(I[4]), .Q(inst4_Q));
SB_DFFE inst5 (.C(CLK), .E(CE), .D(I[5]), .Q(inst5_Q));
SB_DFFE inst6 (.C(CLK), .E(CE), .D(I[6]), .Q(inst6_Q));
SB_DFFE inst7 (.C(CLK), .E(CE), .D(I[7]), .Q(inst7_Q));
assign O = {inst7_Q,inst6_Q,inst5_Q,inst4_Q,inst3_Q,inst2_Q,inst1_Q,inst0_Q};
endmodule

module Add8 (input [7:0] I0, input [7:0] I1, output [7:0] O, output  COUT);
wire  inst0_O;
wire  inst1_CO;
wire  inst2_O;
wire  inst3_CO;
wire  inst4_O;
wire  inst5_CO;
wire  inst6_O;
wire  inst7_CO;
wire  inst8_O;
wire  inst9_CO;
wire  inst10_O;
wire  inst11_CO;
wire  inst12_O;
wire  inst13_CO;
wire  inst14_O;
wire  inst15_CO;
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst0 (.I0(1'b0), .I1(I0[0]), .I2(I1[0]), .I3(1'b0), .O(inst0_O));
SB_CARRY inst1 (.I0(I0[0]), .I1(I1[0]), .CI(1'b0), .CO(inst1_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst2 (.I0(1'b0), .I1(I0[1]), .I2(I1[1]), .I3(inst1_CO), .O(inst2_O));
SB_CARRY inst3 (.I0(I0[1]), .I1(I1[1]), .CI(inst1_CO), .CO(inst3_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst4 (.I0(1'b0), .I1(I0[2]), .I2(I1[2]), .I3(inst3_CO), .O(inst4_O));
SB_CARRY inst5 (.I0(I0[2]), .I1(I1[2]), .CI(inst3_CO), .CO(inst5_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst6 (.I0(1'b0), .I1(I0[3]), .I2(I1[3]), .I3(inst5_CO), .O(inst6_O));
SB_CARRY inst7 (.I0(I0[3]), .I1(I1[3]), .CI(inst5_CO), .CO(inst7_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst8 (.I0(1'b0), .I1(I0[4]), .I2(I1[4]), .I3(inst7_CO), .O(inst8_O));
SB_CARRY inst9 (.I0(I0[4]), .I1(I1[4]), .CI(inst7_CO), .CO(inst9_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst10 (.I0(1'b0), .I1(I0[5]), .I2(I1[5]), .I3(inst9_CO), .O(inst10_O));
SB_CARRY inst11 (.I0(I0[5]), .I1(I1[5]), .CI(inst9_CO), .CO(inst11_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst12 (.I0(1'b0), .I1(I0[6]), .I2(I1[6]), .I3(inst11_CO), .O(inst12_O));
SB_CARRY inst13 (.I0(I0[6]), .I1(I1[6]), .CI(inst11_CO), .CO(inst13_CO));
SB_LUT4 #(.LUT_INIT(16'hC33C)) inst14 (.I0(1'b0), .I1(I0[7]), .I2(I1[7]), .I3(inst13_CO), .O(inst14_O));
SB_CARRY inst15 (.I0(I0[7]), .I1(I1[7]), .CI(inst13_CO), .CO(inst15_CO));
assign O = {inst14_O,inst12_O,inst10_O,inst8_O,inst6_O,inst4_O,inst2_O,inst0_O};
assign COUT = inst15_CO;
endmodule

module Mux2x8 (input [7:0] I0, input [7:0] I1, input  S, output [7:0] O);
wire  inst0_O;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
wire  inst4_O;
wire  inst5_O;
wire  inst6_O;
wire  inst7_O;
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst0 (.I0(I0[0]), .I1(I1[0]), .I2(S), .I3(1'b0), .O(inst0_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst1 (.I0(I0[1]), .I1(I1[1]), .I2(S), .I3(1'b0), .O(inst1_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst2 (.I0(I0[2]), .I1(I1[2]), .I2(S), .I3(1'b0), .O(inst2_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst3 (.I0(I0[3]), .I1(I1[3]), .I2(S), .I3(1'b0), .O(inst3_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst4 (.I0(I0[4]), .I1(I1[4]), .I2(S), .I3(1'b0), .O(inst4_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst5 (.I0(I0[5]), .I1(I1[5]), .I2(S), .I3(1'b0), .O(inst5_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst6 (.I0(I0[6]), .I1(I1[6]), .I2(S), .I3(1'b0), .O(inst6_O));
SB_LUT4 #(.LUT_INIT(16'hCACA)) inst7 (.I0(I0[7]), .I1(I1[7]), .I2(S), .I3(1'b0), .O(inst7_O));
assign O = {inst7_O,inst6_O,inst5_O,inst4_O,inst3_O,inst2_O,inst1_O,inst0_O};
endmodule

module main (input [7:0] J1, output [7:0] J3, input  CLKIN);
wire [15:0] inst0_RDATA;
wire  inst1_O;
wire  inst2_O;
wire  inst3_O;
wire  inst4_O;
wire  inst5_O;
wire  inst6_O;
wire  inst7_O;
wire  inst8_Q;
wire  inst9_O;
wire [7:0] inst10_O;
wire [7:0] inst11_O;
wire  inst11_COUT;
wire [7:0] inst12_O;
wire [7:0] inst13_O;
SB_RAM40_4K #(.INIT_1(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_0(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_3(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_2(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_5(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_4(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_7(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_6(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_9(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_8(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_A(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_C(256'h7000600050004000300020001000000070006000500040003000200010000000),
.READ_MODE(0),
.INIT_E(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_D(256'h7000600050004000300020001000000070006000500040003000200010000000),
.INIT_F(256'h7000600050004000300020001000000070006000500040003000200010000000),
.WRITE_MODE(0),
.INIT_B(256'h7000600050004000300020001000000070006000500040003000200010000000)) inst0 (.RDATA(inst0_RDATA), .RADDR({1'b0,1'b0,1'b0,inst10_O[7],inst10_O[6],inst10_O[5],inst10_O[4],inst10_O[3],inst10_O[2],inst10_O[1],inst10_O[0]}), .RCLK(CLKIN), .RCLKE(1'b1), .RE(1'b1), .WCLK(CLKIN), .WCLKE(1'b0), .WE(1'b0), .WADDR({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}), .MASK({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}), .WDATA({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0}));
SB_LUT4 #(.LUT_INIT(16'h0001)) inst1 (.I0(inst0_RDATA[14]), .I1(inst0_RDATA[15]), .I2(1'b0), .I3(1'b0), .O(inst1_O));
SB_LUT4 #(.LUT_INIT(16'h0002)) inst2 (.I0(inst0_RDATA[14]), .I1(inst0_RDATA[15]), .I2(1'b0), .I3(1'b0), .O(inst2_O));
SB_LUT4 #(.LUT_INIT(16'h0003)) inst3 (.I0(inst0_RDATA[14]), .I1(inst0_RDATA[15]), .I2(1'b0), .I3(1'b0), .O(inst3_O));
SB_LUT4 #(.LUT_INIT(16'h0100)) inst4 (.I0(inst0_RDATA[12]), .I1(inst0_RDATA[13]), .I2(inst0_RDATA[14]), .I3(inst0_RDATA[15]), .O(inst4_O));
SB_LUT4 #(.LUT_INIT(16'h0400)) inst5 (.I0(inst0_RDATA[12]), .I1(inst0_RDATA[13]), .I2(inst0_RDATA[14]), .I3(inst0_RDATA[15]), .O(inst5_O));
SB_LUT4 #(.LUT_INIT(16'h0800)) inst6 (.I0(inst0_RDATA[12]), .I1(inst0_RDATA[13]), .I2(inst0_RDATA[14]), .I3(inst0_RDATA[15]), .O(inst6_O));
SB_LUT4 #(.LUT_INIT(16'h1000)) inst7 (.I0(inst0_RDATA[12]), .I1(inst0_RDATA[13]), .I2(inst0_RDATA[14]), .I3(inst0_RDATA[15]), .O(inst7_O));
SB_DFF inst8 (.C(CLKIN), .D(inst9_O), .Q(inst8_Q));
SB_LUT4 #(.LUT_INIT(16'h6666)) inst9 (.I0(inst8_Q), .I1(1'b1), .I2(1'b0), .I3(1'b0), .O(inst9_O));
Register8CE inst10 (.I(inst12_O), .O(inst10_O), .CLK(CLKIN), .CE(inst8_Q));
Add8 inst11 (.I0(inst10_O), .I1({1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b0,1'b1}), .O(inst11_O), .COUT(inst11_COUT));
Mux2x8 inst12 (.I0(inst11_O), .I1({inst0_RDATA[7],inst0_RDATA[6],inst0_RDATA[5],inst0_RDATA[4],inst0_RDATA[3],inst0_RDATA[2],inst0_RDATA[1],inst0_RDATA[0]}), .S(inst7_O), .O(inst12_O));
Mux2x8 inst13 (.I0(inst10_O), .I1({inst0_RDATA[15],inst0_RDATA[14],inst0_RDATA[13],inst0_RDATA[12],inst0_RDATA[11],inst0_RDATA[10],inst0_RDATA[9],inst0_RDATA[8]}), .S(inst8_Q), .O(inst13_O));
assign J3 = inst13_O;
endmodule

