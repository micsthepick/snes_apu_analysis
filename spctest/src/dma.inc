.ifndef DMA_H
.define DMA_H

; Prepares a DMA transfer.
; A: The A-bus address to access ($43n3:43n2).
; ch: The DMA channel to use.
; mode: The B-bus address & transfer mode to use ($43n1:43n0)
; sbank: The A-bus bank number ($43n4).
; len: How many bytes to transfer. Can be a constant, or X or Y.
;
; Note: Does not start the transfer.
.macro dma  ch, mode, sbank, len
    .assert .asize = 16, error, "Accumulator must be 16 bits"
    .local CH
    CH = ch << 4

    sta CH+DMAADDR
    lda #mode
    sta CH+DMAMODE
    lda #sbank
    sta CH+DMAADDRBANK
    .if .match(len, x) || .match(len, y)
        .if .isize = 8
            stz CH+DMALEN
        .endif
        .if .match(len, x)
            stx CH+DMALEN
        .else
            sty CH+DMALEN
        .endif
    .else
        lda #len
        sta CH+DMALEN
    .endif
.endmacro

.endif
