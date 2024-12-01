# Simulador RISC-V
# Gabriel Lucas França do Nascimento
# 190107111
# OAC - 2024/2
# Github: https://github.com/mrkeepout/UnB-GIT/tree/40e37c4c889ba180328d1cfeca2ba4cba94f7f5c/OAC/T02

import numpy as np

# Configuração da memória e registradores
MEM_SIZE = 16384  # 16 KB de memória
mem = np.zeros(MEM_SIZE, dtype=np.uint8)

# Registradores RISC-V
reg = np.zeros(32, dtype=np.int32)  # Registradores x0-x31
pc = 0  # Program Counter (PC)
reg[0] = 0 # Registrador zero sempre vale zero

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


# Função para ler uma palavra da memória
def read_word(address):
    return int.from_bytes(mem[address:address+4], byteorder='little', signed=True)

# Função para escrever uma palavra na memória
def write_word(address, value):
    #mem[address:address+4] = value.to_bytes(4, byteorder='little', signed=True)
    for i in range(4):
        mem[address + i] = np.uint8((value >> (8 * i)) & 0xFF)

# Fetch: busca a instrução da memória
def fetch():
    global pc
    instruction = read_word(pc)
    pc += 4
    return instruction

# Decode: decodificação da instrução
def decode(instruction):
    def get_field(value, offset, mask):
        return (value >> offset) & mask

    def set_field(value, offset, mask, field_value):
        value &= ~(mask << offset)  # Limpa o campo atual
        value |= (field_value & mask) << offset  # Insere o novo campo
        return value

    def get_bit(value, bit_position):
        return (value >> bit_position) & 1

    def set_bit(value, bit_position, bit_value):
        if bit_value:
            return value | (1 << bit_position)
        else:
            return value & ~(1 << bit_position)

    # Decodificação básica
    opcode = instruction & 0x7F
    rs2 = (instruction >> 20) & 0x1F
    rs1 = (instruction >> 15) & 0x1F
    rd = (instruction >> 7) & 0x1F
    shamt = (instruction >> 20) & 0x1F
    funct3 = (instruction >> 12) & 0x7
    funct7 = (instruction >> 25) & 0x7F

    # Imediatos
    imm12_i = instruction >> 20  # Estende sinal automaticamente no Python
    tmp = get_field(instruction, 7, 0x1F)
    imm12_s = set_field(imm12_i, 0, 0x1F, tmp)
    imm13 = imm12_s
    imm13 = set_bit(imm13, 11, imm12_s & 1)
    imm13 &= ~1
    imm20_u = instruction & (~0xFFF)

    # Imediato de 21 bits (imm21)
    imm21 = instruction >> 11  # Estende sinal automaticamente no Python
    tmp = get_field(instruction, 12, 0xFF)  # Campo [19:12]
    imm21 = set_field(imm21, 12, 0xFF, tmp)
    tmp = get_bit(instruction, 20)  # Bit 11 em ri(20)
    imm21 = set_bit(imm21, 11, tmp)
    tmp = get_field(instruction, 21, 0x3FF)  # Campo [10:1]
    imm21 = set_field(imm21, 1, 0x3FF, tmp)
    imm21 &= ~1  # Zera o bit 0

    # Retorna todos os campos necessários para execução da instrução
    return opcode, rd, funct3, rs1, rs2, funct7, imm12_i, imm12_s, imm13, imm21, imm20_u, shamt

