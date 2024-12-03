# Trabalho de programacao Assembly RISC-V
# Gabriel Lucas França do Nascimento
# 190107111
# Github: 

.data
mat1: 	.word 1, 2, 3, 4, 5, 6, 7, 8, 9  # Matriz 3x3
mat2: 	.word 9, 8, 7, 6, 5, 4, 3, 2, 1  # Outra matriz 3x3
result: .space 36                      # Espaço para matriz resultado (3x3)
lado: 	.word 3                          # Tamanho do lado da matriz
menu:	.asciz "Seja bem-vindo(a)! Escolha a operação: 1-Soma, 2-Multiplicação, 3-Transposta, 4-Imprime\n"

.text
.global main

main:
    addi t1, zero, 1
    addi t2, zero, 2
    addi t3, zero, 3
    addi t4, zero, 4

    # Exibe menu
    la a0, menu
    li a7, 4           # syscall para print string
    ecall

    # Lê a opção do usuário
    li a7, 5           # syscall para read int
    ecall
    mv t0, a0          # Armazena opção em t0
    

    # Decide operação
    beq t0, t1, chama_soma
    #beq t0, t2, chama_multiplica
    #beq t0, t3, chama_transposta
    #beq t0, t4, chama_imprime
    
chama_soma:
    la a0, mat1        # Endereço da matriz 1
    la a1, mat2        # Endereço da matriz 2
    la a2, result      # Endereço da matriz resultado
    lw a3, lado        # Lado da matriz
    jal soma           # Chama função soma
    j main             # Retorna ao menu
    
read_cel:
    mul t0, a0, a3     # Linha * lado
    add t0, t0, a1     # Linha + coluna
    slli t0, t0, 2     # t0 = t0 * 4 (offset)
    add t0, t0, a2     # t0 = endereço base + offset
    lw a0, 0(t0)       # Lê valor da célula
    jr ra
    
write_cel:
    mul t0, a0, a3     # Linha * lado
    add t0, t0, a1     # Linha + coluna
    slli t0, t0, 2     # t0 = t0 * 4 (offset)
    add t0, t0, a2     # t0 = endereço base + offset
    sw a2, 0(t0)       # Escreve valor
    jr ra
    
soma:
    li t0, 0           # Inicializa índice da matriz
    mul t1, a3, a3     # t1 = lado * lado (número de elementos)

soma_loop:
    beq t0, t1, soma_fim  # Fim se todos os elementos foram somados
    lw t2, 0(a0)          # Lê elemento de mat1
    lw t3, 0(a1)          # Lê elemento de mat2
    add t4, t2, t3        # Soma os elementos
    sw t4, 0(a2)          # Armazena no resultado
    addi a0, a0, 4        # Incrementa endereço de mat1
    addi a1, a1, 4        # Incrementa endereço de mat2
    addi a2, a2, 4        # Incrementa endereço do resultado
    addi t0, t0, 1        # Incrementa índice
    j soma_loop

soma_fim:
    jr ra

fim:
    li a7, 10          # syscall para sair
    ecall