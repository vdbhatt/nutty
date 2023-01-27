
OUTPUT_ARCH("riscv")
ENTRY(_start)

MEMORY {
  dmem (rwx) : ORIGIN = 0x08000000, LENGTH =  0x2000 + 1024
  imem (rx) : ORIGIN =  0x00000000, LENGTH =  0x2000
}
SECTIONS
 {
  .text.init ALIGN(4) : AT(ALIGN((ORIGIN(imem) ))) {
    PROVIDE(_start = .);
    *(.text.init)
   }
  .text ALIGN((ADDR(.text.init) + SIZEOF(.text.init)), 4) : AT(ALIGN((LOADADDR(.text.init) + SIZEOF(.text.init)),4)) {
     *(.text)
   }
  .data.string ALIGN( ORIGIN(dmem) , 4) : AT( ADDR(.text) + SIZEOF(.text) ) {
    PROVIDE( _fstext = ADDR(.data.string) );
    *(.data.string)
    PROVIDE( _estext = ADDR(.data.string)  + SIZEOF(.data.string));
   }
  PROVIDE(_data_strings =  LOADADDR(.data.string));

  .data ALIGN((ADDR(.data.string ) + SIZEOF(.data.string )), 4) : AT(ALIGN((LOADADDR(.data.string) + SIZEOF(.data.string)), 4)) {
    PROVIDE(_data = ADDR(.data));
    *(.data)
    PROVIDE(_edata = ADDR(.data) + SIZEOF(.data));
   }
  PROVIDE(_data_lma = LOADADDR(.data));

  .bss ALIGN((ADDR(.data) + SIZEOF(.data)), 4) : AT(ALIGN((LOADADDR(.data) + SIZEOF(.data)), 4))  {
    PROVIDE(_fbss = .);
    *(.bss)
    PROVIDE(_ebss = .);
  }
  .tohost ALIGN((ADDR(.bss) + SIZEOF(.bss)),4) : AT(ALIGN((LOADADDR(.bss) + SIZEOF(.bss)), 4) ) {
     *(.tohost)
   }
  PROVIDE(_end = .);
}