# Execute: executa a instrução
def execute(opcode, rd, funct3, rs1, rs2, funct7, imm12_i, imm12_s, imm13, imm21, imm20_u, shamt):
    global pc
    reg[0] = 0  # Registrador zero sempre vale zero

    # Tipo I (ADDI, ANDI, ORI, etc.)
    if opcode == 0x13:
        if funct3 == 0x0:  # ADDI
            reg[rd] = reg[rs1] + imm12_i
        elif funct3 == 0x7:  # ANDI
            reg[rd] = reg[rs1] & imm12_i
        elif funct3 == 0x6:  # ORI
            reg[rd] = reg[rs1] | imm12_i
        elif funct3 == 0x4:  # XORI
            reg[rd] = reg[rs1] ^ imm12_i
        elif funct3 == 0x1 and funct7 == 0x00:  # SLLI
            reg[rd] = reg[rs1] << shamt
        elif funct3 == 0x5 and funct7 == 0x00:  # SRLI
            reg[rd] = np.uint32(reg[rs1]) >> shamt
        elif funct3 == 0x5 and funct7 == 0x20:  # SRAI
            reg[rd] = reg[rs1] >> shamt  # Shift aritmético

    # Load Functions
    elif opcode == 0x03: 
        if funct3 == 0x0: # LB
            address = reg[rs1] + imm12_i
            reg[rd] = np.int8(mem[address])
        elif funct3 == 0x2: # LW
            address = reg[rs1] + imm12_i
            reg[rd] = read_word(address)
        elif funct3 == 0x4: # LBU
            address = reg[rs1] + imm12_i
            reg[rd] = np.uint8(mem[address])
        
    # Jump Functions
    elif opcode == 0x67:  # JALR
        temp = pc - 4
        pc = int((reg[rs1] + imm12_i) & ~1)
        reg[rd] = temp

    # Tipo R (ADD, SUB, etc.)
    elif opcode == 0x33:
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

    # Tipo S (SW, SB)
    elif opcode == 0x23:
        if funct3 == 0x2:  # SW
            address = reg[rs1] + imm12_s
            write_word(address, reg[rs2])
        elif funct3 == 0x0:  # SB
            address = reg[rs1] + imm12_s
            mem[address] = np.uint8(reg[rs2])

    # Tipo B (Branch)
    elif opcode == 0x63:
        temp = pc - 4

        if funct3 == 0x0 and (reg[rs1] == reg[rs2]):  # BEQ
            pc = temp + imm13
        elif funct3 == 0x1 and (reg[rs1] != reg[rs2]):  # BNE
            pc = temp + imm13
        elif funct3 == 0x4 and (reg[rs1] < reg[rs2]):  # BLT
            pc = temp + imm13
        elif funct3 == 0x5 and (reg[rs1] >= reg[rs2]):  # BGE
            pc = temp + imm13
        elif funct3 == 0x6 and (np.uint32(reg[rs1]) < np.uint32(reg[rs2])):  # BLTU
            pc = temp + imm13
        elif funct3 == 0x7 and (np.uint32(reg[rs1]) >= np.uint32(reg[rs2])):  # BGEU
            pc = temp + imm13

    # Tipo U (AUIPC, LUI)
    elif opcode == 0x17:  # AUIPC
        reg[rd] = (pc-4) + imm20_u
    elif opcode == 0x37:  # LUI
        reg[rd] = imm20_u

    # Tipo J (JAL)
    elif opcode == 0x6F:  # JAL
        pc -= 4
        reg[rd] = pc + 4
        pc += imm21

    # ECALL - syscall
    elif opcode == 0x73:
        #print(reg[17])
        if reg[17] == SYSCALL_PRINT_INT:
            num = str(reg[10])
            print(f" {num}", end="")
        elif reg[17] == SYSCALL_PRINT_STR:
            addr = reg[10]
            string = ""
            while True:
                byte = mem[addr]
                if byte == 0: # Fim da string
                    break
                string += chr(byte)
                addr += 1
            print(string, end="")
        elif reg[17] == SYSCALL_EXIT:
            global encerrar 
            encerrar = True

def step():
        global pc

        instruction = fetch()

        (
            opcode,
            rd,
            funct3,
            rs1,
            rs2,
            funct7,
            imm12_i,
            imm12_s,
            imm13,
            imm21,
            imm20_u,
            shamt,
        ) = decode(instruction)

        execute(opcode, rd, funct3, rs1, rs2, funct7, imm12_i, imm12_s, imm13, imm21, imm20_u, shamt)

    

# Run: executa o programa até o fim
def run():
    global encerrar
    while encerrar == False:
        step()
        #print(pc)
        if pc > 8192:
            encerrar = True
    exit()

# Exemplo de uso
# Carregar os binários gerados pelo RARS

# Carregamento do ambiente de teste - temporário
load_mem("code.bin", "data.bin")
run()