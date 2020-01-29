import pytest
from virtual_machine import VirtualMachine
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

def test_add():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 4, ADD, STOP]) == 7

def test_sub():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 4, SUB, STOP]) == 1

def test_mul():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 4, MUL, STOP]) == 12

def test_div():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 6, DIV, STOP]) == 2

def test_LT():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 4, LT, STOP]) == 0

def test_GT():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 4, GT, STOP]) == 1

def test_EQ():
    assert VirtualMachine().runCode([PUSH, 3, PUSH, 4, EQ, STOP]) == 0

def test_and():
    assert VirtualMachine().runCode([PUSH, 0, PUSH, 1, AND, STOP]) == 0

def test_or():
    assert VirtualMachine().runCode([PUSH, 0, PUSH, 1, OR, STOP]) == 1

def test_jump():
    assert VirtualMachine().runCode(
        [PUSH, 6, JUMP, PUSH, 0, JUMP, PUSH, 'jump successful', STOP]
    ) == 'jump successful'

def test_jumpi():
    assert VirtualMachine().runCode(
        [PUSH, 8, PUSH, 1, JUMPI, PUSH, 0, JUMP, PUSH, 'jumpi successful', STOP]
    ) == 'jumpi successful'

def test_invalid_jump_destination():
    with pytest.raises(IndexError) as excinfo:
        VirtualMachine().runCode(
            [PUSH, 66, PUSH, 1, JUMPI, PUSH, 0, JUMP, PUSH, 'jumpi successful', STOP]
        )
    assert "Invalid destination" in str(excinfo.value)

def test_infinite_loop():
    with pytest.raises(RecursionError) as excinfo:
        VirtualMachine().runCode([PUSH, 0, JUMP, STOP])
    assert "infinite loop" in str(excinfo.value)

def test_push_instruction_last():
    with pytest.raises(RuntimeError) as excinfo:
        VirtualMachine().runCode([PUSH, 1, PUSH, 2, ADD, PUSH])
    assert "cannot be last" in str(excinfo.value)
