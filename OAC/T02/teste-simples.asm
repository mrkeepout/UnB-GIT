.data
word:	.word 0xFAFEF1F0

TAB: 	.asciz "\t"
NL: 	.asciz	"\n"
Label:	.asciz "Teste"
l_ok:	.asciz	" OK"
l_fail:	.asciz	" FAIL"

.text

teste1:
	li t1, -2	# Testa ADD
	li t2, 3
	add t3, t1, t2
	li a1, 1
	li t6, 1	
	beq t3, t6, t1_ok
	jal FAIL
t1_ok:
	jal OK
	
fim:
	li a7, 10
	ecall		
	
	
OK:	# a1 eh o numero do teste
	la a0, Label
	li a7, 4
	ecall
	add a0, zero, a1
	li a7, 1
	ecall
	la a0, l_ok
	li a7, 4
	ecall
	la a0, NL
	ecall
	jr ra
	
FAIL:   # a1 eh o numero do teste
	la a0, Label
	li a7, 4
	ecall

	add a0, zero, a1
	li a7, 1
	ecall

	la a0, l_fail
	li a7, 4
	ecall
	la a0, NL
	ecall
	jr ra