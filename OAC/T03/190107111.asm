# Trabalho de programacao Assembly RISC-V
# Gabriel Lucas França do Nascimento
# 190107111
# Github: 

.data
mat1: .word 1, 2, 3, 4, 5, 6, 7, 8, 9  # Matriz 3x3
mat2: .word 9, 8, 7, 6, 5, 4, 3, 2, 1  # Outra matriz 3x3
result: .space 36                      # Espaço para matriz resultado (3x3)
lado: .word 3                          # Tamanho do lado da matriz
msg_menu: .asciiz "Seja bem-vindo(a)! Escolha a operação: 1-Soma, 2-Multiplicação, 3-Transposta, 4-Imprime\n"

.text
.global main

main:
    # Exibe menu
    la a0, msg_menu
    li a7, 4           # syscall para print string
    ecall

    # Lê a opção do usuário
    li a7, 5           # syscall para read int
    ecall
    mv t0, a0          # Armazena opção em t0

    # Decide operação
    beq t0, 1, chama_soma
    beq t0, 2, chama_multiplica
    beq t0, 3, chama_transposta
    beq t0, 4, chama_imprime

fim:
    li a7, 10          # syscall para sair
    ecall