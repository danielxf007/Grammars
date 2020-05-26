#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import Production as p
import re


# In[ ]:


class ProductionCreator:
    
    def __init__(self, string_separator, non_terminal_start, non_terminal_finish, arrow_tail, arrow_op):
        self.string_separator = string_separator
        self.non_terminal_start = non_terminal_start
        self.non_terminal_finish = non_terminal_finish
        self.arrow_tail = arrow_tail
        self.arrow_op = arrow_op
        
    def production_has_arrow_op(self, string):
        return re.search(self.arrow_op, string) != None
    
    def from_string_to_list(self, string):
        _list = []
        start = 0
        end = 0
        while end < len(string):
            if string[end] == self.string_separator:
                _list.append(string[start:end])
                end += 1
                while end < len(string) and string[end] == self.string_separator:
                    end +=1
                start = end
            else:
                end += 1
        if start < len(string):
            _list.append(string[start:])
        return _list
    
    def create_productions(self, string_list):
        productions = []
        for string in string_list:
            if not self.production_has_arrow_op(string):
                productions = []
                break
            left_side = string[0: string.index(self.arrow_tail)]
            right_side = []
            right_string = string[string.index(self.arrow_tail)+2:]
            index = 0
            while index < len(right_string):
                if right_string[index] != self.non_terminal_start:
                    right_side.append(right_string[index])
                else:
                    aux = index+1
                    while aux < len(right_string) and right_string[aux] != self.non_terminal_finish:
                        aux += 1
                    if aux < len(right_string):
                        right_side.append(right_string[index: aux +1])
                        index = aux
                    else:
                        right_side.append(right_string[index])
                index += 1
            production = p.Production(left_side, right_side)
            productions.append(production)
        return productions
    
    def get_non_terminals(self, productions):
        non_terminals = []
        for production in productions:
            if not production.left_side in non_terminals:
                non_terminals.append(production.left_side)
        return non_terminals


# In[ ]:


class ProductionValidator:
    
    def __init__(self, non_terminals, null_sequence_symbol, non_terminal_pattern, special_characters):
        self.non_terminals = non_terminals
        self.null_sequence_symbol = null_sequence_symbol
        self.non_terminal_pattern = non_terminal_pattern
        self.special_characters = special_characters

    def is_non_terminal(self, symbol):
        return symbol in self.non_terminals
    
    def is_terminal(self, symbol):
        return symbol != self.null_sequence_symbol and not self.is_non_terminal(symbol)
    
    def production_has_null_sequence_on_right_side(self, production):
        return production.right_side[0] == self.null_sequence_symbol
    

    def production_has_right_side_of_terminals(self, production):
        has_right_side_of_terminals = True
        for symbol in production.right_side:
            if not self.is_terminal(symbol):
                has_right_side_of_terminals = False
                break
        return has_right_side_of_terminals
    
    def production_has_non_infinite_cycle_non_terminals_on_right_side(self, non_infinite_cycle_non_terminals,
                                                                      production_right_side):
        has_non_infinite_cycle_non_terminals_on_right_side = False
        for non_terminal in non_infinite_cycle_non_terminals:
            if non_terminal in production_right_side:
                has_non_infinite_cycle_non_terminals_on_right_side = True
                break
        return has_non_infinite_cycle_non_terminals_on_right_side

    def production_has_suspected_non_terminals_on_right_side(self, suspected_non_terminals,
                                                                      production_right_side):
        has_suspected_non_terminals_on_right_side = False
        for non_terminal in suspected_non_terminals:
            if non_terminal in production_right_side:
                has_suspected_non_terminals_on_right_side = True
                break
        return has_suspected_non_terminals_on_right_side
    
    def safe_production(self, non_infinite_cycle_non_terminals, suspected_non_terminals, production):
        is_safe =  (self.production_has_right_side_of_terminals(production) or
                self.production_has_null_sequence_on_right_side(production))
        is_safe = is_safe or self.production_has_non_infinite_cycle_non_terminals_on_right_side(
            non_infinite_cycle_non_terminals, production.right_side)
        is_safe = is_safe and not self.production_has_suspected_non_terminals_on_right_side(suspected_non_terminals,
                                                                                           production.right_side)
        return is_safe
    
    def production_with_infinite_cycle(self, productions):
        infinite_cycle = False
        non_infinite_cycle_non_terminals = []
        suspected_non_terminals = self.non_terminals.copy()
        suspected_productions = productions.copy()
        production_infinite_cycle = None
        n_suspected_productions_before = len(suspected_productions)
        n_suspected_productions_after = len(suspected_productions)
        while suspected_productions:
            n_suspected_productions_before = len(suspected_productions)
            for production in suspected_productions:
                if self.safe_production(non_infinite_cycle_non_terminals, suspected_non_terminals, production):
                    if not production.left_side in non_infinite_cycle_non_terminals:
                        non_infinite_cycle_non_terminals.append(production.left_side)
                        suspected_non_terminals.remove(production.left_side)
                    suspected_productions.remove(production)
            n_suspected_productions_after = len(suspected_productions)
            if n_suspected_productions_before == n_suspected_productions_after:
                infinite_cycle = True
                break
        return infinite_cycle
    
    def non_terminal_is_well_written(self, non_terminal):
        return re.search(self.non_terminal_pattern, non_terminal) != None
    
    def right_side_is_well_written(self, right_side):
        if len(right_side) == 0:
            return False
        if self.null_sequence_symbol in right_side:
            return len(right_side) == 1
        well_written = True
        for symbol in right_side:
            if self.is_non_terminal(symbol):
                if not self.non_terminal_is_well_written(symbol):
                    well_written = False
                    break
            elif symbol in self.special_characters:
                well_written = False
                break
        return well_written
            
    
    def productions_are_well_written(self, productions):
        well_written = True
        if not productions:
            well_written = False
        for production in productions:
            if (not self.non_terminal_is_well_written(production.left_side) or
                not self.right_side_is_well_written(production.right_side)):
                well_written = False
                break
        return well_written

