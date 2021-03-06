#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import PDA11 as pda


# In[ ]:


class PDACreator:
    def __init__(self, end_of_sequence_symbol, null_sequence_symbol, empty_PDA_symbol, initial_non_terminal,
                 non_terminals, productions, stack_operations, selection_set):
        self.end_of_sequence_symbol = end_of_sequence_symbol
        self.null_sequence_symbol = null_sequence_symbol
        self.empty_PDA_symbol = empty_PDA_symbol
        self.initial_non_terminal = initial_non_terminal
        self.non_terminals = non_terminals
        self.productions = productions
        self.stack_operations = stack_operations
        self.selection_set = selection_set
        
    def is_non_terminal(self, symbol):
        return symbol in self.non_terminals
        
    def is_terminal(self, symbol):
        return symbol != self.null_sequence_symbol and not self.is_non_terminal(symbol)
    
    def production_has_null_sequence_on_right_side(self, production):
        return production.right_side[0] == self.null_sequence_symbol
    
    def get_productions_same_non_terminal_l_side(self, non_terminal):
        productions_same_l_side = []
        for production in self.productions:
            if production.left_side == non_terminal:
                productions_same_l_side.append(production)
        return productions_same_l_side
    
    def get_productions_number_same_non_terminal_l_side(self, productions_same_l_side):
        productions_number_same_l_side = []
        for production in productions_same_l_side:
            productions_number_same_l_side.append(self.productions.index(production))
        return productions_number_same_l_side
    
    def get_productions_start_with_terminal(self, terminal, productions):
        productions_start_with_terminal = []
        for production in productions:
            if production.right_side[0] == terminal:
                productions_start_with_terminal.append(production)
        return productions_start_with_terminal
    
    def get_terminals_on_right_side(self, right_side):
        terminals = set()
        for symbol in right_side:
            if self.is_terminal(symbol):
                terminals.add(symbol)
        return terminals
    
    def get_productions_with_numbers(self, numbers):
        productions_with_numbers = []
        for number in numbers:
            productions_with_numbers.append(self.productions[number])
        return productions_with_numbers
    
    def production_starts_with_terminal(self, production):
        return self.is_terminal(production.right_side[0])
    
    def is_s_grammar(self):
        s_grammar = (0, None)
        for non_terminal in self.non_terminals:
            terminals = []
            productions_same_non_terminal_l_side = self.get_productions_same_non_terminal_l_side(non_terminal)
            for production in productions_same_non_terminal_l_side:
                if self.production_starts_with_terminal(production):
                    if not production.right_side[0] in terminals:
                        terminals.append(production.right_side[0])
                    else:
                        s_grammar = (1, self.get_productions_start_with_terminal(production.right_side[0],
                                                                                 productions_same_non_terminal_l_side))
                        # productions with same left side start with the the same terminal
                        break
                else:
                    if self.is_non_terminal(production.right_side[0]):
                        s_grammar = (2, production) # production starts with non_terminal
                        break
                    else:
                        s_grammar = (3, production) # production is nullable
                    break
        return s_grammar
    
    def selection_sets_are_disjoint(self, production_numbers):
        disjoint = True
        current_set = self.selection_set[production_numbers[0]]
        index = 1
        while(index < len(production_numbers)):
            current_set = current_set.intersection(self.selection_set[production_numbers[index]])
            if current_set != set():
                disjoint = False
                break
            index += 1
        return disjoint
    
    def get_selection_sets_not_disjoint(self, production_numbers):
        sets = set()
        for number in production_numbers:
            index = production_numbers.index(number)+1
            while(index < len(production_numbers)):
                current_set = self.selection_set[number]
                current_set = current_set.intersection(self.selection_set[production_numbers[index]])
                if current_set != set():
                    sets.add(number)
                    sets.add(production_numbers[index])
                index +=1
        return list(sets)
    
    def get_selection_sets_with_numbers(self, numbers):
        sets = []
        for number in numbers:
            sets.append(self.selection_set[number])
        return sets
    
    def is_q_grammar(self):
        q_grammar = (0, None)
        for non_terminal in self.non_terminals:
            terminals = []
            productions_same_non_terminal_l_side = self.get_productions_same_non_terminal_l_side(non_terminal)
            productions_number_same_l_side = self.get_productions_number_same_non_terminal_l_side(
            productions_same_non_terminal_l_side)
            if not self.selection_sets_are_disjoint(productions_number_same_l_side):
                numbers = self.get_selection_sets_not_disjoint(productions_number_same_l_side)
                productions_with_numbers = self.get_productions_with_numbers(numbers)
                selection_sets_with_numbers = self.get_selection_sets_with_numbers(numbers)
                q_grammar = (4, list(zip(productions_with_numbers, selection_sets_with_numbers))) # selection_sets are joint
                break
            for production in productions_same_non_terminal_l_side:
                if self.production_starts_with_terminal(production):
                    if not production.right_side[0] in terminals:
                        terminals.append(production.right_side[0])
                    else:
                        q_grammar = (1, self.get_productions_start_with_terminal(production.right_side[0],
                                                                                 productions_same_non_terminal_l_side))
                        break
                else:
                    if self.is_non_terminal(production.right_side[0]):
                        q_grammar = (2, production) # production starts with non_terminal
                        break
        return q_grammar
    
    def is_ll_grammar(self):
        ll_grammar = (0, None)
        for non_terminal in self.non_terminals:
            productions_same_non_terminal_l_side = self.get_productions_same_non_terminal_l_side(non_terminal)
            productions_number_same_l_side = self.get_productions_number_same_non_terminal_l_side(
            productions_same_non_terminal_l_side)
            if not self.selection_sets_are_disjoint(productions_number_same_l_side):
                numbers = self.get_selection_sets_not_disjoint(productions_number_same_l_side)
                productions_with_numbers = self.get_productions_with_numbers(numbers)
                selection_sets_with_numbers = self.get_selection_sets_with_numbers(numbers)
                ll_grammar = (4, list(zip(productions_with_numbers, selection_sets_with_numbers)))
                break
        return ll_grammar
    
    def get_terminals(self):
        terminals = []
        for production in self.productions:
            for symbol in production.right_side:
                if self.is_terminal(symbol) and not symbol in terminals:
                    terminals.append(symbol)
        return terminals
                    
    def get_input_symbols_PDA(self, terminals):
        input_symbols = terminals.copy()
        input_symbols.append(self.end_of_sequence_symbol)
        return input_symbols
    
    def get_initial_configuration_PDA(self):
        return [self.empty_PDA_symbol, self.initial_non_terminal]
    
    def production_terminal_alpha(self, production_same_l_side, input_symbol):
        terminal_alpha = None
        for production in production_same_l_side:
            if production.right_side[0] == input_symbol:
                terminal_alpha = production
        return terminal_alpha
    
    def get_transition_production_terminal_alpha(self, production, name):
        transition = None
        if len(production.right_side) >= 2:
            right_side = production.right_side[1:]
            right_side.reverse()
            transition = pda.Transition(name, self.stack_operations.replace_generator(right_side), True)
        else:
            transition = pda.Transition(name, self.stack_operations.pop_generator(), True)
        return transition
                
    def production_null_sequence_x_in_selection_p(self, production_numbers, symbol):
        x_in_selection_p = False
        for number in production_numbers:
            if symbol in list(self.selection_set[number]):
                x_in_selection_p = True
                break
        return x_in_selection_p
    
    def get_productions_type_beta(self, productions_same_l_side):
        productions_type_beta = []
        for production in productions_same_l_side:
            if self.is_non_terminal(production.right_side[0]):
                productions_type_beta.append(production)
        return productions_type_beta
        
    def get_transition_table_s_grammar(self, symbols_in_PDA, input_symbols_PDA):
        table = []
        n = 0
        for symbol in symbols_in_PDA:
            transitions = []
            for input_symbol in input_symbols_PDA:
                if self.is_non_terminal(symbol):
                    productions_same_l_side = self.get_productions_same_non_terminal_l_side(symbol)
                    production = self.production_terminal_alpha(productions_same_l_side, input_symbol)
                    if production:
                        transitions.append(self.get_transition_production_terminal_alpha(production, '#' + str(n)))
                        n+=1
                        continue
                elif self.is_terminal(symbol) and symbol == input_symbol:
                    transition = pda.Transition('#' + str(n), self.stack_operations.pop_generator(), True)
                    transitions.append(transition)
                    n += 1
                    continue
                elif symbol == self.empty_PDA_symbol and input_symbol == self.end_of_sequence_symbol:
                    transition = pda.Transition('A', None, None)
                    transitions.append(transition)
                    continue
                transition = pda.Transition('R', None, None)
                transitions.append(transition)
            table.append(transitions)
        return pda.TransitionTable(symbols_in_PDA, input_symbols_PDA, table)
    
    def production_null_sequence(self, productions):
        prod = None
        for production in productions:
            if self.production_has_null_sequence_on_right_side(production):
                prod = production
                break
        return prod
    
    def input_symbol_in_selection_set_of_production(self, input_symbol, production):
        return input_symbol in list(self.selection_set[self.productions.index(production)])

    def get_transition_table_q_grammar(self, symbols_in_PDA, input_symbols_PDA):
        table = []
        n = 0
        for symbol in symbols_in_PDA:
            transitions = []
            for input_symbol in input_symbols_PDA:
                if self.is_non_terminal(symbol):
                    productions_same_l_side = self.get_productions_same_non_terminal_l_side(symbol)
                    production = self.production_terminal_alpha(productions_same_l_side, input_symbol)
                    if production:
                        transitions.append(self.get_transition_production_terminal_alpha(production, '#' + str(n)))
                        n+=1
                        continue
                    production = self.production_null_sequence(productions_same_l_side)
                    if production and self.input_symbol_in_selection_set_of_production(input_symbol, production):
                        transition = pda.Transition('#' + str(n), self.stack_operations.pop_generator(), False)
                        transitions.append(transition)
                        n += 1
                        continue
                elif self.is_terminal(symbol) and symbol == input_symbol:
                    transition = pda.Transition('#' + str(n), self.stack_operations.pop_generator(), True)
                    transitions.append(transition)
                    n += 1
                    continue
                elif symbol == self.empty_PDA_symbol and input_symbol == self.end_of_sequence_symbol:
                    transition = pda.Transition('A', None, None)
                    transitions.append(transition)
                    continue
                transition = pda.Transition('R', None, None)
                transitions.append(transition)
            table.append(transitions)
        return pda.TransitionTable(symbols_in_PDA, input_symbols_PDA, table)
    
    def input_symbol_in_selection_set_of_production_type_beta(self,  input_symbol, productions_type_beta):
        production = None
        for production_beta in productions_type_beta:
            if self.input_symbol_in_selection_set_of_production(input_symbol, production_beta):
                production = production_beta
                break
        return production

    def get_transition_table_ll_grammar(self, symbols_in_PDA, input_symbols_PDA):
        table = []
        n = 0
        for symbol in symbols_in_PDA:
            transitions = []
            for input_symbol in input_symbols_PDA:
                if self.is_non_terminal(symbol):
                    productions_same_l_side = self.get_productions_same_non_terminal_l_side(symbol)
                    production = self.production_terminal_alpha(productions_same_l_side, input_symbol)
                    if production:
                        transitions.append(self.get_transition_production_terminal_alpha(production, '#' + str(n)))
                        n+=1
                        continue
                    productions_type_beta = self.get_productions_type_beta(productions_same_l_side)
                    production = self.input_symbol_in_selection_set_of_production_type_beta(input_symbol, productions_type_beta)
                    if productions_type_beta and production:
                        beta = production.right_side.copy()
                        beta.reverse()
                        transition = pda.Transition('#' + str(n), self.stack_operations.replace_generator(beta), False)
                        transitions.append(transition)
                        n += 1
                        continue
                    production = self.production_null_sequence(productions_same_l_side)
                    if production and self.input_symbol_in_selection_set_of_production(input_symbol, production):
                        transition = pda.Transition('#' + str(n), self.stack_operations.pop_generator(), False)
                        transitions.append(transition)
                        n += 1
                        continue
                elif self.is_terminal(symbol) and symbol == input_symbol:
                    transition = pda.Transition('#' + str(n), self.stack_operations.pop_generator(), True)
                    transitions.append(transition)
                    n += 1
                    continue
                elif symbol == self.empty_PDA_symbol and input_symbol == self.end_of_sequence_symbol:
                    transition = pda.Transition('A', None, None)
                    transitions.append(transition)
                    continue
                transition = pda.Transition('R', None, None)
                transitions.append(transition)
            table.append(transitions)
        return pda.TransitionTable(symbols_in_PDA, input_symbols_PDA, table)
    
    def is_production_terminal_alpha(self, production):
        return self.is_terminal(production.right_side[0])
    
    def is_production_beta(self, production):
        return self.is_non_terminal(production.right_side[0])
    
    def get_symbols_in_PDA_for_s_or_q(self, terminals):
        symbols_in_PDA = set(self.non_terminals)
        for terminal in terminals:
            for production in self.productions:
                if self.is_production_terminal_alpha(production) and len(production.right_side) >= 2:
                    if terminal in production.right_side[1:]:
                        symbols_in_PDA.add(terminal)
        symbols_in_PDA.add(self.empty_PDA_symbol)
        return list(symbols_in_PDA)
    
    def get_symbols_in_PDA_for_ll(self, terminals):
        symbols_in_PDA = set(self.non_terminals)
        for terminal in terminals:
            for production in self.productions:
                if self.is_production_terminal_alpha(production) and len(production.right_side) >= 2:
                    if terminal in production.right_side[1:]:
                        symbols_in_PDA.add(terminal)
                elif self.is_production_beta(production) and terminal in production.right_side:
                    symbols_in_PDA.add(terminal)
        symbols_in_PDA.add(self.empty_PDA_symbol)
        return list(symbols_in_PDA)
    
    def create_PDA(self):
        push_down_automata = None
        result = []
        terminals = self.get_terminals()
        input_symbols = self.get_input_symbols_PDA(terminals)
        initial_configuration = self.get_initial_configuration_PDA()
        s_grammar = self.is_s_grammar()
        q_grammar = self.is_q_grammar()
        ll_grammar = self.is_ll_grammar()
        
        if s_grammar[0] == 0:
            symbols_in_PDA = self.get_symbols_in_PDA_for_s_or_q(terminals)
            transition_table = self.get_transition_table_s_grammar(symbols_in_PDA, input_symbols)
            push_down_automata = pda.PushDownAutomaton(input_symbols, self.end_of_sequence_symbol, 'A', 'R',
                                                      initial_configuration, transition_table)
            result.append(('It is S grammar', push_down_automata, 0))
        elif s_grammar[0] == 1:
            result.append(('It is not S grammar, same non terminal starts with same terminal: ', s_grammar[1], 1))
        elif s_grammar[0] == 2:
            result.append(('It is not S grammar, production starts with a non terminal: ', s_grammar[1], 2))
        elif s_grammar[0] == 3:
            result.append(('It is not S grammar, production is nullable: ', s_grammar[1], 3))
            
        if q_grammar[0] == 0:
            symbols_in_PDA = self.get_symbols_in_PDA_for_s_or_q(terminals)
            transition_table = self.get_transition_table_q_grammar(symbols_in_PDA, input_symbols)
            if not push_down_automata:
                push_down_automata = pda.PushDownAutomaton(input_symbols, self.end_of_sequence_symbol, 'A', 'R',
                                                           initial_configuration, transition_table)
                result.append(('It is Q grammar', push_down_automata, 0))
            else:
                result.append(('It is Q grammar', None, 0))
        elif q_grammar[0] == 1:
            result.append(('It is not Q grammar, same non terminal starts with same terminal: ', q_grammar[1], 1))
        elif q_grammar[0] == 2:
            result.append(('It is not Q grammar, production starts with a non terminal: ', q_grammar[1], 2))
        elif q_grammar[0] == 4:
            result.append(('It is not Q grammar, selection sets of these productions are not disjoint: ', q_grammar[1], 4))

        if ll_grammar[0] == 0:
            symbols_in_PDA = self.get_symbols_in_PDA_for_ll(terminals)
            transition_table = self.get_transition_table_ll_grammar(symbols_in_PDA, input_symbols)
            if not push_down_automata:
                push_down_automata = pda.PushDownAutomaton(input_symbols, self.end_of_sequence_symbol, 'A', 'R',
                                                           initial_configuration, transition_table)
                result.append(('It is LL grammar', push_down_automata, 0))
            else:
                result.append(('It is LL grammar', None, 0))
            
        elif ll_grammar[0] == 4:
            result.append(('It is not LL grammar, selection sets of these productions are not disjoint: ', ll_grammar[1], 4))
        
        return result

