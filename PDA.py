#!/usr/bin/env python
# coding: utf-8

# In[1]:


class StateOperation:
    def __init__(self, encoded_columns, function_table):
        self.encoded_columns = encoded_columns
        self.table = function_table
    
    def state_function(self, column_symbol):
        next_state = None
        for j in range(0, len(self.encoded_columns)):
            if self.encoded_columns[j] == column_symbol:
                next_state = self.table[j]
                break
        return next_state


# In[2]:


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


# In[3]:


class Transition:
    def __init__(self, name, stack_operation, state_operation, advance_input_operation):
        self.name = name
        self.stack_operation = stack_operation
        self.state_operation= state_operation
        self.advance_input_operation = advance_input_operation
    
    def has_stack_operation(self):
        return self.stack_operation != None
    
    def has_state_operation(self):
        return self.state_operation != None
    
    def has_input_operation(self):
        return self.advance_input_operation != None


# In[4]:


class TransitionTable:
    
    def __init__(self, encoded_rows, encoded_columns, name, function_table):
        self.encoded_rows = encoded_rows
        self.encoded_columns = encoded_columns
        self.name = name
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
    
    def print_table(self):
        for row_symbol in self.encoded_rows:
            row = self.get_transition_row(row_symbol)
            row_names = ''
            for transition in row:
                row_names += (transition.name +' ')
            print(row_symbol + '( ' + row_names + ')')


# In[5]:


class PushDownAutomaton:
    
    def __init__(self, symbols, end_sequence_symbol, acceptance_transition_name,
                 reject_transition_name, states, initial_state, init_config, transition_table_set):
        self.symbols = symbols
        self.end_sequence_symbol = end_sequence_symbol
        self.acceptance_transition_name = acceptance_transition_name
        self.reject_transition_name = reject_transition_name
        self.states = states
        self.initial_state= initial_state
        self.transition_table_set = transition_table_set
        self.stack = init_config
    
    def belongs_to_language(self, symbol_arr):
        is_well_written = self.is_well_written(symbol_arr)
        iterator = iter(symbol_arr)
        current_state = self.initial_state
        transition_table = self.get_transition_table(current_state)
        belongs = False
        input_symbol = next(iterator)
        while is_well_written:
            try:
                top_symbol = self.get_top_symbol()
                transition = transition_table.get_transition(top_symbol, input_symbol)
                if self.is_reject_transition(transition):
                    break
                if self.end_of_sequence(input_symbol) and self.is_acceptance_transition(transition):
                    belongs = True
                    break
                if transition.has_stack_operation():
                    self.stack = transition.stack_operation(self.stack)
                if transition.has_state_operation():
                    current_state = transition.state_operation.state_function(current_state)
                if transition.has_input_operation():
                    if transition.advance_input_operation:
                        input_symbol = next(iterator)
            except StopIteration:
                break
        return belongs
    
    def symbol_in_language(self, symbol):
        return symbol in self.symbols
    
    def is_well_written(self, symbol_arr):
        well_written = False
        for index in range(0, len(symbol_arr)):
            if self.end_of_sequence(symbol_arr[index]):
                well_written = (index == len(symbol_arr)-1)
                break
            elif not self.symbol_in_language:
                break
        return well_written
                
            
    def get_top_symbol(self):
        return self.stack[len(self.stack)-1]
    
    def get_transition_table(self, state):
        transition_table = None
        for element in self.transition_table_set:
            if element.name == state:
                transition_table = element
                break
        return transition_table
                
    def end_of_sequence(self, symbol):
        return self.end_sequence_symbol == symbol
    
    def is_acceptance_transition(self, transition):
        return transition.name == self.acceptance_transition_name
    
    def is_reject_transition(self, transition):
        return transition.name == self.reject_transition_name

