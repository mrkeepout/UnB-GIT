#Código em Python - Simulador processador RISC-V
#Autor: Gabriel Lucas França do Nascimento
#Disciplina: Organização e Arquitetura de Computadores
#Professor: Dr. Ricardo Jacobi

import sys

registradores = {
    'zero'  : 0,
    'ra'    : 1,
    'sp'    : 2,
    'gp'    : 3,
    'tp'    : 4,
    't0'    : 5,
    't1'    : 6,
    't2'    : 7,
    's0'    : 8,
    's1'    : 9,
    'a0'    : 10,
    'a1'    : 11,
    'a2'    : 12,
    'a3'    : 13,
    'a4'    : 14,
    'a5'    : 15,
    'a6'    : 16,
    'a7'    : 17,
    's2'    : 18,
    's3'    : 19,
    's4'    : 20,
    's5'    : 21,
    's6'    : 22,
    's7'    : 23,
    's8'    : 24,
    's9'    : 25,
    's10'   : 26,
    's11'   : 27,
    't3'    : 28,
    't4'    : 29,
    't5'    : 30,
    't6'    : 31,
}

# Opcode para instruções tipo R - passivo de otimizacao
tipo_r = {
    'and' : '0110011',
    'sub' : '0110011',
    'slt' : '0110011',
    'sltu': '0110011',
    'xor' : '0110011',
    'or'  : '0110011',
    'add' : '0110011',
}

tipo_i = {
    'andi' : '0010011',
    'addi' : '0010011',
    'lb'   : '0000011',
    'lbu'  : '0000011',
    'lw'   : '0000011',
    'slli' : '0010011',
    'srai' : '0010011',
    'srli' : '0010011',
    'ori'  : '0010011',
    'jalr' : '1100111',
    'ecall': '1110011',
}

tipo_u = {
    'lui'   : '0110111',
    'auipc' : '0010111'
}

tipo_j = {
    'jal' : '1101111'
}

tipo_b = {
    'beq' : '1100011',
    'bne' : '1100011',
    'blt' : '1100011',
    'bge' : '1100011',
    'bltu': '1100011',
    'bgeu': '1100011'
}

tipo_s = {
    'sb' : '0100011',
    'sw' : '0100011'
}


if __name__ == '__main__':
    main()
