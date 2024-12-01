.data
word:	.word 0xFAFEF1F0

TAB: 	.asciz "\t"
NL: 	.asciz	"\n"
Label:	.asciz "Teste"
l_ok:	.asciz	" OK"
l_fail:	.asciz	" FAIL"

.text

teste22:		# Testa SRL
	li t1, -1
	srli t2, t1, 24
	li a1, 22
	li t6, 255
	beq  t2, t6, t22_ok
	jal FAIL 
	j fim
t22_ok:
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
