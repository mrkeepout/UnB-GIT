# Simulador RISC-V
# Gabriel Lucas França do Nascimento
# 190107111
# OAC - 2024/2


import numpy as np

# Configuração da memória e registradores
MEM_SIZE = 16384  # 16 KB de memória
mem = np.zeros(MEM_SIZE, dtype=np.uint8)

# Registradores RISC-V
reg = np.zeros(32, dtype=np.int32)  # Registradores x0-x31
pc = 0  # Program Counter (PC)

# Constantes para syscalls - reg a0-a7 = 10-17; registrador a7 = 17
SYSCALL_PRINT_INT = 1
SYSCALL_PRINT_STR = 4
SYSCALL_EXIT = 10
encerrar = False

# Carregar memória a partir de arquivos binários
def load_mem(code_file, data_file):
    # Carrega segmento de código
    with open(code_file, 'rb') as f:
        code = f.read()
    mem[:len(code)] = np.frombuffer(code, dtype=np.uint8)
    
    # Carrega segmento de dados
    with open(data_file, 'rb') as f:
        data = f.read()
    mem[0x2000:0x2000 + len(data)] = np.frombuffer(data, dtype=np.uint8)


# Função para ler um byte da memória e estender o sinal para 32 bits
def lb(reg, offset):
    address = reg + offset
    byte = np.int8(mem[address])
    return hex(np.int32(byte) & 0xffffffff)


# Função para ler um byte da memória sem sinal
def lbu(reg, offset):
    address = reg + offset
    return hex(np.uint32(mem[address]))


# Função para ler uma palavra de 32 bits da memória
def lw(reg, offset):
    address = reg + offset
    word = 0
    for i in range(4):
        word |= np.uint32(mem[address + i]) << (8 * i)
    return hex(word)


# Função para escrever um byte na memória
def sb(reg, offset, byte):
    address = reg + offset
    mem[address] = np.uint8(byte)


# Função para escrever uma palavra de 32 bits na memória
def sw(reg, offset, word):
    address = reg + offset
    for i in range(4):
        mem[address + i] = np.uint8((word >> (8 * i)) & 0xFF)


# Execução das instruções conforme o exemplo forneci
#print("Dados escritos na memória:")
#for i in range(8):
#    print(hex(mem[i]))

#print("\nDados lidos da memória:")
#print(lw(0, 0))
#print(lb(0, 0))  # Extensão de sinal para 32 bits
#print(lb(0, 1))  # Extensão de sinal para 32 bits
#print(lb(0, 2))  # Extensão de sinal para 32 bits
#print(lb(0, 3))  # Extensão de sinal para 32 bits
#print(lbu(0, 0))
#print(lbu(0, 1))
#print(lbu(0, 2))
#print(lbu(0, 3))



# Função para ler uma palavra da memória
def read_word(address):
    return int.from_bytes(mem[address:address+4], byteorder='little', signed=True)

# Função para escrever uma palavra na memória
def write_word(address, value):
    mem[address:address+4] = value.to_bytes(4, byteorder='little', signed=True)

# Fetch: busca a instrução da memória
def fetch():
    global pc
    instruction = read_word(pc)
    pc += 4
    return instruction

# Decode: decodificação da instrução
def decode(instruction):
    opcode = instruction & 0x7F
    rd = (instruction >> 7) & 0x1F
    funct3 = (instruction >> 12) & 0x7
    rs1 = (instruction >> 15) & 0x1F
    rs2 = (instruction >> 20) & 0x1F
    funct7 = (instruction >> 25) & 0x7F

    #if opcode == 0x13 or opcode == 0


    imm_i = (instruction >> 12) & 0xFFFFF
    return opcode, rd, funct3, rs1, rs2, funct7, imm_i

