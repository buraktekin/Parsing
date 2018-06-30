from collections import defaultdict

class CNF(object):
    """
    !! IMPORTANT NOTE !!:
    This part will be referenced in comments in the code base below. While referencing the symbol
    '@' will be in use.
    
    Rules to follow for chomsky normal form conversion are as follows:
    1. Define a start symbol. If there is Start Symbol on the right hand side (RHS), create 
    a new rule which derives Start Symbol (S).
    2. Get rid of ε-productions if any exists.
    3. Get rid of all productions with one non-terminal symbol on the RHS.
    4. Replace all long productions (which has more than 2 symbols) with the shorter ones.
    5. Move all terminals to productions.
    """

    def __init__(self):
        #-----------------------------------------------
        # CONSTANTS:
        self.id = 0
        self.EPSILON = "ε"
        self.start_symbol = None
        self.filename = "grammar.txt"
        self.non_terminals = list()
        self.terminals = list()
        #-----------------------------------------------
        # NOTE:
        # RULES: this turns all productions into a list 
        # and if there is no available key then this 
        # returns an empty list
        self.rules = defaultdict(list)
        #-----------------------------------------------
        # NOTE:
        # Load Grammar from text file...
        self.load_grammar("./grammar.txt")
        self._eliminate_epsilon_productions()
        self._eliminate_unit_productions()
        self._eliminate_terminal_with_nonterminal()
        self._eliminate_longer_productions()

    #-----------------------------------------------
    # FIND AND DEFINE THE START SYMBOL
    def define_start_symbol(self, symbol):
        self.start_symbol = symbol
    # END OF START SYMBOL DEFINITION
    #-----------------------------------------------

    #-----------------------------------------------
    # LOAD GRAMMAR FROM A FILE
    def load_grammar(self, filename):
        self.filename = filename
        with open(self.filename, "r") as grammar:
            rules = grammar.readlines()
            for rule in rules:
                #-----------------------------------------------
                # Split lhs and rhs of the rules to
                # create a dictionary of rules
                lhs, rhs = rule.strip().split(" -> ")
                self.non_terminals.append(lhs)
                rhs_symbols = rhs.strip().split(" | ")
                if rules.index(rule) == 0:
                    self.start_symbol = lhs
                for r in rhs_symbols:
                    self.rules[lhs].append(r.split())
                #-----------------------------------------------
                # NOTE:
                # Check start symbol: Rule @1
                self.check_start_symbol_on_rhs(
                    self.start_symbol, 
                    rhs_symbols
                )
                #-----------------------------------------------
        return self.rules
        # DONE
    # END OF LOADING THE GRAMMAR
    #-----------------------------------------------

    #-----------------------------------------------
    # FIND AND ELIMINATE RHS START SYMBOLS
    def check_start_symbol_on_rhs(self, symbol, rhs):
        #-----------------------------------------------
        ''' If RHS carries the start symbol generate a new rule '''
        if symbol in rhs:
            new_symbol = symbol + "'"
            self.rules[new_symbol].append([symbol])
            self.start_symbol = new_symbol
        # DONE
    # END OF RHS START SYMBOL
    #-----------------------------------------------


    #-----------------------------------------------
    # FIND AND ELIMINATE EPSILON PRODUCTIONS
    def find_epsilon_productions(self):
        for lhs in self.rules:
            if not self.start_symbol is None and lhs == self.start_symbol:
                continue
            for index, rhs in enumerate(self.rules[lhs]):
                if self.EPSILON in rhs:
                    return lhs, index # EPSILON found in index 'index'

        return None, None

    def _eliminate_epsilon_productions(self):
        while True:
            # Get the production rules have EPSILON in it.
            lhs, index = self.find_epsilon_productions()
            
            #-----------------------------------------------
            # NOTE:
            # if find_epsilon_productions returns nothing 
            # for LHS then break the loop.
            if lhs is None:
                break
            #-----------------------------------------------
            # NOTE: 
            # Delete epsilon rule from RHS
            del self.rules[lhs][index]
            #-----------------------------------------------

            # Create the new productions for the rules that 
            # contains the LHS non-terminals which has 
            # EPSILON rule.
            for symbol in self.rules:
                no_epsilon = list()
                for possible_rhs_of_rule in self.rules[symbol]:
                    number_of_epsilon_carrier = possible_rhs_of_rule.count(lhs)
                    if (number_of_epsilon_carrier == 0) & (possible_rhs_of_rule not in no_epsilon):
                        no_epsilon.append(possible_rhs_of_rule)
                    else:
                        new_productions = self._create_new_productions(
                                rhs = possible_rhs_of_rule,
                                lhs = lhs,
                                number_of_epsilon = number_of_epsilon_carrier
                            )
                        if new_productions not in no_epsilon:
                            no_epsilon.extend(new_productions)

                self.rules[symbol] = no_epsilon
                # DONE

    def _create_new_productions(self, rhs, lhs, number_of_epsilon):
        ''' 
            NOTE:
            ( !! VERY CHALLENGING !! POSSIBLY NEED A REFACTORING )
            Lets say we have rules like B -> ... | ε and S -> BS then
            the following productions should be generated:
                S -> BS | S
                    |- 2 new productions -|

            2. if B -> ... | ε and S -> BSB then
                S -> BSB | BS | SB | S
                    |- 4 new productions -|
            
            3. if B -> ... | ε and S -> BSBSB then
                S -> BSBSB | SBSB | BSSB | BSBS | SSB | BSS | SBS | SS
                    |---------------- 8 new productions --------------|

            ... and so on.

            As you can see the number of new productions changes by the nth 
            power of 2 where n is the number of non-terminals which has ε production.
            So, while we creating new productions we would create 2^n new productions
            for the production carrying ε production and replace that production with
            the output.
        '''

        number_of_productions = 2 ** number_of_epsilon
        list_of_new_productions = []

        for i in range(number_of_productions):
            nth_nt = 0
            new_production = []
            for s in rhs:
                if s == lhs:
                    if i & (2 ** nth_nt):
                        new_production.append(s)
                    nth_nt += 1
                else:
                    new_production.append(s)
            if len(new_production) == 0:
                new_production.append(self.EPSILON)
            list_of_new_productions.append(new_production)
        return list_of_new_productions
    # END OF EPSILON PRODUCTION
    #-----------------------------------------------

    #-----------------------------------------------
    # FIND UNIT PRODUCTIONS ON THE FLY    
    def _find_unit_productions(self):
        for lhs in self.rules:
            for index, rhs in enumerate(self.rules[lhs]):
                if(len(rhs) == 1):
                    if rhs[0] in self.non_terminals:
                        return lhs, index
                    else:
                        self.terminals.append(rhs[0])
                        # remove duplicates
                        self.terminals = list(set(self.terminals))
        
        return None, None

    def _eliminate_unit_productions(self):
        while True:
            # Get the production rules have unit productions 
            # in it.
            lhs, index = self._find_unit_productions()
            
            #-----------------------------------------------
            # NOTE:
            # if find_unit_productions returns nothing 
            # for LHS then break the loop.
            if lhs is None:
                break
            #-----------------------------------------------
            # NOTE:
            # Copy the one to be deleted and delete that unit
            # rule from corresponding RHS
            removing_part = self.rules[lhs][index][:]
            del self.rules[lhs][index]
            #-----------------------------------------------

            if removing_part[0] != lhs:
                self.rules[lhs] += self.rules[removing_part[0]]
            # DONE
    # END OF UNIT PRODUCTION
    #-----------------------------------------------

    #-----------------------------------------------
    # FIND A RULE THAT A TERMINAL IS COMBINED WITH A
    # NON-TERMINAL
    def _find_terminal_with_nonterminal(self):
        for lhs in self.rules:
            for index, rhs in enumerate(self.rules[lhs]):
                if(len(rhs) == 2):
                    for symbol in rhs:
                        if symbol in self.terminals:
                            symbol_index = self.rules[lhs][index].index(symbol)
                            return lhs, index, symbol_index
        
        return None, None, None

    def _eliminate_terminal_with_nonterminal(self):
        while True:
            # Get the production rules have unit productions 
            # in it.
            lhs, index, symbol_index = self._find_terminal_with_nonterminal()
            #-----------------------------------------------
            # NOTE:
            # if find_unit_productions returns nothing 
            # for LHS then break the loop.
            if lhs is None:
                break
            #-----------------------------------------------
            # NOTE:
            # Copy the one to be deleted and delete that unit
            # rule from corresponding RHS
            new_rule_lhs = f"NR{str(self.id)}"
            self.id += 1
            self.rules[new_rule_lhs] = [[self.rules[lhs][index][symbol_index]]]
            del self.rules[lhs][index][symbol_index]
            self.rules[lhs][index].insert(symbol_index, new_rule_lhs)
            #-----------------------------------------------
            # DONE
    # END OF TERMINAL WITH NONTERMINAL
    #-----------------------------------------------

    #-----------------------------------------------
    # FIND A RULE THAT RHS HAS MORE THAN 2 SYMBOLS
    def _find_longer_productions(self):
        for lhs in self.rules:
            for index, rhs in enumerate(self.rules[lhs]):
                if(len(rhs) > 2):
                    return lhs, index
        
        return None, None

    def _eliminate_longer_productions(self):
        mem = list()
        while True:
            # Get the production rules have unit productions 
            # in it.
            lhs, index = self._find_longer_productions()
            #-----------------------------------------------
            # NOTE:
            # if find_unit_productions returns nothing 
            # for LHS then break the loop.
            if lhs is None:
                break    
            #-----------------------------------------------
            # NOTE:
            # Create new productions
            if self.rules[lhs][index] not in mem:
                mem.append(self.rules[lhs][index])
                self._generate_shorter_rules(self.rules[lhs][index])
            # DONE
    def _generate_shorter_rules(self, rhs):
        pop_index = 0
        new_production = list()
        while len(new_production) < 2:
            item = rhs.pop(pop_index)
            new_production.append(item)
        new_rule_lhs = f"NR{str(self.id)}"
        self.id += 1
        rhs.insert(pop_index, new_rule_lhs)
        self.rules[new_rule_lhs] = new_production
    # END OF LONGER PRODUCTIONS
    #-----------------------------------------------

    # HELPER METHODS
    def _find_lhs_from_rhs(self, rhs_rule):
        temp_lhs = list()
        for lhs in self.rules:
            if rhs_rule in self.rules[lhs]:
                temp_lhs.append(lhs)
        return temp_lhs