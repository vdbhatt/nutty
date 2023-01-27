__asm__("lui	s9, %hi( 0x80004000)");
__asm__("addi	a0, zero, 0xf");
__asm__("addi	a1, zero, 0xf");
__asm__("addi	a2, zero, 0xf");
__asm__("addi	a3, zero, 0xf");
__asm__("sh 	a0, 0(s9)");