# Execute: executa a instrução
def execute(opcode, rd, funct3, rs1, rs2, funct7, imm_i):
    global pc


    if opcode == 0x13:  # Tipo I (ADDI, ANDI, ORI, etc.)
        if funct3 == 0x0:  # ADDI
            reg[rd] = reg[rs1] + imm_i
        elif funct3 == 0x7:  # ANDI
            reg[rd] = reg[rs1] & imm_i
        elif funct3 == 0x6:  # ORI
            reg[rd] = reg[rs1] | imm_i
        elif funct3 == 0x4:  # XORI
            reg[rd] = reg[rs1] ^ imm_i
        elif funct3 == 0x2:  # LW
            address = reg[rs1] + imm_i
            reg[rd] = read_word(address)
        elif funct3 == 0x0:  # JALR
            temp = pc
            pc = (reg[rs1] + imm_i) & ~1
            reg[rd] = temp


    elif opcode == 0x33:  # Tipo R
        if funct3 == 0x0 and funct7 == 0x00:  # ADD
            reg[rd] = reg[rs1] + reg[rs2]
        elif funct3 == 0x0 and funct7 == 0x20:  # SUB
            reg[rd] = reg[rs1] - reg[rs2]
        elif funct3 == 0x7 and funct7 == 0x00:  # AND
            reg[rd] = reg[rs1] & reg[rs2]
        elif funct3 == 0x6 and funct7 == 0x00:  # OR
            reg[rd] = reg[rs1] | reg[rs2]
        elif funct3 == 0x4 and funct7 == 0x00:  # XOR
            reg[rd] = reg[rs1] ^ reg[rs2]
        elif funct3 == 0x2 and funct7 == 0x00:  # SLT
            reg[rd] = 1 if reg[rs1] < reg[rs2] else 0
        elif funct3 == 0x3 and funct7 == 0x00:  # SLTU
            reg[rd] = 1 if (reg[rs1] & 0xFFFFFFFF) < (reg[rs2] & 0xFFFFFFFF) else 0


    elif opcode == 0x23:  # Tipo S
        if funct3 == 0x2:  # SW
            address = reg[rs1] + imm_i
            write_word(address, reg[rs2])
        elif funct3 == 0x0:  # SB
            address = reg[rs1] + imm_i
            mem[address:address+1] = (reg[rs2] & 0xFF).to_bytes(1, byteorder='little')


    elif opcode == 0x63:  # Tipo B
        if funct3 == 0x0:  # BEQ
            if reg[rs1] == reg[rs2]:
                pc += imm_i
        elif funct3 == 0x1:  # BNE
            if reg[rs1] != reg[rs2]:
                pc += imm_i
        elif funct3 == 0x4:  # BLT
            if reg[rs1] < reg[rs2]:
                pc += imm_i
        elif funct3 == 0x5:  # BGE
            if reg[rs1] >= reg[rs2]:
                pc += imm_i
        elif funct3 == 0x6:  # BLTU
            if (reg[rs1] & 0xFFFFFFFF) < (reg[rs2] & 0xFFFFFFFF):
                pc += imm_i
        elif funct3 == 0x7:  # BGEU
            if (reg[rs1] & 0xFFFFFFFF) >= (reg[rs2] & 0xFFFFFFFF):
                pc += imm_i


    elif opcode == 0x17:  # AUIPC
        reg[rd] = pc + (imm_i << 12)

    elif opcode == 0x37:  # LUI
        reg[rd] = imm_i << 12

    elif opcode == 0x6F:  # JAL
        reg[rd] = pc + 4
        pc += imm_i

    elif opcode == 0x73:  # ECALL - imprimir inteiro, string e encerrar

        if reg[10] == SYSCALL_PRINT_INT:
            print(reg[11])

        elif reg[10] == SYSCALL_PRINT_STR:
            print(f"Endereço da string em a0: 0x{reg[11]:04X}")
            addr = 0x2000
            #addr = reg[11]  # Endereço da string em a0
            string = ""
            while True:
                byte = mem[addr]  # Lê um byte da memória
                print(byte)
                if byte == 0:  # Termina ao encontrar o caractere nulo
                    break
                string += chr(byte)  # Converte o byte em caractere
                addr += 1  # Avança para o próximo byte
            print(string)  

        elif reg[10] == SYSCALL_EXIT:
            encerrar = True
def step():
        instruction = fetch()
        opcode, rd, funct3, rs1, rs2, funct7, imm_i = decode(instruction)
        execute(opcode, rd, funct3, rs1, rs2, funct7, imm_i)
    

# Run: executa o programa até o fim
def run():
    global encerrar
    while encerrar == False:
        step()
        print(pc)
        if pc > 8192:
            encerrar = True
    exit()

# Exemplo de uso
# Carregar os binários gerados pelo RARS

# Carregamento do ambiente de teste - temporário
load_mem("code.bin", "data.bin")
run()
