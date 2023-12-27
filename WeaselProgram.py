
import numpy as np
import random
import string
import os, sys



class Weasel:

    def __init__(self, n_copies=100, p_mutation=0.05):

        np.random.seed(10)
        # Number of copies of the string for each generation (default value:100)
        self.n_copies = n_copies

        # Probability of mutation: replace a character with a new random character (default value: 5%)
        self.p_mutation = p_mutation

        # number of generation
        self.n_generation = 0
        
        # when the random generated string is the target string the program ends
        # the comparison of the two strings is done character by character, white
        # space included
        self.target_string = "METHINKS IT IS LIKE A WEASEL"

        # total number of characters (white space included)
        self.n_char = int(len(self.target_string))

        # all ascii uppercase letters list
        self.ascii_uppercase_letters_list = list(string.ascii_uppercase)

        # all ascii uppercase letters list with white space
        self.ascii_uppercase_letters_list.append(" ")

        # this dictionary contains the copies of the string for each generation
        self.string_copies_dict = {}

        # this dictionary contains the score of the generated string
        self.score_dict = {}
        self.score_dict_init()

        # this list is used to select which character will mutate
        # a list of N 0 and 1 is created with a p=1-p_mutation for 0 and p=p_mutation for  
        self.if_mutation = [0,1]


    def score_dict_init(self):

        '''
        
        This function is used to initialize the score dictionary

        '''
        
        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)
            self.score_dict[copy_name] = 0
        
        
    def string_init(self):

        '''
        
        This function is used to initialize the initial 28 random characters string
        
        '''
        
        random_string_list = list(np.random.choice(self.ascii_uppercase_letters_list,
                                                   size=self.n_char))

        
        return random_string_list



    def make_string_copy(self):

        '''
        
        This function is used to make N copies of the string (string generated in each generation). The copies are saved in a dictionary

        '''

        random_string_list = self.string_init()
        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)            
            
            self.string_copies_dict[copy_name] = random_string_list
        

    def mutation(self):

        '''
        
        This function is used to randomly mutate the characters in the generated string

        '''

        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)
            string_list = self.string_copies_dict[copy_name]
            
            mutation_list = np.random.choice(self.if_mutation,
                                             size=self.n_char,
                                             p=[1-self.p_mutation, self.p_mutation])

            id_mutation_list = np.where(mutation_list==1)[0]
            for _id in id_mutation_list:
                self.string_copies_dict[copy_name][_id] = np.random.choice(self.ascii_uppercase_letters_list)


    def string_comparison(self):

        '''
    
        This function compares all the strings for the i-th generation with the target string

        '''

        for n in range(self.n_copies):
            copy_name = "copy_"+str(n+1)
            string_test = self.string_copies_dict[copy_name]

            for char1, char2 in zip(string_test, self.string_target):
                if(char1 == char2):
                    self.score_dict[copy_name] += 1
        

    def generation(self):

        '''
        '''

        target_condition = len([k for k in self.string_copies_dict if self.string_copies_dict[k] == self.n_char])

        while(target_condition == 0):
            if(self.n_generation == 0):
                self.make_string_copy()
                
            self.n_generation += 1

            self.mutation()
            self.string_comparison()
                    
def main():

    wp = Weasel()
    
if(__name__ == "__main__"):
    
    main()
