; CÓDIGO ENSAMBLADOR
; ==================================================================================================

.data
    result: .word 0
    resultado1: .word 0
    resultado2: .word 0
    resultado3: .word 0
    resultado4: .word 0

.text
    .globl main
main:

func_factorial:
    LDR R0, [SP, #0]
    MOV R1, #0
    CMP R0, R1
    MOVEQ R2, #1
    MOVNEQ R2, #0
    CMP R2, #0
    BEQ L0
    B L1
L0:
    LDR R3, [SP, #0]
    MOV R4, #1
    SUB R5, R3, R4
    STR R6, [SP, #0]
L1:
    STR R7, [SP, #4]
    LDR R0, [SP, #4]
    MOV R0, R0
    BL _print_int
    STR R1, [SP, #8]
    LDR R2, [SP, #8]
    MOV R0, R2
    BL _print_int
    STR R3, [SP, #12]
    LDR R4, [SP, #12]
    MOV R0, R4
    BL _print_int
    STR R5, [SP, #16]
    LDR R6, [SP, #16]
    MOV R0, R6
    BL _print_int

    MOV R0, #0
    B _exit
