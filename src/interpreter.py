# Is welcome to use!

class BrainfuckInterpreter:
    """Interprets and executes Brainfuck code"""
    
    def __init__(self, tape_size=30000, cell_size=256):
        """
        Initialize interpreter with specified memory configuration
        
        Args:
            tape_size (int): Number of memory cells
            cell_size (int): Maximum value per cell (0 to cell_size-1)
        """
        self.tape_size = tape_size
        self.cell_size = cell_size
        self.reset()
    
    def reset(self):
        """Reset interpreter state to initial conditions"""
        self.tape = [0] * self.tape_size
        self.pointer = 0
        self.input_buffer = b""
        self.input_index = 0
        self.output_buffer = []
        self.code_pointer = 0
        self.loop_stack = []
    
    def load_code(self, code):
        """
        Load and sanitize Brainfuck code
        
        Args:
            code (str): Brainfuck code string
        """
        self.code = ''.join(c for c in code if c in '><+-.,[]')
        self.reset()
    
    def load_input(self, input_data):
        """
        Load input data for the ',' command
        
        Args:
            input_data (bytes): Input data as bytes
        """
        self.input_buffer = input_data
        self.input_index = 0
    
    def step(self):
        """
        Execute a single Brainfuck command
        
        Returns:
            bool: True if execution should continue, False if finished
        """
        if self.code_pointer >= len(self.code):
            return False
        
        command = self.code[self.code_pointer]
        
        if command == '>':
            self.pointer = (self.pointer + 1) % self.tape_size
            
        elif command == '<':
            self.pointer = (self.pointer - 1) % self.tape_size
            
        elif command == '+':
            self.tape[self.pointer] = (self.tape[self.pointer] + 1) % self.cell_size
            
        elif command == '-':
            self.tape[self.pointer] = (self.tape[self.pointer] - 1) % self.cell_size
            
        elif command == '.':
            self.output_buffer.append(self.tape[self.pointer])
            
        elif command == ',':
            if self.input_index < len(self.input_buffer):
                self.tape[self.pointer] = self.input_buffer[self.input_index]
                self.input_index += 1
            else:
                self.tape[self.pointer] = 0
            
        elif command == '[':
            if self.tape[self.pointer] == 0:
                depth = 1
                while depth > 0:
                    self.code_pointer += 1
                    if self.code_pointer >= len(self.code):
                        raise RuntimeError("Unmatched '[' in Brainfuck code")
                    if self.code[self.code_pointer] == '[':
                        depth += 1
                    elif self.code[self.code_pointer] == ']':
                        depth -= 1
            else:
                self.loop_stack.append(self.code_pointer)
                
        elif command == ']':
            if not self.loop_stack:
                raise RuntimeError("Unmatched ']' in Brainfuck code")
            
            if self.tape[self.pointer] != 0:
                self.code_pointer = self.loop_stack[-1]
            else:
                self.loop_stack.pop()
        
        self.code_pointer += 1
        return True
    
    def execute(self, code=None, input_data=b""):
        """
        Execute Brainfuck code to completion
        
        Args:
            code (str, optional): Brainfuck code to execute
            input_data (bytes, optional): Input data for program
            
        Returns:
            list: Output values from the program
        """
        if code is not None:
            self.load_code(code)
        
        if input_data:
            self.load_input(input_data)
        
        while self.step():
            pass
        
        return self.output_buffer
    
    def execute_file(self, filename, input_data=b""):
        """
        Execute Brainfuck code from a file
        
        Args:
            filename (str): Path to .bf file
            input_data (bytes, optional): Input data for program
            
        Returns:
            list: Output values from the program
        """
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        
        return self.execute(code, input_data)
    
    def get_tape_snapshot(self, start=0, end=10):
        """
        Get a snapshot of tape memory for debugging
        
        Args:
            start (int): Start index
            end (int): End index
            
        Returns:
            list: Tape values from start to end
        """
        return self.tape[start:end]
    
    def get_state(self):
        """
        Get current interpreter state for debugging
        
        Returns:
            dict: Current state information
        """
        return {
            'pointer': self.pointer,
            'current_cell': self.tape[self.pointer],
            'code_pointer': self.code_pointer,
            'loop_depth': len(self.loop_stack),
            'output_length': len(self.output_buffer),
            'input_remaining': len(self.input_buffer) - self.input_index
        }