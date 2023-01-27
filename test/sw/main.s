	.file	"main.c"
	.option nopic
	.attribute arch, "rv32i2p0"
	.attribute unaligned_access, 0
	.attribute stack_align, 4
	.text
 #APP
	lui	s9, %hi( 0x80004000)
	addi	a0, zero, 0xf
	addi	a1, zero, 0xf
	addi	a2, zero, 0xf
	addi	a3, zero, 0xf
	sh 	a0, 0(s9)
	.ident	"GCC: (GNU) 10.2.0"
