import math
import re



def get_probability_distribution_of_ngrams(selected_text, n, ngrams_and_their_respective_probability):
    for i in range(len(selected_text) -n + 1):
        if selected_text[i:i+n] in ngrams_and_their_respective_probability:
            ngrams_and_their_respective_probability[selected_text[i:i+n]] += 1
        else:
            ngrams_and_their_respective_probability[selected_text[i:i+n]] = 1
    return ngrams_and_their_respective_probability



def structure_of_entropy_of_text():
    chunk_size = 1024*1024
    entropy_per_letter_of_different_lenghts_of_ngrams = {}



    for i in range(1,11):
        ngrams_and_their_respective_probability = {}
        k=1



        with open("SvenskaWikipedia.txt", "r", encoding='utf-8', errors='ignore') as file:
            while chunk := file.read(chunk_size):
                cleaned_text = re.sub(r"[^a-zåäö ]", "", chunk.lower())
                cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
                ngrams_and_their_respective_probability = get_probability_distribution_of_ngrams(cleaned_text, i, ngrams_and_their_respective_probability)
                print(k)
                k+=1



        total_count_of_frequency = sum(ngrams_and_their_respective_probability.values())
        ngrams_and_their_respective_probability = {word_string: count / total_count_of_frequency for word_string, count in ngrams_and_their_respective_probability.items()}

            

        entropy_using_ngrams = 0

        for word_string, probability in ngrams_and_their_respective_probability.items():
            entropy_using_ngrams -= probability * (math.log2(probability))

        entropy_per_letter = entropy_using_ngrams / i

        entropy_per_letter_of_different_lenghts_of_ngrams[i] = entropy_per_letter
        print(i)
    


    print(entropy_per_letter_of_different_lenghts_of_ngrams)



structure_of_entropy_of_text()