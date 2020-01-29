from opcode_map import (
	STOP,
	ADD,
	SUB,
	MUL,
	DIV,
	PUSH,
	LT,
	GT,
	EQ,
	AND,
	OR,
	JUMP,
	JUMPI
)

from constants import (
	EXECUTION_COMPLETE,
	EXECUTION_LIMIT
)

class VirtualMachine(object):
	def __init__(self):
		self.state = {
			'programCounter': 0,
			'executionCounter': 0,
			'stack': [],
			'code': []
		}

	def jump(self):
		destination = self.state['stack'].pop()

		if destination < 0 or destination > len(self.state['code']):
			raise IndexError('Invalid destination: {x}.'.format(x=destination))

		self.state['programCounter'] = destination
		self.state['programCounter'] -= 1

	def runCode(self, code):
		self.state['code'] = code

		while self.state['programCounter'] < len(self.state['code']):
			self.state['executionCounter'] += 1

			if self.state['executionCounter'] > EXECUTION_LIMIT:
				raise RecursionError(
					'Check for an infinite loop. Execution limit of {x} exceeded.'.format(x=EXECUTION_LIMIT)
				)

			opCode = self.state['code'][self.state['programCounter']]

			try:
				if opCode == STOP:
					raise ValueError(EXECUTION_COMPLETE)
				elif opCode == PUSH:
					self.state['programCounter'] += 1

					if self.state['programCounter'] == len(self.state['code']):
						raise RuntimeError('The PUSH instruction cannot be last.')

					value = self.state['code'][self.state['programCounter']]
					self.state['stack'].append(value)
				elif opCode in (ADD, SUB, MUL, DIV, PUSH, LT, GT, EQ, AND, OR):
					a = self.state['stack'].pop()
					b = self.state['stack'].pop()

					result = None
					if opCode == ADD: 
						result = a + b
					elif opCode == SUB: 
						result = a - b
					elif opCode == MUL:
						result = a * b
					elif opCode == DIV:
						result = a / b
					elif opCode == LT:
						result = 1 if a < b else 0
					elif opCode == GT:
						result = 1 if a > b else 0
					elif opCode == EQ:
						result = 1 if a == b else 0
					elif opCode == AND:
						result = a and b
					elif opCode == OR:
						result = a or b

					self.state['stack'].append(result)	
				elif opCode == JUMP:
					self.jump()
				elif opCode == JUMPI:
					condition = self.state['stack'].pop()

					if condition == 1:
						self.jump()
				else:
					break
			except ValueError:
					print(EXECUTION_COMPLETE)
					return self.state['stack'][-1]

			self.state['programCounter'] += 1
