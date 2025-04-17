import math
from ordlista import data
from metod4förberäkning import PreCalculations2_best_first_guesses



word_dict = {}

for line in data.split("\n"):
    word, number = line.split(",")
    word_dict[word] = int(number)

total_count_of_frequency = sum(word_dict.values())

word_list = {word: count / total_count_of_frequency for word, count in word_dict.items()}

best_first_guesses = PreCalculations2_best_first_guesses


alphabet = "abcdefghijklmnopqrstuvwxyz"



def find_the_best_guess_with_informationtheory(word_list_according_to_information):
    letters_and_their_corresponding_entropies = {letter: 0 for letter in alphabet}
        
    for letter in alphabet:
        
        probability_distribution_of_letter = {tuple([]): 0}

        for word in word_list_according_to_information:
            if letter in word:
                list_of_places_of_letter = tuple([i for i, char in enumerate(word) if char == letter])
                if list_of_places_of_letter in probability_distribution_of_letter:
                    probability_distribution_of_letter[list_of_places_of_letter] += word_list_according_to_information[word]
                else:
                    probability_distribution_of_letter[list_of_places_of_letter] = word_list_according_to_information[word]
            else:
                probability_distribution_of_letter[tuple([])] += word_list_according_to_information[word]



        total_entropy_of_guess = 0

        for key, value in probability_distribution_of_letter.items():
            if value != 0:
                total_entropy_of_guess -= value * (math.log2(value))
        


        letters_and_their_corresponding_entropies[letter] = total_entropy_of_guess
        


    sorted_letters = dict(sorted(letters_and_their_corresponding_entropies.items(), key=lambda item: item[1], reverse=True))
    return sorted_letters



def hangman_using_informationtheory(the_current_word):
    word_list_according_to_information = {word: count for word, count in word_list.items() if len(word) == len(the_current_word)}
    wrong_guesses = 0
    checking_number = 0



    while True:
        if len(word_list_according_to_information) > 1:
            total_probability_according_to_information = sum(word_list_according_to_information.values())
            word_list_according_to_information = {word: count / total_probability_according_to_information for word, count in word_list_according_to_information.items()}



            if checking_number == 1:
                list_of_best_guesses_in_order = find_the_best_guess_with_informationtheory(word_list_according_to_information)
                letter_in_word = list(list_of_best_guesses_in_order.keys())[0]
            else:
                letter_in_word = best_first_guesses[len(the_current_word)]
                checking_number = 1
            


            if letter_in_word in the_current_word:
                list_of_places_of_letter = [i for i, char in enumerate(the_current_word) if char == letter_in_word]
                word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if has_letter_only_at_positions(word, list_of_places_of_letter, letter_in_word)}
            else:
                wrong_guesses += 1
                word_list_according_to_information = {word: count for word, count in word_list_according_to_information.items() if letter_in_word not in word}

            

            if len(word_list_according_to_information) == 1:
                break
        else:
            if len(word_list_according_to_information) == 1:
                break
    
    

    return wrong_guesses



def has_letter_only_at_positions(word, positions, letter_in_word):
    for i, char in enumerate(word):
        if char == letter_in_word and i not in positions:
            return False
        if i in positions and char != letter_in_word:
            return False
    return True



def structure_of_hangman_statistics():
    wrong_guesses_statistics = {}
    p = 1


    for word in word_list:
        wrong_guesses = hangman_using_informationtheory(word)



        if wrong_guesses in wrong_guesses_statistics:
            wrong_guesses_statistics[wrong_guesses] += word_list[word]
        else:
            wrong_guesses_statistics[wrong_guesses] = word_list[word]
        print(p)
        p+=1
    


    wrong_guesses_statistics = dict(sorted(wrong_guesses_statistics.items()))

    print(wrong_guesses_statistics)



structure_of_hangman_statistics()