from p2explicate import *
class P3Explicate(P2Explicate):
	def visit_If(self,node):
		myTest = self.visit(node.tests[0][0])
		myThen = self.visit(node.tests[0][1])
		myElse_ = self.visit(node.else_)
		tmpMyTest = Name(self._makeTmpVar())
		return Let( tmpMyTest, myTest, If([(tmpMyTest,myThen)],myElse_))
	def visit_While(self, node):
		myTest = self.visit(node.test)
		myBody = self.visit(node.body)
		tmpMyTest = Name(self._makeTmpVar())
		return Let( tmpMyTest, myTest, While(myTest, myBody, None)) 
