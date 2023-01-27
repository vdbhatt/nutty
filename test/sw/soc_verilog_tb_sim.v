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

initial begin
    $dumpfile("nutty_soc_iverilog_manual.vcd");
    $dumpvars;
    #300
    $finish();
end
top top(.rst(rst),.clk(clk));


//tb_updated
initial begin
$readmemh("/workspaces/nutty/test/sw/build/nutty.rom", top.U$$0.imem._mem);
end
endmodule