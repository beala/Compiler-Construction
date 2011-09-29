import compiler
from compiler import *
import myparser
import unittest

class TestMyParser(unittest.TestCase):
	parser=None
	# Tuple of test cases to cycle through
	test_cases=('print 1',
				'print 1\nprint 2',
				'print 1+2+3+-input()',
				'x=1+2+3+-input()+4',
				'x=1\nx=2\nx=input()\nprint (1+2+3)+-(1+33+(1))\n\n',
				'x=1 #Comment\n#Comment 2',
				#'',	# P0 doesn't contain empty stmts. Test fails.
				'x=1\ny=x+(-1)+(1+(1+(1))+-y)\nprint y',
				#'1+2+3',	#Discards don't compile correctly
				'input\n(1+3)'
			)

	def setUp(self):
		self.parser = myparser.MyParser()

	def test_all(self):
		for test in self.test_cases:
			self.assertEqual(str(self.parser.parse(test)),  str(compiler.parse(test)))

if __name__ == '__main__':
	unittest.main()

