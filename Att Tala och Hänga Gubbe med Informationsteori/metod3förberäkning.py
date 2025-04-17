import math
from ordlista import data



word_dict = {}

for line in data.split("\n"):
    word, number = line.split(",")
    word_dict[word] = int(number)

total_count_of_frequency = sum(word_dict.values())

word_dict_with_probabilities = {word: count / total_count_of_frequency for word, count in word_dict.items()}

word_list = list(word_dict_with_probabilities.keys())

lengths = list(set([len(word) for word in word_list]))


alphabet = "abcdefghijklmnopqrstuvwxyz"



def find_the_best_guess_with_informationtheory(word_list_according_to_information):
    letters_and_their_corresponding_entropies = {letter: 0 for letter in alphabet}
        
    for letter in alphabet:
        
        probability_distribution_of_letter = {tuple([]): 0}

        for word in word_list_according_to_information:
            if letter in word:
                list_of_places_of_letter = tuple([i for i, char in enumerate(word) if char == letter])
                if list_of_places_of_letter in probability_distribution_of_letter:
                    probability_distribution_of_letter[list_of_places_of_letter] += 1
                else:
                    probability_distribution_of_letter[list_of_places_of_letter] = 1
            else:
                probability_distribution_of_letter[tuple([])] +=1
        
        total_frequency_count = len(word_list_according_to_information)
        probability_distribution_of_letter = {x: y / total_frequency_count for x,y in probability_distribution_of_letter.items()}



        total_entropy_of_guess = 0

        for key, value in probability_distribution_of_letter.items():
            if value != 0:
                total_entropy_of_guess -= value * (math.log2(value))
        


        letters_and_their_corresponding_entropies[letter] = total_entropy_of_guess
        

    
    sorted_letters = dict(sorted(letters_and_their_corresponding_entropies.items(), key=lambda item: item[1], reverse=True))
    return sorted_letters



def structure_of_hangman_best_first_guesses():
    best_first_guesses = {x: "" for x in lengths}



    for x in lengths:
        word_list_according_to_information = [word for word in word_list if len(word) == x]
        list_of_best_guesses_in_order = find_the_best_guess_with_informationtheory(word_list_according_to_information)
        best_guess = list(list_of_best_guesses_in_order.keys())[0]
        best_first_guesses[x] = best_guess
    


    return(best_first_guesses)



PreCalculations1_best_first_guesses = structure_of_hangman_best_first_guesses()