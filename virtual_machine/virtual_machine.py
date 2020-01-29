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
	"""The Virtual Machine Executes Smart Contract Code"""

	def __init__(self):
		"""The state field keeps track of changes in data as the Virtual Machine executes"""

		self.state = {
			'programCounter': 0,
			'executionCounter': 0,
			'stack': [],
			'code': []
		}

	def jump(self):
		"""Performs a jump given a destination from the stack"""

		destination = self.state['stack'].pop()

		if destination < 0 or destination > len(self.state['code']):
			raise IndexError('Invalid destination: {x}.'.format(x=destination))

		self.state['programCounter'] = destination
		self.state['programCounter'] -= 1

	def runCode(self, code):
		"""Accepts and executes smart contract code"""

		# Update the state of the Virtual Machine with the code to be executed
		self.state['code'] = code

		# Iterate through the code array which contains instructions (opCode)
		while self.state['programCounter'] < len(self.state['code']):
			self.state['executionCounter'] += 1

			if self.state['executionCounter'] > EXECUTION_LIMIT:
				raise RecursionError(
					'Check for an infinite loop. Execution limit of {x} exceeded.'.format(x=EXECUTION_LIMIT)
				)

			opCode = self.state['code'][self.state['programCounter']]

			# try detects exceptions when they occur, this allows us to catch the exception and return the result of runCode execution
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
					# Pop two values off stack, perform an opCode and push result back onto stack
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
					# The jump instruction moves the program counter to another location in the code array. 
            		# It does this by popping one value off the stack which represents the destination (list index)
					# The program counter is then set equal to the destination
					self.jump()
				elif opCode == JUMPI:
					# Only jumps if the condition on the stack is 1
					condition = self.state['stack'].pop()

					if condition == 1:
						self.jump()
				else:
					break
			except ValueError:
					# Return the result of runCode if execution completed successfully (final value on stack)
					# Need to replace ValueError with custom exception
					print(EXECUTION_COMPLETE)
					return self.state['stack'][-1]

			self.state['programCounter'] += 1