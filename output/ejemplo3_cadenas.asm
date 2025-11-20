; CÓDIGO ENSAMBLADOR
; ==================================================================================================

.data
    nombre: .word 0
    apellido: .word 0
    len_nombre: .word 0
    len_apellido: .word 0
    palabras: .word 0
    saludo: .word 0
    len_saludo: .word 0

.text
    .globl main
main:

    LDR R0, [SP, #0]
    STR R0, [SP, #0]
    LDR R1, [SP, #0]
    STR R1, [SP, #4]
    LDR R2, [SP, #0]
    MOV R0, R2
    BL _list_len
    MOV R3, R0
    STR R3, [SP, #8]
    LDR R4, [SP, #4]
    MOV R0, R4
    BL _list_len
    MOV R5, R0
    STR R5, [SP, #12]
    LDR R6, [SP, #8]
    MOV R0, R6
    BL _print_int
    LDR R7, [SP, #12]
    MOV R0, R7
    BL _print_int
    LDR R0, [SP, #8]
    MOV R1, #5
    CMP R0, R1
    MOVGT R2, #1
    MOVNGT R2, #0
    CMP R2, #0
    BEQ L0
    MOV R3, #1
    MOV R0, R3
    BL _print_int
    B L1
L0:
    MOV R4, #0
    MOV R0, R4
    BL _print_int
L1:
    LDR R5, [SP, #12]
    LDR R6, [SP, #8]
    CMP R5, R6
    MOVGT R7, #1
    MOVNGT R7, #0
    CMP R7, #0
    BEQ L2
    MOV R0, #1
    MOV R0, R0
    BL _print_int
    B L3
L2:
    MOV R1, #0
    MOV R0, R1
    BL _print_int
L3:
    BL _list_create
    MOV R2, R0
    STR R2, [SP, #16]
    LDR R3, [SP, #16]
    LDR R4, [SP, #0]
    MOV R0, R3
    MOV R1, R4
    BL _list_append
    LDR R5, [SP, #16]
    LDR R6, [SP, #4]
    MOV R0, R5
    MOV R1, R6
    BL _list_append
    LDR R7, [SP, #16]
    MOV R0, R7
    BL _list_len
    MOV R0, R0
    MOV R0, R0
    BL _print_int
    LDR R1, [SP, #0]
    STR R1, [SP, #20]
    LDR R2, [SP, #20]
    MOV R0, R2
    BL _list_len
    MOV R3, R0
    STR R3, [SP, #24]
    LDR R4, [SP, #24]
    MOV R0, R4
    BL _print_int
    LDR R5, [SP, #0]
    LDR R6, [SP, #0]
    CMP R5, R6
    MOVEQ R7, #1
    MOVNEQ R7, #0
    CMP R7, #0
    BEQ L4
    MOV R0, #1
    MOV R0, R0
    BL _print_int
    B L5
L4:
    MOV R1, #0
    MOV R0, R1
    BL _print_int
L5:
    LDR R2, [SP, #16]
    MOV R0, R2
    BL _list_len
    MOV R3, R0
    MOV R4, #2
    CMP R3, R4
    MOVEQ R5, #1
    MOVNEQ R5, #0
    CMP R5, #0
    BEQ L6
    MOV R6, #1
    MOV R0, R6
    BL _print_int
    B L7
L6:
    MOV R7, #0
    MOV R0, R7
    BL _print_int
L7:

    MOV R0, #0
    B _exit
