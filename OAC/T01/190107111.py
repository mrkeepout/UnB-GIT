# Algoritmo para OAC - Trabalho 1
# Author: Gabriel Lucas França do Nascimento
# Matricula: 190107111
# Reaproveitei o meu código do semestre passado. 

import numpy as np

# Definição da memória como um arranjo de bytes de 32 bits
mem = np.zeros(16384, dtype=np.uint8)


# Função para ler um byte da memória e estender o sinal para 32 bits
def lb(reg, kte):
    address = reg + kte
    byte = np.int8(mem[address])
    return hex(np.int32(byte) & 0xffffffff)


# Função para ler um byte da memória sem sinal
def lbu(reg, kte):
    address = reg + kte
    return hex(np.uint32(mem[address]))


# Função para ler uma palavra de 32 bits da memória
def lw(reg, kte):
    address = reg + kte
    word = 0
    for i in range(4):
        word |= np.uint32(mem[address + i]) << (8 * i)
    return hex(word)


# Função para escrever um byte na memória
def sb(reg, kte, byte):
    address = reg + kte
    mem[address] = np.uint8(byte)


# Função para escrever uma palavra de 32 bits na memória
def sw(reg, kte, word):
    address = reg + kte
    for i in range(4):
        mem[address + i] = np.uint8((word >> (8 * i)) & 0xFF)


# Execução das instruções conforme o exemplo fornecido
sw(0, 0, 0xABACADEF)
sb(4, 0, 1)
sb(4, 1, 2)
sb(4, 2, 3)
sb(4, 3, 4)

print("Dados escritos na memória:")
for i in range(8):
    print(hex(mem[i]))

print("\nDados lidos da memória:")
print(lw(0, 0))
print(lb(0, 0))  # Extensão de sinal para 32 bits
print(lb(0, 1))  # Extensão de sinal para 32 bits
print(lb(0, 2))  # Extensão de sinal para 32 bits
print(lb(0, 3))  # Extensão de sinal para 32 bits
print(lbu(0, 0))
print(lbu(0, 1))
print(lbu(0, 2))
print(lbu(0, 3))
