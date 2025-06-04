# Trabalho de programacao Assembly RISC-V
# Gabriel Lucas França do Nascimento
# 190107111
# Github: 

.data
mat1: 	.word 1, 2, 3, 4, 5, 6, 7, 8, 9  # Matriz 3x3
mat2: 	.word 9, 8, 7, 6, 5, 4, 3, 2, 1  # Outra matriz 3x3
result: .space 36                        # Espaço para matriz resultado (3x3)
lado: 	.word 3                          # Tamanho do lado da matriz
menu:	.asciz "Seja bem-vindo(a)! Escolha a operação: 1-Soma, 2-Multiplicação, 3-Transposta, 4-Imprime\n"

.text
.global main

main:
    addi s1, zero, 1
    addi s2, zero, 2
    addi s3, zero, 3
    addi s4, zero, 4

    # Exibe menu
    la a0, menu
    li a7, 4           # syscall para print string
    ecall

    # Lê a opção do usuário
    li a7, 5           # syscall para read int
    ecall
    mv t0, a0          # Armazena opção em t0
    

    # Decide operação
    beq t0, s1, chama_soma
    beq t0, s2, chama_multiplica
    #beq t0, s3, chama_transposta
    #beq t0, s4, chama_imprime
    
chama_soma:
    la a0, mat1        # Endereço da matriz 1
    la a1, mat2        # Endereço da matriz 2
    la a2, result      # Endereço da matriz resultado
    lw a3, lado        # Lado da matriz
    jal soma           # Chama função soma
    j main             # Retorna ao menu
    
chama_multiplica:
    la a0, mat1        # Endereço da matriz 1
    la a1, mat2        # Endereço da matriz 2
    la a2, result      # Endereço da matriz resultado
    lw a3, lado        # Lado da matriz
    jal multiplica     # Chama a função de multiplicação
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
    
# ------ funcao de soma
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
    
# ------ funcao de multiplicacao
multiplica:
    # Inicializa os índices para linha e coluna
    li t0, 0           # Índice da linha (i)

multiplica_linha:
    beq t0, a3, multiplica_fim  # Se t0 == lado, termina a multiplicação
    li t1, 0           # Índice da coluna (j)

multiplica_coluna:
    beq t1, a3, multiplica_proxima_linha  # Se t1 == lado, passa para próxima linha
    li t2, 0           # Inicializa índice acumulador (k)
    li t3, 0           # Inicializa acumulador (resultado da célula)

multiplica_acumula:
    beq t2, a3, multiplica_escreve  # Se t2 == lado, termina o somatório

    # Calcula endereço do elemento de mat1[i][k]
    mul t4, t0, a3     # t4 = linha * lado
    add t4, t4, t2     # t4 = linha * lado + k
    slli t4, t4, 2     # t4 = t4 * 4 (offset em bytes)
    add t4, a0, t4     # t4 = endereço base de mat1 + offset
    lw t5, 0(t4)       # t5 = mat1[i][k]

    # Calcula endereço do elemento de mat2[k][j]
    mul t6, t2, a3     # t6 = k * lado
    add t6, t6, t1     # t6 = k * lado + coluna
    slli t6, t6, 2     # t6 = t6 * 4 (offset em bytes)
    add t6, a1, t6     # t6 = endereço base de mat2 + offset
    lw s5, 0(t6)       # t7 = mat2[k][j]

    # Multiplica e acumula
    mul s6, t5, s5     # t8 = mat1[i][k] * mat2[k][j]
    add t3, t3, s6     # Soma o produto ao acumulador

    addi t2, t2, 1     # Incrementa k
    j multiplica_acumula

multiplica_escreve:
    # Calcula endereço do elemento de result[i][j]
    mul t4, t0, a3     # t4 = linha * lado
    add t4, t4, t1     # t4 = linha * lado + coluna
    slli t4, t4, 2     # t4 = t4 * 4 (offset em bytes)
    add t4, a2, t4     # t4 = endereço base de result + offset
    sw t3, 0(t4)       # Armazena o valor acumulado em result[i][j]

    addi t1, t1, 1     # Incrementa coluna (j)
    j multiplica_coluna

multiplica_proxima_linha:
    addi t0, t0, 1     # Incrementa linha (i)
    j multiplica_linha

multiplica_fim:
    jr ra              # Retorna para a função chamadora

fim:
    li a7, 10          # syscall para sair
    ecall