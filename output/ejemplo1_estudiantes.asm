; CÓDIGO ENSAMBLADOR
; ==================================================================================================

.data
    estudiantes: .word 0
    nombres: .word 0
    calificaciones: .word 0

.text
    .globl main
main:

    BL _list_create
    MOV R0, R0
    STR R0, [SP, #0]
    BL _list_create
    MOV R1, R0
    STR R1, [SP, #4]
    BL _list_create
    MOV R2, R0
    STR R2, [SP, #8]
    LDR R3, [SP, #0]
    MOV R4, #1
    MOV R0, R3
    MOV R1, R4
    BL _list_append
    LDR R5, [SP, #4]
    LDR R6, [SP, #0]
    MOV R0, R5
    MOV R1, R6
    BL _list_append
    LDR R7, [SP, #8]
    MOV R0, #85
    MOV R0, R7
    MOV R1, R0
    BL _list_append
    LDR R1, [SP, #0]
    MOV R2, #2
    MOV R0, R1
    MOV R1, R2
    BL _list_append
    LDR R3, [SP, #4]
    LDR R4, [SP, #0]
    MOV R0, R3
    MOV R1, R4
    BL _list_append
    LDR R5, [SP, #8]
    MOV R6, #92
    MOV R0, R5
    MOV R1, R6
    BL _list_append
    LDR R7, [SP, #0]
    MOV R0, #3
    MOV R0, R7
    MOV R1, R0
    BL _list_append
    LDR R1, [SP, #4]
    LDR R2, [SP, #0]
    MOV R0, R1
    MOV R1, R2
    BL _list_append
    LDR R3, [SP, #8]
    MOV R4, #78
    MOV R0, R3
    MOV R1, R4
    BL _list_append
    LDR R5, [SP, #0]
    MOV R6, #0
    MOV R0, R5
    MOV R1, R6
    BL _list_get
    MOV R7, R0
    MOV R0, R7
    BL _print_int
    LDR R0, [SP, #4]
    MOV R1, #0
    MOV R0, R0
    MOV R1, R1
    BL _list_get
    MOV R2, R0
    MOV R0, R2
    BL _print_int
    LDR R3, [SP, #8]
    MOV R4, #0
    MOV R0, R3
    MOV R1, R4
    BL _list_get
    MOV R5, R0
    MOV R0, R5
    BL _print_int
    LDR R6, [SP, #0]
    MOV R7, #1
    MOV R0, R6
    MOV R1, R7
    BL _list_get
    MOV R0, R0
    MOV R0, R0
    BL _print_int
    LDR R1, [SP, #4]
    MOV R2, #1
    MOV R0, R1
    MOV R1, R2
    BL _list_get
    MOV R3, R0
    MOV R0, R3
    BL _print_int
    LDR R4, [SP, #8]
    MOV R5, #1
    MOV R0, R4
    MOV R1, R5
    BL _list_get
    MOV R6, R0
    MOV R0, R6
    BL _print_int
    LDR R7, [SP, #8]
    MOV R0, #0
    MOV R0, R7
    MOV R1, R0
    BL _list_get
    MOV R1, R0
    MOV R0, R1
    BL _print_int
    LDR R2, [SP, #8]
    MOV R3, #1
    MOV R0, R2
    MOV R1, R3
    BL _list_get
    MOV R4, R0
    MOV R0, R4
    BL _print_int
    LDR R5, [SP, #8]
    MOV R6, #2
    MOV R0, R5
    MOV R1, R6
    BL _list_get
    MOV R7, R0
    MOV R0, R7
    BL _print_int
    LDR R0, [SP, #0]
    MOV R1, #0
    MOV R0, R0
    MOV R1, R1
    BL _list_get
    MOV R2, R0
    MOV R0, R2
    BL _print_int
    LDR R3, [SP, #0]
    MOV R4, #1
    MOV R0, R3
    MOV R1, R4
    BL _list_get
    MOV R5, R0
    MOV R0, R5
    BL _print_int
    LDR R6, [SP, #0]
    MOV R7, #2
    MOV R0, R6
    MOV R1, R7
    BL _list_get
    MOV R0, R0
    MOV R0, R0
    BL _print_int

    MOV R0, #0
    B _exit
