#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class StackOperation:
    
    def push_generator(self, element):
        return (lambda stack:
                stack + element)
    
    def replace_generator(self, elements):
        return (lambda stack:
               stack[0: len(stack)-1] + elements)
    
    def pop_generator(self):
        return (lambda stack:
               stack[0: len(stack)-1])


# In[ ]:


class Transition:
    def __init__(self, name, stack_operation, advance):
        self.name = name
        self.stack_operation = stack_operation
        self.advance = advance
    
    def has_stack_operation(self):
        return self.stack_operation != None


# In[ ]:


class TransitionTable:
    
    def __init__(self, encoded_rows, encoded_columns, function_table):
        self.encoded_rows = encoded_rows
        self.encoded_columns = encoded_columns
        self.table = function_table
        
    def get_transition_row(self, row_symbol):
        transition_row = []
        for i in range(0, len(self.encoded_rows)):
            if self.encoded_rows[i] == row_symbol:
                transition_row = self.table[i]
                break
        return transition_row
    
    def get_transition(self, row_symbol, column_symbol):
        transition = None
        transition_row = self.get_transition_row(row_symbol)
        for j in range(0, len(self.encoded_columns)):
            if self.encoded_columns[j] == column_symbol:
                transition = transition_row[j]
                break
        return transition
        
    def insert_row(self, row):
        self.table.append(row)


# In[ ]:


class PushDownAutomaton:
    
    def __init__(self, symbols, end_sequence_symbol, acceptance_transition_name,
                 reject_transition_name, init_config, transition_table):
        self.symbols = symbols
        self.end_sequence_symbol = end_sequence_symbol
        self.acceptance_transition_name = acceptance_transition_name
        self.reject_transition_name = reject_transition_name
        self.transition_table = transition_table
        self.init_config = init_config
        self.stack = None
    
    def belongs_to_language(self, symbol_arr):
        if not self.symbols_in_language(symbol_arr):
            return False
        iterator = iter(symbol_arr)
        belongs = False
        input_symbol = next(iterator)
        self.stack = self.init_config.copy()
        while True:
            try:
                top_symbol = self.get_top_symbol()
                transition = self.transition_table.get_transition(top_symbol, input_symbol)
                if self.is_reject_transition(transition):
                    break
                if self.end_of_sequence(input_symbol) and self.is_acceptance_transition(transition):
                    belongs = True
                    break
                if transition.has_stack_operation():
                    self.stack = transition.stack_operation(self.stack)
                if transition.advance:
                    input_symbol = next(iterator)
            except StopIteration:
                break
        return belongs
    
    def symbol_in_language(self, symbol):
        return symbol in self.symbols
    
    def symbols_in_language(self, symbol_arr):
        in_language = True
        for symbol in symbol_arr:
            if not self.symbol_in_language(symbol):
                in_language = False
                break
        return in_language
            
    def get_top_symbol(self):
        return self.stack[len(self.stack)-1]
                
    def end_of_sequence(self, symbol):
        return self.end_sequence_symbol == symbol
    
    def is_acceptance_transition(self, transition):
        return transition.name == self.acceptance_transition_name
    
    def is_reject_transition(self, transition):
        return transition.name == self.reject_transition_name

