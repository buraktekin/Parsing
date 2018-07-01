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

# -*- coding: utf-8 -*-

import sys, os
from collections import defaultdict
from CNF_converter import CNF

class Parser:
    def __init__(self):
        #-----------------------------------------------
        # Grammar in CNF
        self.cnf_rules = CNF().rules
        #-----------------------------------------------
        # CONSTANTS:
        self.set_of_tokens = list()
        self.filename = "sentence.txt"
        self.strings_of_rows = defaultdict(list)
        self.table_rows = defaultdict(list)
        #-----------------------------------------------
        # Memory // history 
        self.mem = defaultdict(list)
        #-----------------------------------------------
        # Initialization
        self.load_sentences(self.filename)
        self.bottom_up()
        print(f"\n#--------------------\n{self.cnf_rules}\n#--------------------\n")

    
    def load_sentences(self, filename):
        self.filename = filename
        with open(self.filename, "r") as sentences:
            lines = sentences.readlines()
            for line in lines:
                self.set_of_tokens.append(line.split())
    
    def _generate_row_productions(self, row, sentence):
        result = list()
        sentence = [[x] for x in sentence]
        for index, item in enumerate(sentence):
            new_string = sentence[index:index + row]
            if len(new_string) == row:
                if row < 3:
                    result.append(new_string)
                else:
                    for num in range(len(new_string) - 1):
                        temp_string = [new_string[:num + 1], new_string[num+1:]]
                        result.append(temp_string)
        return result

    #-----------------------------------------------
    # NOTE:
    # mutual with the method _find_cells()
    #-----------------------------------------------
    def _generate_strings(self):
        for sentence in self.set_of_tokens:
            for index in range(len(sentence)):
                row = self._generate_row_productions(index + 1, sentence)
                self.strings_of_rows[index + 1] = row
    #-----------------------------------------------

    def _cartesian_product(self, first, second):
        result = list()
        for i in first:
            for j in second:
                result.append([i,j])
        return result

    def _find_lhs_from_rhs(self, rhs_rule):
        temp_lhs = list()
        for lhs in self.cnf_rules:
            if rhs_rule in self.cnf_rules[lhs]:
                temp_lhs.append(lhs)
        return temp_lhs

    def bottom_up(self):
        self._generate_strings()
        strings = self.strings_of_rows
        for index in strings:
            for string in strings[index]:
                for s in string:
                    if len(string) == 1:
                        lhs = self._find_lhs_from_rhs(s)
                        self.table_rows[index].append(lhs)
                        if lhs not in self.mem[str(s)]:
                            self.mem[str(s)].append(lhs)
                    else:
                        print(str(s), " ---> ", self.mem[str(s)])
        print(self.mem)


if __name__ == '__main__':
    Parser()