class Lexer:
	lexer = None

	def __init__(self):
		reserved = {'print' : 'PRINT'}
		
		tokens = ['INT','PLUS','ASSIGN','NEGATE','FUNC', 'NAME', 'END_STMT', 'R_PAREN', 'L_PAREN'] + list(reserved.values())
	
		t_PLUS  = r'\+'
		t_ASSIGN= r'='
		t_NEGATE= r'-'
		t_END_STMT= r';'
		t_R_PAREN= r'\)'
		t_L_PAREN= r'\('
		
		# Taken from the PLY documentation: http://www.dabeaz.com/ply/ply.html#ply_nn6
		def t_NAME(t):
			r'[a-zA-Z_][a-zA-Z_0-9]*'
			t.type = reserved.get(t.value,'NAME')    # Check for reserved words
			return t

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
