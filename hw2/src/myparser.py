import compiler
class MyParser:
	lexer = None
	parser = None
	stmtList = None
	
	def __init__(self):
		reserved = {'print' : 'PRINT',
					'input' : 'INPUT'}
		
		tokens = ['INT','PLUS','ASSIGN','NEGATE','NAME', 'R_PAREN', 'L_PAREN'] + list(reserved.values())
	
		t_PLUS  = r'\+'
		t_ASSIGN= r'='
		t_NEGATE= r'-'
		t_R_PAREN= r'\)'
		t_L_PAREN= r'\('
		t_ignore_COMMENT = r'\#.*' #ignore comments
		
		# Taken from the PLY documentation: http://www.dabeaz.com/ply/ply.html#ply_nn6
		def t_NAME(t):
			r'[a-zA-Z_][a-zA-Z_0-9]*'
			t.type = reserved.get(t.value,'NAME')    # Check for reserved words
			return t

		#def t_FUNC(t):
		#	r'[a-zA-Z]+()'
		#	t.value = t.value[:len(t.value)-2]
		#	return t

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
		
		#------------- PARSER
		
		from compiler.ast import Printnl, Add, Const, UnarySub, CallFunc, Assign, AssName, Module, Stmt, Name, Expression

		#define precedence
		precedence = (
			('right','ASSIGN'),
			('left','PLUS'),
			('right', 'NEGATE'),
			('left','L_PAREN','R_PAREN'),
		)
		
		# Empty statement object that the parser will add to.
		self.stmtList = Stmt([])

		#define parse logic
		def p_program_module(t):
			'program : module'	
			t[0] = Module(None, t[1])
		def p_module_statement(t):
			'module : statement'
			t[0] = t[1]
		def p_statements_statement(t):
			'''statement : statement simple_statement
						| simple_statement'''
			if( len(t) == 2 ):
				self.stmtList.nodes.append(t[1])
			elif( len(t) == 3):
				self.stmtList.nodes.append(t[2])
			t[0]=self.stmtList
#		def p_empty_statement(t):
#			'simple_statement : '
#			t[0]=self.stmtList
		def p_print_statement(t):
			'simple_statement : PRINT expression'
			t[0] = Printnl([t[2]], None)
		def p_assign_statement(t):
			'simple_statement : NAME ASSIGN expression'
			t[0] = Assign([AssName(t[1],'OP_ASSIGN')],t[3])
		def p_expression_statement(t):
			'simple_statement : expression'
			t[0] = t[1]
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
			'expression : INPUT L_PAREN R_PAREN'
			t[0] = CallFunc(Name(t[1]),[],None,None)
		def p_l_paren_expression_r_paren(t):
			'expression : L_PAREN expression R_PAREN'
			t[0] = t[2]
		
		def p_error(t):
			print "Syntax Error at '%s'" % t.value
		
		import ply.yacc as yacc
		self.parser = yacc.yacc()

		
	def testLexer(self, to_lex):
		self.lexer.input(to_lex)
		while True:
			tok = self.lexer.token()
			if not tok: break
			print tok

	# Desc: Clears the list of statements that the parser appends to
	#	as it builds the tree. Needs to be called in between calls
	#	to parse() and parseFile()
	def clearStatements(self):
		self.stmtList.nodes=[]
	
	def parseFile(self, path):
		self.clearStatements()
		file_to_parse = open(path, 'r')
		text_to_parse = file_to_parse.read()
		return self.parser.parse(text_to_parse)

	def parse(self, to_parse):
		# Clear stmtList. See comment in parseFile()
		self.clearStatements()
		return self.parser.parse(to_parse)
