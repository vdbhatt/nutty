`default_nettype none
module rv32_compliance();

reg clk;
reg rst;

initial begin
    clk = 0;
    forever begin
        #1 clk = ~clk;
    end
end

initial begin
    #1 rst = 0;
    #1 rst = 1;
    #2 rst = 0;
end

top top(.rst(rst),.clk(clk));
integer file;
integer  i;

localparam BASE_ADDR = 32'h80000000;
localparam LENGTH = 32'h00200000;
localparam TESTUTIL_BASE = BASE_ADDR + LENGTH - 32'hc;
localparam TESTUTIL_ADDR_HALT = TESTUTIL_BASE>>2;
localparam TESTUTIL_ADDR_BEGIN_SIGNATURE = TESTUTIL_ADDR_HALT - 1;
localparam TESTUTIL_ADDR_END_SIGNATURE = TESTUTIL_ADDR_BEGIN_SIGNATURE - 1;


always @(posedge clk) begin
    if(top.U$$0.decoder__bus__adr == TESTUTIL_ADDR_HALT) begin
        file = $fopen("output.txt","w");
        for(i = top.U$$0.dram._mem[TESTUTIL_ADDR_BEGIN_SIGNATURE[19:0]][19:2] ; i < top.U$$0.dram._mem[TESTUTIL_ADDR_END_SIGNATURE[19:0]][19:2]; i = i + 1) begin
            $fwrite(file,"%h\n",top.U$$0.dram._mem[i]);
        end
        $fclose(file);
        $finish();
    end
end


//tb_updated
initial begin
$readmemh("/workspaces/nutty/test/riscof_work/image.rom", top.U$$0.imem._mem);
end
endmodule
