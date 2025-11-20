; CÓDIGO ENSAMBLADOR
; ==================================================================================================

.data
    producto1: .word 0
    producto2: .word 0
    producto3: .word 0
    precio1: .word 0
    precio2: .word 0
    precio3: .word 0
    valor_total: .word 0
    suma_precios: .word 0
    promedio: .word 0

.text
    .globl main
main:

    MOV R0, #10
    STR R0, [SP, #0]
    MOV R1, #15
    STR R1, [SP, #4]
    MOV R2, #20
    STR R2, [SP, #8]
    MOV R3, #100
    STR R3, [SP, #12]
    MOV R4, #150
    STR R4, [SP, #16]
    MOV R5, #200
    STR R5, [SP, #20]
    LDR R6, [SP, #0]
    LDR R7, [SP, #4]
    ADD R0, R6, R7
    LDR R1, [SP, #8]
    ADD R2, R0, R1
    MOV R0, R2
    BL _print_int
    LDR R3, [SP, #0]
    LDR R4, [SP, #12]
    MUL R5, R3, R4
    LDR R6, [SP, #4]
    LDR R7, [SP, #16]
    MUL R0, R6, R7
    ADD R1, R5, R0
    LDR R2, [SP, #8]
    LDR R3, [SP, #20]
    MUL R4, R2, R3
    ADD R5, R1, R4
    STR R5, [SP, #24]
    LDR R6, [SP, #24]
    MOV R0, R6
    BL _print_int
    LDR R7, [SP, #0]
    MOV R0, #5
    SUB R1, R7, R0
    STR R1, [SP, #0]
    LDR R2, [SP, #0]
    MOV R0, R2
    BL _print_int
    LDR R3, [SP, #12]
    LDR R4, [SP, #16]
    ADD R5, R3, R4
    LDR R6, [SP, #20]
    ADD R7, R5, R6
    STR R7, [SP, #28]
    LDR R0, [SP, #28]
    MOV R1, #3
    DIV R2, R0, R1
    STR R2, [SP, #32]
    LDR R3, [SP, #32]
    MOV R0, R3
    BL _print_int

    MOV R0, #0
    B _exit
