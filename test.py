class test:
	_hello = ['_','_']
	@property
	def hello(self):
		return self.__class__._hello
	@hello.setter
	def hello(self,newValue,m):
		self.__class__._hello[m] = newValue

	def another(self):
		self.hello = ['2','2']

j = test()
print(j.hello)
j.hello = ['_', '__hhh']
print(j.hello)
j.another()
print(j.hello)