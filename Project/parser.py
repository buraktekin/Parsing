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
import itertools

class Parser:
    # -----------------------------------------------------------------
    # create dictionaries to hold the rules to make it easier to reach
    # them, while the production is on going.
    # -----------------------------------------------------------------
    def __init__(self):
        self.EPSILON = "ε"
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

        self.load_grammar("./grammar.cfg")
        print(self.derivations)
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
        for value in list(grammar.items()):
            for symbol in value[1]:
                if( term in symbol ):
                    return value[0]

    def new_productions(self, prev, new):
        flatten = [item for sublist in new for item in sublist if item != self.EPSILON]
        production = [[p, n] for p in prev for n in flatten ]
        return production


    def is_epsilon_exist(self, grammar):
        temp_epsilons = list()
        addition = list()
        items = grammar.items()
        for rule in grammar:
            for symbol in grammar[rule]:
                if( self.EPSILON in symbol ):
                    addition = grammar[rule][:]
                    grammar[rule].remove(symbol)
                    self.epsilons[rule] = grammar[rule]
                    temp_epsilons.append(rule)
        
        for check_symbol in temp_epsilons:
            for rule in items:
                for r in rule[1]:
                    if( check_symbol in r ):
                        for _ in range(r.count(check_symbol)):
                            index = grammar[rule[0]].index(r)
                            del grammar[rule[0]][index]
                            r_new = r[:]
                            r_new.remove(check_symbol)
                            if(r_new):
                                production = self.new_productions(r_new, addition)
                                r_new = [r_new] + production
                            else:
                                r_new += grammar[check_symbol]
                            grammar[rule[0]] += r_new
                        print(r)
                        


    def is_unit_production_exist(self, grammar):
        for rule in list(grammar.values()):
            for symbol in rule:
                non_terminals = [n_t for n_t in symbol if n_t in self.non_terminals]
                if( len( symbol ) == 1 and non_terminals ):
                    self.unit_productions.append(symbol)


    def is_mixed_terminals_exist(self, grammar):
        # in form of: 
        # (non−terminal) -> (terminal)(non−terminal)
        #                  ~ OR ~
        # (non−terminal) -> (non-terminal)(terminal)))
        # X -> yZ || X -> Zy
        for rule in list(grammar.values()):
            for symbol in rule:
                terminals = [t for t in symbol if t in self.terminals]
                if( ( len( symbol ) == 2 ) and terminals ):
                    self.mixed_type.append(rule)
            
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
        self.is_epsilon_exist(grammar)
        self.is_unit_production_exist(grammar)
        self.is_mixed_terminals_exist(grammar)

        print(grammar)
        #if(self.epsilons):
        #    for epsilon in self.epsilons:
        #        symbols = [ for e in rules[1]]

        #epsilon in [x for v in values for x in v if type(v)==list]
        #self.is_unit_production_exist(rule)
        #self.is_mixed_terminals_exist(rule)



if __name__ == '__main__':
    Parser()