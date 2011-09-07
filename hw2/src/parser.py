import lexer
class Parser:	
	parser = None
	#this is our grammar in P0++
	# 		program ::= module
	#             module ::= simple_statement+
	#             simple_statement ::= "print" expression
	#                                | name "=" expression
	#                                | expression
	#             expression ::= name
	#                          | decimalinteger
	#                          | "-" expression
	#                          | expression "+" expression
	#                          | "(" expression ")"
	#                          | "input" "(" ")"
	def __init__(self):
		from compiler.ast import Printnl, Add, Const, UnarySub, CallFunc, Assign, AssName
		lex = lexer.Lexer()
		tokens = lex.getTokens()
		#define precedence
		precedence = (
			('right','ASSIGN'),
			('left','PLUS'),
			('right', 'NEGATE'),
			('left','L_PAREN','R_PAREN')
		)
		
		#define parse logic
		def p_print_statement(t):
			'statement : PRINT expression'
			t[0] = Printnl([t[2]], None)
		def p_assign_statement(t):
			'statement : NAME = expression'
			t[0] = Assign(AssName(t[1],'OP_ASSIGN'),t[3])
		
		def p_plus_expression(t):
			'expression : expression PLUS expression'
			t[0] = Add((t[1], t[3]))
		def p_negate_expression(t):
			'expression : NEGATE expression'
			t[0] = UnarySub(t[2])
		def p_int_expression(t):
			'expression : INT'
			t[0] = Const(t[1])
		def p_name_expression(t):
			'expression : NAME'
			t[0] = Name(t[1])
		def p_func_expression(t):
			'expression : FUNC'
			t[0] = CallFunc(t[1],None,None,None)
		def p_l_paren_expression_r_paren(t):
			'expression : L_PAREN expression R_PAREN'
			t[0] = t[2]
		
		def p_error(t):
			print "Syntax Error at '%s'" % t.value
		
		import ply.yacc as yacc
		self.parser = yacc.yacc()
