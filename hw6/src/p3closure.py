from p2closure import *

class P3Closure(P2Closure):
	def visit_If(self, node):
		(body_tests_test, funs_tests_test) = self.visit(node.tests[0][0])
		(body_tests_then, funs_tests_then) = self.visit(node.tests[0][1])
		(body_else_, funs_else_) = self.visit(node.else_)
		return (If([(body_tests_test, body_tests_then)], body_else_), funs_tests_test, funs_tests_then, funs_else_)

	def visit_While(self, node):
		(body_test, funs_test) = self.visit(node.test)
		(body_body, funs_body) = self.visit(node.body)
		return (While(body_test, body_body, None), funs_test + funs_body)
