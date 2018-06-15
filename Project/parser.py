# -----------------------------------------------------------------
# :: Author :: Burak Tekin
# :: Lecture :: Parsing - SuSe 2018, University of Stuttgart
# :: Parsing ::
#
# ::Design Recipe::
# PURPOSE: Generating parsing tree for the given sentence by applying 
# the rules defined in given grammar.
#
# ::Contract::
# parser( list_of_rules::List, sentence::String ) --> parse_tree::String
# -----------------------------------------------------------------

import sys, os
import numpy as np
import itertools

class Parser:
    # -----------------------------------------------------------------
    # create dictionaries to hold the rules to make it easier to reach
    # them, while the production is on going.
    # -----------------------------------------------------------------
    def __init__(self):
        self.rules = {}
        # derivations: all productions as a key, value pairs
        self.derivations = {} 
        # List of terminals
        self.terminals = []
        # List of non-terminals
        self.non_terminals = []
        # list of epsilons
        self.epsilons = {}
        # list of unit_productions 
        self.unit_productions = []
        # list of yZ || Yz type 
        self.mixed_type = []
        # Load Grammar from text file...
        self.load_grammar("./grammar.cfg")
        # Constants
        self.EPSILON = "ε"
        self.start_symbol = list(self.derivations.keys())[0]
        self.converter(self.derivations)


    # -----------------------------------------------------------------
    # Split terminals and non-terminals
    # -----------------------------------------------------------------
    def find_terminals(self, rhs, non_terminals):
        temp_array = list()
        for symbols in rhs:
            for symbol in symbols:
                for s in symbol:
                    if( s not in non_terminals 
                    and s not in temp_array ):
                        temp_array.append( s )
        return temp_array


    # -----------------------------------------------------------------
    # Get LHS and RHS of the rule
    # -----------------------------------------------------------------
    def lhs_rhs(self, rule):
        rule_string = rule.strip().split("->")
        lhs = rule_string[0].strip()
        rhs = [ r.split() for r in rule_string[1].strip().split(" | ") ]
        self.derivations[lhs] = rhs
        return rule_string


    # -----------------------------------------------------------------
    # Load grammar from a file
    # -----------------------------------------------------------------
    def load_grammar(self, filename):
        with open(filename) as grammar:
            unit_rules = grammar.readlines()
        list_of_rules = list(map(self.lhs_rhs, unit_rules))
        print(list_of_rules)
        rhs = list(self.derivations.values())
        self.non_terminals = list(set(self.derivations.keys()))
        self.terminals = self.find_terminals(rhs, self.non_terminals)
        print("Terminals: ", self.terminals)
        print("Non terminals: ", self.non_terminals)
        return list_of_rules


    # -----------------------------------------------------------------
    # Detect whether the given grammar is in CNF form or not?
    # Every rule in the grammar has to be in the form of:
    #
    # I) (non-terminal) -> (non-terminal)(non-terminal) | not(ε) 
    #                  ~ OR ~
    # II) (non−terminal) -> (non−terminal)(non−terminal)
    #                  ~ OR ~
    # III) (non−terminal) -> (terminal)
    # -----------------------------------------------------------------
    def find_lhs(self, grammar, term):
        lhs_list = list()
        for value in list(grammar.items()):
            for symbol in value[1]:
                if( term in symbol ):
                    lhs_list.append(value[0])
        return lhs_list


    def new_productions(self, prev, new):
        flatten = [item for sublist in new for item in sublist if item != self.EPSILON]
        production = [[p, n] for p in prev for n in flatten ]
        return production

    
    def is_start_symbol_in_rhs(self, grammar):
        for value in list(grammar.items()):
            for symbol in value[1]:
                if( self.start_symbol in symbol ):
                    return True
                else:
                    return False

    def is_epsilon_exist(self, grammar):
        # TODO: REFACTOR this part
        temp_epsilons = list()
        addition = list()
        items = grammar.items()
        for rule in grammar:
            for symbol in grammar[rule]:
                if( self.EPSILON in symbol ):
                    addition = grammar[rule][:]
                    grammar[rule].remove(symbol)
                    """
                    l = self.find_lhs(grammar, rule).pop()
                    temp = list()
                    grammar[l].append([self.EPSILON])
                    rule_container = list()
                    for symbols in grammar[l]:
                        temp.append(symbols)
                        if(rule in symbols):
                            rule_container.append(rule)
                            temp.append(symbols)
                            #symbols.remove(rule)
                    grammar[l] = temp

                    #self.epsilons[rule] = grammar[rule]
                    #if(rule not in temp_epsilons):
                    #    temp_epsilons.append(rule)"""
        """ for check_symbol in temp_epsilons:
            for rule in items:
                for r in rule[1]:
                    r_new = r[:]
                    index = grammar[rule[0]].index(r)
                    if( check_symbol in r_new ):
                        #print(rule, " ---> ", index)
                        r_new.remove(check_symbol)
                        if(r_new):
                            production = self.new_productions(r_new, addition)
                            for i in production:
                                if(check_symbol in i):
                                    i.remove(check_symbol)
                                    production = self.new_productions(i, addition)
                            r_new = [r_new] + production
                        else:
                            grammar[rule[0]].append([self.EPSILON])
                            r_new += grammar[check_symbol]
                        grammar[rule[0]] += r_new
                        del grammar[rule[0]][index] """


    def is_unit_production_exist(self, grammar):
        lhs = list()
        rhs = list()
        for rule in list(grammar.items()):
            for i, symbol in enumerate(rule[1]):
                if( len(symbol) == 1 ):
                    if(symbol[0] in self.non_terminals):
                        if(rule[0] not in lhs):
                            lhs.append(rule[0])
                        if(symbol[0] not in rhs):
                            rhs.append(symbol[0])

        for left in lhs:
            for right in rhs:
                if [right] in grammar[left]:
                    index = grammar[left].index([right])
                    grammar[left].pop(index)
                    for z in grammar[right]:
                        grammar[left].append(z)



    def is_mixed_terminals_exist(self, grammar):
        # in form of: 
        # (non−terminal) -> (terminal)(non−terminal)
        #                  ~ OR ~
        # (non−terminal) -> (non-terminal)(terminal)))
        #                  ~ OR ~
        # (non−terminal) -> (non-terminal)(non-terminal)(non-terminal)...
        # X -> yZ || X -> Zy || X -> A B C...
        index = 1
        long_productions = []
        removed_prod = []
        for rule in list(grammar.items()):
            for symbol in rule[1]:
                if len(symbol) > 2 and symbol not in long_productions:
                    long_productions.append(symbol)
                for prod in long_productions:
                    if len(prod)>2:
                        left = self.find_lhs(grammar, rule)
                        for times in range(2):
                            removed_prod.append(prod[0])
                            prod.remove(prod[0]) 
                        #creates new rule name (ex: N1,N2..etc.)
                        new_rule = f"{'N'}{str(index)}"
                        index += 1
                        self.rules[new_rule] = [removed_prod]
                        rule[1].append([removed_prod])
                        self.non_terminals.append(new_rule)
                        prod.insert(0,new_rule)
        index = 1                    
        for nt in list(grammar.items()):
            print(nt)
            for symbol in nt[1]:
                if len(symbol) > 1:
                    for item in symbol:
                        if item in self.terminals:
                            position = symbol.index(item)
                            symbol.remove(item)
                            new_rule = f"{'N'}{str(index)}"
                            index += 1
                            grammar[new_rule] = [list(item)]
                            symbol.insert(position,new_rule)
                            self.non_terminals.append(new_rule)
            
    # -----------------------------------------------------------------
    # Converts a given CFG formatted grammar into the form of CNF.
    # (non−terminal) -> (non−terminal)(non−terminal) :: n - 1
    # (non−terminal) -> (terminal) :: n
    # Totally :: 2n + 1 rules applied where n is the length of string
    # # However CNF reduces complexity by constraining the number of LHS
    # to 2 and it gives us the complexity of O(n^3).
    # 
    # STEPS: 
    # 0. Start Symbol: If start symbol S occurs on some right side create
    # a new start symbol S' and a new production S' -> S
    # 1. Elimiate ε-Rules: 
    # 2. Eliminate Unit Productions
    # 3. Replace Long Productions with Shorter Ones
    # 4. Move Terminals to Unit Productions
    # -----------------------------------------------------------------
    def converter( self, grammar ):
        converted_grammar = dict()
        rules = list(grammar.items())
        if(self.is_start_symbol_in_rhs(grammar)):
            new_rule = f"{self.start_symbol}'"
            grammar[new_rule] = [[self.start_symbol]]
        self.is_epsilon_exist(grammar)
        self.is_unit_production_exist(grammar)
        self.is_mixed_terminals_exist(grammar)
        #if(self.epsilons):
        #    for epsilon in self.epsilons:
        #        symbols = [ for e in rules[1]]
        print("\nGRAMMAR:\n",grammar)


if __name__ == '__main__':
    Parser()