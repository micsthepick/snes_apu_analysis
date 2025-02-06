.p816
.a16
.i16

.include "snes.inc"
.include "dma.inc"

.include "blaargapu.inc"

MAX_FRAME = 128

BLANK = $010F

.zeropage
temp: .res 16
input_index: .res 2
current_frame: .res 2
line_buffer: .res 8
input_buffer: .res 48
current_input: .res 2
last_frame_input: .res 2

consecutive_pumps: .res 2

frame_controller: .res 2
subframe_controller: .res 2

last_frame_with_input: .res 2

mask_0: .res 2
mask_1: .res 2

.bss

hud: .res 32*2*8
endhud:

.segment "HEADER"
    .byte "pollice"

.segment "ROMINFO"
    .byte $30            ; LoROM, fast-capable
    .byte 0              ; no battery RAM
    .byte $05            ; 32K ROM
    .byte 0,0,0,0
    .word $AAAA,$5555    ; dummy checksum and complement

.segment "VECTORS"
    .word .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(halt)
    .word .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(halt), .loword(reset), .loword(halt)

.segment "BANK0": absolute

zero:
    .word $0000

.proc reset
    jmp f:_reset
_reset:
    clc
    xce
    rep #$FB
    jml f:continue
continue:
    lda #$1fff
    tcs
    lda #$0000
    tcd
    pha
    plb
    plb

    stz MDMAEN

    setaxy8
    stz NMITIMEN

    ; Enable FastROM and forced blanking
    lda #$01
    sta MEMSEL
    lda #$8F
    sta INIDISP

    ; Reset PPU registers
    ldx #$32
@loop:
    stz $2100,x
    stz $2100,x
    dex
    bne @loop

    lda #$80
    sta VMAIN

    setaxy16
    ; Initialize WRAM
    lda #.loword(zero)
    dma 0, DMAMODE_WRAM|DMA_CONST, ^zero, $2000
    stz WMADDL

    seta8
    lda #$01
    sta COPYSTART
    
    ; Initialize SPC
    jsr spc_wait_boot

    ldy #$0300
    jsr spc_begin_upload

upload_loop:
    lda sample_data, y
    jsr spc_upload_byte

    cpy #sample_data_end-sample_data
    bne upload_loop

.macro dsp addr, val
    ldx #(addr | (val<<8))
    jsr spc_write_dsp
.endmacro

    dsp $0C, $7F    ; Master volume
    dsp $1C, $7F
    dsp $2C, $00    ; Echo volume
    dsp $3C, $00
    dsp $6C, $20    ; Flags
    dsp $2D, $00
    dsp $3D, $00
    dsp $4D, $00
    dsp $5D, $03    ; Sample directory

    dsp $00, $7F    ; Sample volume
    dsp $01, $7F
    dsp $02, $00    ; Sample pitch
    dsp $03, $10
    dsp $04, $00    ; Sample source
    dsp $05, $00    ; ADSR off
    dsp $07, $7F    ; Gain

    dsp $4C, $01    ; Key on

    jmp halt
.endproc

.proc halt
    bra halt
.endproc

sample_data:
    ; Sample start & loop address
    .word $0304, $0304
    ; Sample data
    .byte $F3
    .byte $70, $E0
    .byte $70, $E0
    .byte $70, $E0
    .byte $70, $E0
sample_data_end:
