import random
from ordlista import data



word_dict = {}

for line in data.split("\n"):
    word, number = line.split(",")
    word_dict[word] = int(number)

total_count_of_frequency = sum(word_dict.values())

word_dict_with_probabilities = {word: count / total_count_of_frequency for word, count in word_dict.items()}

word_list = list(word_dict_with_probabilities.keys())



def hangman_using_informationtheory(the_current_word):
    word_list_according_to_information = [word for word in word_list if len(word) == len(the_current_word)]
    wrong_guesses = 0
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y","z"]



    while True:
        if len(word_list_according_to_information) > 1:
            letter_in_word = random.choice(alphabet)
            alphabet.remove(letter_in_word)
            

            
            if letter_in_word in the_current_word:
                list_of_places_of_letter = [i for i, char in enumerate(the_current_word) if char == letter_in_word]
                word_list_according_to_information = [word for word in word_list_according_to_information if has_letter_only_at_positions(word, list_of_places_of_letter, letter_in_word)]
            else:
                wrong_guesses += 1
                word_list_according_to_information = [word for word in word_list_according_to_information if letter_in_word not in word]

            

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



    k=1
    for word in word_list:
        wrong_guesses = hangman_using_informationtheory(word)



        if wrong_guesses in wrong_guesses_statistics:
            wrong_guesses_statistics[wrong_guesses] += 1
        else:
            wrong_guesses_statistics[wrong_guesses] = 1
        print(k)
        k+=1
    
    

    wrong_guesses_statistics = dict(sorted(wrong_guesses_statistics.items()))

    wrong_guesses_statistics = {number: count / len(word_list) for number, count in wrong_guesses_statistics.items()}

    print(wrong_guesses_statistics)



structure_of_hangman_statistics()