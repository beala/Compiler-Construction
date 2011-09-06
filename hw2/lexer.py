class Lexer:
	lexer = None

	def __init__(self):
		tokens = ('PRINT','INT','PLUS','ASSIGN','NEGATE','FUNC', 'NAME', 'END_STMT', 'R_PAREN', 'L_PAREN')

		# FIX: All PRINTs turn into NAMEs
		t_PRINT = r'print'
		t_PLUS  = r'\+'
		t_ASSIGN= r'='
		t_NEGATE= r'-'
		t_END_STMT= r';'
		t_R_PAREN= r'\)'
		t_L_PAREN= r'\('
		t_NAME= r'[a-zA-Z_]*'

	#	def t_NAME(t):
	#		r'[A-Za-z_][\w_]*'
	#		t.type = reserved_map.get(t.value,"NAME")
	#		return t

		def t_FUNC(t):
			r'[a-zA-Z]+\(\)'
			t.value = t.value[:len(t.value)-2]
			return t

		def t_INT(t):
			r'\d+'
			try:
				t.value = int(t.value)
			except ValueError:
				print "Int value too large", t.value
				t.value = 0
			return t

		t_ignore = ' \t'

		def t_newline(t):
			r'\n+'
			t.lexer.lineno += t.value.count("\n")

		def t_error(t):
			print "Illegal character '%s'" % t.value[0]
			t.lexer.skip(1)

		import ply.lex as lex
		self.lexer = lex.lex()

	def test_lex(self, to_lex):
		self.lexer.input(to_lex)
		while True:
			tok = self.lexer.token()
			if not tok: break
			print tok
