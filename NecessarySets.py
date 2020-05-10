#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Production:
    def __init__(self, left_side, right_side):
        self.left_side = left_side #Non terminal of the form <str>
        self.right_side = right_side #Array of terminals and non terminals, empty sequence 
    
    def get_left_side(self):
        return self.left_side
    
    def get_right_side(self):
        return self.right_side


# In[2]:


class ProductionSet:
    def __init__(self, initial_non_terminal, null_sequence_symbol, end_of_sequence_symbol, production_arr, non_terminal_arr):
        self.initial_non_terminal = initial_non_terminal
        self.null_sequence_symbol = null_sequence_symbol
        self.end_of_sequence_symbol = end_of_sequence_symbol
        self.production_arr = production_arr
        self.non_terminal_arr = non_terminal_arr

    def is_non_terminal(self, symbol):
        return symbol in self.non_terminal_arr
        
    def is_terminal(self, symbol):
        return symbol != self.null_sequence_symbol and not self.is_non_terminal(symbol)
    
    def get_non_terminals(self):
        return self.non_terminal_arr
    
    def only_right_side_of_non_terminals(self, production):
        only_non_terminals = True
        for symbol in production.right_side:
            if not self.is_non_terminal(symbol):
                only_non_terminals = False
                break
        return only_non_terminals
    
    def production_has_null_sequence_on_right_side(self, production):
        return production.right_side[0] == self.null_sequence_symbol
    
    def get_non_terminal_set_from_productions(self, productions):
        non_terminals = set()
        for production in productions:
            if not production.left_side in non_terminals:
                non_terminals.add(production.left_side)
        return non_terminals
    
    def non_terminals_can_not_be_nullable(self, non_terminals, no_nullable_non_terminals):
        nullable = True
        for non_terminal in non_terminals:
            if non_terminals in  no_nullable_non_terminals:
                nullable = False
                break
        return nullable
    
    def non_terminal_in_productions_left_side(self, non_terminal, productions):
        in_productions = False
        for production in productions:
            if production.left_side == non_terminal:
                in_productions = True
                break
        return in_productions
    
    def get_nullables_base_case(self):
        nullables = set()
        for production in self.production_arr:
            if self.production_has_null_sequence_on_right_side(production):
                nullables.add(production.left_side)
        return nullables
    
    def get_suspected_productions(self, nullable_non_terminals, no_nullable_non_terminals):
        suspected_productions = []
        for production in self.production_arr:
            if (self.only_right_side_of_non_terminals(production) and not production.left_side in nullable_non_terminals and
                not production.left_side in no_nullable_non_terminals):
                suspected_productions.append(production)
        return suspected_productions
    
    def get_suspected_non_terminals(self, suspected_productions):
        suspected_non_terminals = set()
        for non_terminal in self.non_terminal_arr:
            for production in suspected_productions:
                if production.left_side == non_terminal:
                    suspected_non_terminals.add(non_terminal)
                    break
        return suspected_non_terminals
    
    def get_no_nullable_non_terminals(self, nullable_non_terminals, suspected_non_terminals):
        no_nullable_non_terminals = set()
        for non_terminal in self.non_terminal_arr:
            if not non_terminal in nullable_non_terminals and not non_terminal in suspected_non_terminals:
                no_nullable_non_terminals.add(non_terminal)
        return no_nullable_non_terminals
    
    def get_nullable_non_terminals(self):
        nullable_non_terminals = self.get_nullables_base_case()
        suspected_p = self.get_suspected_productions(nullable_non_terminals, set())
        suspected_non_terminals = self.get_suspected_non_terminals(suspected_p)
        no_nullable_non_terminals = self.get_no_nullable_non_terminals(nullable_non_terminals, suspected_non_terminals)
        while suspected_non_terminals:
            for production in suspected_p:
                all_nullables = True
                for symbol in production.right_side:
                    if symbol in no_nullable_non_terminals:
                        no_nullable_non_terminals.add(production.left_side)
                        all_nullables = False
                        break
                    if symbol in suspected_non_terminals:
                        all_nullables = False
                        break
                if all_nullables:
                    nullable_non_terminals.add(production.left_side)
            suspected_p = self.get_suspected_productions(nullable_non_terminals, no_nullable_non_terminals)
            suspected_non_terminals = self.get_suspected_non_terminals(suspected_p)                         
        return nullable_non_terminals
    
    def right_side_is_nullable(self, right_side, nullable_non_terminals):
        nullable = True
        if right_side[0] == self.null_sequence_symbol:
            return nullable
        for symbol in right_side:
            if not symbol in nullable_non_terminals:
                nullable = False
                break
        return nullable
            
    def get_nullable_productions(self, nullable_non_terminals):
        production_indexes = []
        for index in range(0, len(self.production_arr)):
            if self.right_side_is_nullable(self.production_arr[index].right_side, nullable_non_terminals):
                production_indexes.append(index)
        return production_indexes
    
    def get_productions_same_non_terminal_l_side(self, non_terminal):
        productions = []
        for production in self.production_arr:
            if production.left_side == non_terminal and not production in productions:
                productions.append(production)
        return productions
    
    def get_firsts_base_cases(self, nullable_non_terminals):
        base_cases = []
        for symbol in self.non_terminal_arr:
            productions = self.get_productions_same_non_terminal_l_side(symbol)
            firsts = set()
            for production in productions:
                if self.is_non_terminal(production.right_side[0]):
                    for element in production.right_side:
                        if element in nullable_non_terminals:
                                firsts.add(element)
                        else:
                            firsts.add(element)
                            break
                elif self.is_terminal(production.right_side[0]):
                    firsts.add(production.right_side[0])
            base_cases.append([symbol, firsts])
        return base_cases
    
    def all_non_terminals_replaced(self, base_cases):
        all_replaced = True
        for case in base_cases:
            for symbol in case[1]:
                if self.is_non_terminal(symbol):
                    all_replaced = False
                    break
        return all_replaced
    
    def get_set_of_firsts_for_productions(self, nullable_non_terminals, set_of_firsts_for_non_terminals):
        set_of_firsts = []
        for index in range(0, len(self.production_arr)):
            firsts = set()
            for symbol in self.production_arr[index].right_side:
                if self.is_terminal(symbol):
                    firsts.add(symbol)
                    break
                if symbol == self.null_sequence_symbol:
                    break
                if symbol in nullable_non_terminals:
                    firsts = firsts.union(self.get_terminals_from_set(symbol, set_of_firsts_for_non_terminals))
                else:
                    firsts = firsts.union(self.get_terminals_from_set(symbol, set_of_firsts_for_non_terminals))
                    break
            set_of_firsts.append(firsts)
        return set_of_firsts
    
    def get_productions_with_non_terminal_on_r_side(self, non_terminal):
        productions = []
        for production in self.production_arr:
            if non_terminal in production.right_side:
                productions.append(production)
        return productions
    
    def get_terminals_from_set(self, non_terminal, set_of_terminals):
        for case in set_of_terminals:
            if case[0] == non_terminal:
                return case[1]
        
    def get_nexts_base_cases(self, nullable_non_terminals, set_of_firsts_for_non_terminals):
        base_cases = []
        for non_terminal in self.non_terminal_arr:
            nexts = set()
            if non_terminal == self.initial_non_terminal:
                nexts.add(self.end_of_sequence_symbol)
            for production in self.get_productions_with_non_terminal_on_r_side(non_terminal):
                indexes_non_terminal = list(filter(lambda i: production.right_side[i] == non_terminal,
                                                   list(range(0, len(production.right_side)))))
                for index in indexes_non_terminal:
                    next_index = index+1
                    while next_index < len(production.right_side):
                        if self.is_non_terminal(production.right_side[next_index]):
                            if production.right_side[next_index] in nullable_non_terminals:
                                nexts = nexts.union(self.get_terminals_from_set(production.right_side[next_index],
                                                                      set_of_firsts_for_non_terminals))
                                if next_index == len(production.right_side)-1:
                                    nexts.add(production.left_side)
                            else:
                                nexts = nexts.union(self.get_terminals_from_set(production.right_side[next_index],
                                                                      set_of_firsts_for_non_terminals))
                                break
                        else:
                            nexts.add(production.right_side[next_index])
                            break
                        next_index += 1
                    if index == len(production.right_side)-1:
                        nexts.add(production.left_side)
            nexts.discard(non_terminal)
            base_cases.append([non_terminal, nexts])
                
        return base_cases
    
    def replace_non_terminals(self, base_cases):
        while True:
            for case in base_cases:
                non_terminals_to_replace = list(filter(lambda x: self.is_non_terminal(x), case[1]))
                replacements = list(filter(lambda x: x[0] in non_terminals_to_replace, base_cases))
                for non_terminal in non_terminals_to_replace:
                    case[1].discard(non_terminal)
                    case[1] = case[1].union(replacements.pop()[1])
            if self.all_non_terminals_replaced(base_cases):
                break
        return base_cases
    
    def get_set_of_selection_for_productions(self, nullable_productions, set_of_firsts_productions, set_of_nexts):
        selection_set = []
        for index in range(0, len(self.production_arr)):
            if index in nullable_productions:
                selection_set.append(set_of_firsts_productions[index].union(self.get_terminals_from_set(
                    self.production_arr[index].left_side, set_of_nexts)))
            else:
                selection_set.append(set_of_firsts_productions[index])
        return selection_set

