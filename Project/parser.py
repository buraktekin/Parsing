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
        self._generate_strings()
        print(f"\n#--------------------\n{self.cnf_rules}\n#--------------------\n")
        self._find_cells()

    
    def load_sentences(self, filename):
        self.filename = filename
        with open(self.filename, "r") as sentences:
            lines = sentences.readlines()
            for line in lines:
                self.set_of_tokens.append(line.split())
    
    def _generate_row_productions(self, row, sentence):
        result = list()
        for index, item in enumerate(sentence):
            new_string = sentence[index:index + row]
            if len(new_string) == row:
                if row < 3:
                    result.append([new_string])
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
        if not first or not second:
            return 
        result = list()
        for i in first:
            for j in second:
                result.append([i,j])

        return result

    def _bottom_to_top(self, substrings):
        new_row = list()
        key = ""
        # print("STRING: ", substrings)
        for string in substrings:
            cartesians = []
            key += " ".join(str(x) for x in string)
            if(key in self.mem):
                cartesians = self.mem[key]
                #print("CARTESIAN_IN_LINE:", cartesians)
            else:
                for terminal in range(len(string) - 1):
                    list_of_lhs_first = CNF()._find_lhs_from_rhs([string[terminal]])
                    list_of_lhs_second = CNF()._find_lhs_from_rhs([string[terminal + 1]])
                    #print("terminal: ", string[terminal], " First: ", list_of_lhs_first, " Second: ", list_of_lhs_second)
                    cartesians = self._cartesian_product(list_of_lhs_first, list_of_lhs_second)
                    for c in cartesians:
                        if key not in self.mem:
                            self.mem[key].append(CNF()._find_lhs_from_rhs(c))
                #print("CARTESIAN_IN_LINE:", cartesians)
            #print("CARTESIAN:", cartesians, "\n")
            new_row.append(cartesians)
        return new_row

    def _find_cells(self):
        for row in self.strings_of_rows:
            for substring in self.strings_of_rows[row]:
                for symbols in substring:
                    cartesian_productions = self._bottom_to_top(substring)
                    for productions in cartesian_productions:
                        if row == 1:
                            self.table_rows[1] += productions
                        else:
                            results = list()
                            for prod in productions:
                                # print("Prod: ", prod)
                                output = CNF()._find_lhs_from_rhs(prod)
                                if output not in self.table_rows[row]:
                                    self.table_rows[row] += [output]
                        #print(f"ROW{row}: ", self.table_rows[row])
            print("\n")
        print(self.table_rows)

if __name__ == '__main__':
    Parser()