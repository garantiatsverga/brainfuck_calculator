from math import inf
from pathlib import Path
from .interpreter import BrainfuckInterpreter


class Orchestrator:
    def __init__(self, modules_dir="bf_modules", interpreter=None):
        self.modules_dir = Path(modules_dir)
        self.interpreter = interpreter or BrainfuckInterpreter()
        
        # Load Brainfuck modules for 8-bit mode
        self.operations = {
            '+': self._load_module('addition.bf'),
            '-': self._load_module('subtraction.bf'),
            '*': self._load_module('multiplication.bf'),
            '/': self._load_module('division.bf'),
            '^': self._load_module('power.bf')
        }
    
    def _load_module(self, filename):
        filepath = self.modules_dir / filename
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return ''.join(c for c in content if c in '><+-.,[]')
    
    # Big number (past 255) functions
    @staticmethod
    def _split_to_cells(number):
        """Split a number into base-256 cells"""
        if number == 0:
            return [0]
        
        n = abs(number)
        cells = []
        
        while n > 0:
            cells.append(n & 0xFF)  # n % 256
            n >>= 8                  # n // 256
        
        return cells
    
    @staticmethod
    def _cells_to_number(cells):
        """Convert cells back to a number"""
        if not cells:
            return 0
        
        result = 0
        for i, digit in enumerate(cells):
            result += digit << (8 * i)  # digit * (256 ** i)
        
        return result
    
    def _add_big_numbers(self, a_cells, b_cells):
        """Add big numbers"""
        result = []
        carry = 0
        max_len = max(len(a_cells), len(b_cells))
        
        for i in range(max_len):
            a_val = a_cells[i] if i < len(a_cells) else 0
            b_val = b_cells[i] if i < len(b_cells) else 0
            
            total = a_val + b_val + carry
            
            if total >= 256:
                total -= 256
                carry = 1
            else:
                carry = 0
            
            result.append(total)
        
        if carry:
            result.append(1)
        
        # Remove leading zeros
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        
        return result
    
    def _subtract_big_numbers(self, a_cells, b_cells):
        """Subtract big numbers"""
        # Check if result will be negative
        a_int = self._cells_to_number(a_cells)
        b_int = self._cells_to_number(b_cells)
        
        if a_int < b_int:
            # Brainfuck doesn't support negative numbers =(
            return [0]
        
        result = []
        borrow = 0
        max_len = max(len(a_cells), len(b_cells))
        
        for i in range(max_len):
            a_val = a_cells[i] if i < len(a_cells) else 0
            b_val = b_cells[i] if i < len(b_cells) else 0
            
            diff = a_val - b_val - borrow
            
            if diff < 0:
                diff += 256
                borrow = 1
            else:
                borrow = 0
            
            result.append(diff)
        
        # Remove leading zeros
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        
        return result
    
    def _multiply_big_numbers(self, a_cells, b_cells):
        """Multiply big numbers"""
        # Quick checks
        if not a_cells or not b_cells or a_cells == [0] or b_cells == [0]:
            return [0]
        
        if a_cells == [1]:
            return b_cells.copy()
        
        if b_cells == [1]:
            return a_cells.copy()
        
        # For medium-sized numbers use direct conversion
        a_int = self._cells_to_number(a_cells)
        b_int = self._cells_to_number(b_cells)
        
        # If numbers aren't too big, calculate directly
        if a_int.bit_length() + b_int.bit_length() <= 64:
            result_int = a_int * b_int
            return self._split_to_cells(result_int)
        
        # For big numbers use multiplication algorithm
        result_size = len(a_cells) + len(b_cells)
        result = [0] * result_size
        
        for i, a_digit in enumerate(a_cells):
            if a_digit == 0:
                continue
                
            carry = 0
            for j, b_digit in enumerate(b_cells):
                product = a_digit * b_digit + result[i + j] + carry
                result[i + j] = product & 0xFF
                carry = product >> 8
            
            # Carry the remainder
            if carry:
                result[i + len(b_cells)] += carry
        
        # Handle carries
        for i in range(result_size - 1):
            if result[i] >= 256:
                result[i + 1] += result[i] >> 8
                result[i] &= 0xFF
        
        # Remove leading zeros
        while len(result) > 1 and result[-1] == 0:
            result.pop()
        
        return result
    
    def _divide_big_numbers(self, a_cells, b_cells):
        """Divide big numbers"""
        # Check division by zero
        if not b_cells or b_cells == [0]:
            raise ZeroDivisionError("Division by zero")
        
        if b_cells == [1]:
            return a_cells.copy()
        
        # Convert to integers
        a_int = self._cells_to_number(a_cells)
        b_int = self._cells_to_number(b_cells)
        
        if a_int < b_int:
            return [0]
        
        quotient_int = a_int // b_int
        return self._split_to_cells(quotient_int)
    
    def _power_big_numbers(self, a_cells, b_cells):
        """Power of big numbers"""
        # Quick checks
        if not b_cells or b_cells == [0]:
            return [1]  # a^0 = 1
        
        if b_cells == [1]:
            return a_cells.copy()  # a^1 = a
        
        if not a_cells or a_cells == [0]:
            return [0]  # 0^b = 0
        
        if a_cells == [1]:
            return [1]  # 1^b = 1
        
        # Convert to integers
        a_int = self._cells_to_number(a_cells)
        b_int = self._cells_to_number(b_cells)
        
        # Check for too large exponent
        if b_int > 1000:
            raise ValueError(f"Exponent is too large: {b_int}")
        
        # Estimate result size
        estimated_bits = b_int * a_int.bit_length()
        if estimated_bits > 1000000:
            raise ValueError(f"Result will be too large")
        
        # Calculate power
        try:
            result_int = pow(a_int, b_int)
        except (OverflowError, MemoryError):
            raise ValueError(f"Overflow when calculating {a_int}^{b_int}")
        
        # Convert back to cells
        return self._split_to_cells(result_int)
    
    def _execute_big_operation(self, op, a, b):
        """Execute operation with big numbers"""
        # Convert numbers to cells
        a_cells = self._split_to_cells(a)
        b_cells = self._split_to_cells(b)
        
        # Execute operation
        if op == '+':
            result_cells = self._add_big_numbers(a_cells, b_cells)
        elif op == '-':
            result_cells = self._subtract_big_numbers(a_cells, b_cells)
        elif op == '*':
            result_cells = self._multiply_big_numbers(a_cells, b_cells)
        elif op == '/':
            result_cells = self._divide_big_numbers(a_cells, b_cells)
        elif op == '^':
            result_cells = self._power_big_numbers(a_cells, b_cells)
        else:
            raise ValueError(f"Unsupported operation: '{op}'")
        
        # Convert back to number
        return self._cells_to_number(result_cells)
    
    # Public interface
    
    def _prepare_input(self, a, b):
        """Prepare input data for Brainfuck"""
        return bytes([a % 256, b % 256])
    
    def execute_operation(self, operation, a, b):
        """Execute operation via Brainfuck (8-bit mode)"""
        if operation not in self.operations:
            raise ValueError(f"Unsupported operation: '{operation}'")
        
        if operation == '/' and b == 0:
            return inf
        
        bf_code = self.operations[operation]
        if bf_code is None:
            raise ValueError(f"Module for operation '{operation}' not found")
        
        input_data = self._prepare_input(a, b)
        output = self.interpreter.execute(bf_code, input_data)
        
        return output[0] if output else 0
    
    def parse_expression(self, expression):
        """Parse expression into operation and operands"""
        expression = expression.replace(' ', '')
        operations = ['^', '*', '/', '+', '-']
        
        for op in operations:
            if op in expression:
                parts = expression.split(op, 1)
                if len(parts) == 2:
                    try:
                        a = int(parts[0])
                        b = int(parts[1])
                        return op, a, b
                    except ValueError:
                        continue
        
        raise ValueError(f"Cannot parse expression: '{expression}'")
    
    def calculate(self, expression):
        """Main calculation method - always uses big numbers"""
        op, a, b = self.parse_expression(expression)
        return self._execute_big_operation(op, a, b)
    
    def calculate_8bit(self, expression):
        """Calculation in 8-bit mode (for compatibility only)"""
        op, a, b = self.parse_expression(expression)
        return self.execute_operation(op, a, b)
    
    def batch_calculate(self, expressions):
        """Batch calculation of multiple expressions"""
        results = []
        for expr in expressions:
            try:
                result = self.calculate(expr)
                results.append((expr, result))
            except Exception as e:
                results.append((expr, f"ERROR: {e}"))
        
        return results