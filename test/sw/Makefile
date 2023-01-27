
ARCH = rv32i
CROSS = riscv32-unknown-elf
CCPATH = /opt/riscv/bin/

CC = $(CCPATH)/$(CROSS)-gcc
AS = $(CCPATH)/$(CROSS)-as
LD = $(CCPATH)/$(CROSS)-ld
OC = $(CCPATH)/$(CROSS)-objcopy
OD = $(CCPATH)/$(CROSS)-objdump
CPP = $(CCPATH)/$(CROSS)-CPP

CCFLAGS = -Wall -I./include -O0 -march=$(ARCH) -mabi=ilp32e
ASFLAGS = -march=$(ARCH)
LDFLAGS = -Tsoc.ld -Map=$(BUILD_DIR)/$(PROJ).map -m elf32lriscv
CPFLAGS = -PROJ

OCFLAGS = -O binary
ODFLAGS = -d

PROJ = nutty
BUILD_DIR = $(shell pwd)/build
SRCS = main.c

OBJS =  $(foreach f, $(subst .c,.o,$(SRCS)), $(f))
ASMS =  $(foreach f, $(subst .c,.s,$(SRCS)),  $(f))
TARGETS = $(BUILD_DIR)/$(PROJ).rom


all:  $(BUILD_DIR) $(TARGETS) $(OBJS) $(ASMS)
	echo sources ok

clean:
	rm -rf $(BUILD_DIR)
	-rm *.s *.o

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

%.o : %.s
	$(AS) $(ASFLAGS) -c $< -o $@

%.s : %.c
	$(CC) $(CCFLAGS) -S $< -o $@

$(BUILD_DIR)/$(PROJ).o: $(OBJS)
	$(LD) $(LDFLAGS) $(OBJS) -o $@
	$(OD) $(ODFLAGS) $@ > $(BUILD_DIR)/$(PROJ).lst

$(BUILD_DIR)/$(PROJ).rom: $(BUILD_DIR)/$(PROJ).o
	$(OC) $(OCFLAGS) $< $(BUILD_DIR)/$(PROJ).text --only-section .text*
	hexdump -ve '1/4 "%08x\n"' $(BUILD_DIR)/$(PROJ).text > $@
	rm $(BUILD_DIR)/$(PROJ).text
	wc -l $@
	cp $@ $(BUILD_DIR)/$(PROJ).mem


$(BUILD_DIR)/$(PROJ).ram: $(BUILD_DIR)/$(PROJ).o
	$(OC) $(OCFLAGS) $< $(BUILD_DIR)/$(PROJ).text --only-section .*data*
	hexdump -ve '1/4 "%08x\n"' $(BUILD_DIR)/$(PROJ).data > $@
	rm $(BUILD_DIR)/$(PROJ).data
	wc -l $@