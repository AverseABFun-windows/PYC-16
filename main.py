class ByteStr(str):
	def __init__(self, o, **kwargs):
		chars = set('`~23456789!@#$%^&*()-_=+qwertyuiop[]\\QWERTYUIOP{}|asdfghjkl;\'ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?')
		if any((c in chars) for c in o):
			raise ValueError(o, 'bad characters')
		else:
			super().__init__(o, **kwargs)

class Memory:
	def __init__(self, data:ByteStr):
		if len(data) != 16:
			raise ValueError(data, 'inapproprate length')
		else:
			self.data = data
	def __str__(self):
		return self.data

class List(list):

    def __init__(self, type=None, iterable=None, maxsize=536870912):
        """Override initializer which can accept iterable"""
        super(List, self).__init__()
        self.type = type
        self.maxsize = maxsize
        if iterable:
            for item in iterable:
                self.append(item)

    def append(self, item):
        if isinstance(item, self.type) and len(self)+1 <= self.maxsize:
            super(List, self).append(item)
        else:
            raise TypeError(item)

    def insert(self, index, item):
        if isinstance(item, self.type) and len(self)+1 <= self.maxsize:
            super(List, self).insert(index, item)
        else:
            raise TypeError(item)

    def __add__(self, item):
        if isinstance(item, self.type) and len(self)+item <= self.maxsize:
            super(List, self).__add__(item)
        else:
            raise TypeError(item)

    def __iadd__(self, item):
        if isinstance(item, self.type):
            super(List, self).__iadd__(item)
        else:
            raise TypeError(item)


class ExtPort:
	def __init__(self, port, var):
		self.port = port
		self.var = var
	def update(self):
		mmo[ByteStr(str(bin(self.port)))] = globals()[self.var]

class Data(object):
	def __init__(self):
		self._data = {
			"vars": []
		}

	@property
	def vars(self):
		return self._data["vars"]
class Pixel:
	def __init__(self):
		self.red, self.green, self.blue = (0,0,0)

	@property
	def red(self):
		return self.red
	@property
	def green(self):
		return self.green
	@property
	def blue(self):
		return self.blue

class Command:
	def __init__(self, *args):
		self.args = args
	def process(self):
		raise NotImplementedError()
class Error:
	def __init__(self, *args):
		self.data = args
	def __str__(self):
		return self.data
memory = List(type=Memory, maxsize=500000)
data = Data()
mmo = List(type=Memory, maxsize=500000)

width, height=(500,500)

ports = List(type=ExtPort, maxsize=4)
screen = List(type=Pixel, maxsize=width*height)

errorStack = List(type=Error)

v=0
while True:
	try:
		memory.append(Memory(ByteStr('0000000000000000')))
	except:
		break
while True:
	try:
		mmo.append(Memory(ByteStr('0000000000000000')))
	except:
		break
while True:
	try:
		ports.append(ExtPort(bin(v),"ext"+str(v)))
	except:
		break
	v = v+1

rega = 0b0
regb = 0b0
regc = 0b0
regp = memory[rega]

class Gate:
	def __init__(self, *args):
		return self.gate(*args)
	def gate(self, *args):
		raise NotImplementedError()

class And(Gate):
	def gate(self, *args):
		result = args[0]
		for i in args:
			try:
				result = result and args[i+1]
			except:
				pass
		return result

class Or(Gate):
	def gate(self, *args):
		result = args[0]
		for i in args:
			try:
				result = result or args[i+1]
			except:
				pass
		return result

class Nand(Gate):
	def gate(self, *args):
		result = args[0]
		for i in args:
			try:
				result = result and args[i+1]
			except:
				pass
		return not result

class Nor(Gate):
	def gate(self, *args):
		result = args[0]
		for i in args:
			try:
				result = result or args[i+1]
			except:
				pass
		return not result


class MemGate(Gate):
	def __init__(self, x):
		return self.gate(x)
	def gate(self, x):
		raise NotImplementedError()
class GetMem(MemGate):
	def gate(self, x):
		global memory
		return memory[x]

class SetMem(MemGate):
	def __init__(self, x, y):
		return self.gate(x, y)
	def gate(self, x, y):
		try:
			global memory
			memory[x] = y
			return memory[x]
		except:
			return And(x, y)



class GetReg(MemGate):
	def gate(self, x):
		return globals()['reg'+chr(x)]

class SetReg(MemGate):
	def __init__(self, x, y):
		return self.gate(x, y)
	def gate(self, x, y):
		try:
			globals()['reg'+chr(x)] = y
			return globals()['reg'+chr(x)]
		except:
			return And(x, y)


class Move(Command):
	def process(self):
		if len(self.args) < 3:
			errorStack.append(Error('0b101'))
			return
		if self.args[2] == 0b1:
			mmo[self.args[0]] = self.args[1]
		else:
			memory[self.args[0]] = self.args[1]