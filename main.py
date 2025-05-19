import csv
import nltk
import string  
nltk.download('punkt') 

def get_tag_from_input(input_value):
    # Mapping shortcuts to tags
    if input_value == "":
        return "O"
    elif input_value == "2":
        return "B-NG"
    elif input_value == "3":
        return "I-NG"
    else:
        return input_value  # Return the input as the tag

def replace_commas(word_data):
    for key in word_data:
        if isinstance(word_data[key], str) and ',' in word_data[key]:
            word_data[key] = word_data[key].replace(',', 'COMMA')
    return word_data

def tag_corpus(corpus_file):
    # Display input shortcuts for the user (adjust prompts for Greek if needed)
    print("Input shortcuts:")
    print("1 - O (Outside any entity)")
    print("2 - B-NG (Beginning of negation)")
    print("3 - I-NG (Inside negation)")
    print("Press 'c' to correct the previous word\n")

    with open(corpus_file, 'r', encoding='utf-8') as file:
        corpus = file.read()

    sentences = nltk.sent_tokenize(corpus, language='greek')  # Tokenize Greek text into sentences
    tagged_words = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence, language='greek')  # Tokenize Greek sentence into words

        print("\nSentence:")
        print(" ".join(words))
        print("\n")

        tagged_sentence = []
        i = 0
        while i < len(words):
            word = words[i]

            if word == ",":
                word = "COMMA"  # Replace comma with "COMMA"

            tag_input = input(f"Tag for '{word}': ")
            
            if tag_input.lower() == 'c' and i > 0:
                tagged_sentence.pop()  # Remove the last word from the list
                i -= 1  # Move back one word

            else:
                tag = get_tag_from_input(tag_input)  # Get the tag based on user input
                tagged_sentence.append({
                    "Word": word,
                    "Word-2": words[i - 2] if i >= 2 else 'NULL',
                    "Word-1": words[i - 1] if i >= 1 else 'NULL',
                    "Word+1": words[i + 1] if i < len(words) - 1 else 'NULL',
                    "Word+2": words[i + 2] if i < len(words) - 2 else 'NULL',
                    "Tag": tag
                })
                i += 1  # Move to the next word

        tagged_words.extend(tagged_sentence)

    tagged_words = [replace_commas(word_data) for word_data in tagged_words]

    with open('tagged_corpus.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Word", "Word-2", "Word-1", "Word+1", "Word+2", "Tag"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for word_data in tagged_words:
            writer.writerow(word_data)

# Usage: Replace 'your_corpus.txt' with the path to your Greek corpus file
tag_corpus('your_greek_corpus.txt')

