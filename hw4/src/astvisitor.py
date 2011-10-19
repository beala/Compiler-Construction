class ASTVisitor(object):
	def visit(self, node):
		'''Visit a node'''
		# Find a specific visit method. Default to "default".
		methname = "visit_%s" % node.__class__.__name__
		method = getattr(self, methname, self.default)
		return method(node)
	
	def default(self, node):
		'''Visit node children'''
		print "Uh oh: A method doesn't exist for this node type: %s" % node.__class__.__name__
