.data
msg:    .asciz "Hello, World!\n"  # Mensagem a ser exibida

.text

    # Carregar o endereço da string no registrador a0
    la a0, msg            # a0 = endereço de msg

    # Carregar o código da chamada de sistema para print_string (64)
    li a7, 4             # a7 = código de syscall print_string

    # Executar a chamada de sistema
    ecall

    # Encerrar o programa (exit)
    li a7, 93             # a7 = código de syscall exit
    li a0, 0              # a0 = código de saída (0 = sucesso)
    ecall