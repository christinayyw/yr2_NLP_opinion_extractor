from sussex_nltk.parse import load_parsed_dvd_sentences

aspect = "dialogue" # Our aspect word
parsed_sentences = load_parsed_dvd_sentences(aspect)

def opinion_extractor(aspect_token, parsed_sentence):

    # Initialise a list of opinions
    opinions = []

    # Initialize the state of ADVERB, ADJECTIVE and NEGATIVE STATEMENT
    adv = ""
    adj = ""
    conj = ""
    neg = False

    # Initialize head of aspect token for further use
    head_of_aspect_token = parsed_sentence[aspect_token.head-1]



    # Find opinions


    # CASE1: if HEAD of aspect token is ADJECTIVE--------------------------------------------------------

    if aspect_token.deprel == "nsubj" and head_of_aspect_token.pos == "JJ":
        #store the ADJECTIVE found.
        adj = head_of_aspect_token.form

        #loop through all dependants of the ADJECTIVE to find NEGATIVE / ADVERB
        for dependant in parsed_sentence.get_dependants(head_of_aspect_token):
            if dependant.deprel == "neg":
                neg = True
            elif dependant.deprel == "advmod":
                adv = dependant.form

        #find final opinion
        if neg:
            opinions +=["not-"+adv+" "+ adj]
        else:
            if adv =="":
                opinions+=[adj]
            else:
                opinions +=[adv+"-"+ adj]



    # CASE2: if DEPENDANT of aspect token is ADJECTIVE----------------------------------------------------

    else:
        for dependant in parsed_sentence.get_dependants(aspect_token):
            if dependant.pos =="JJ":

                #store the ADJECTIVE found.
                adj = dependant.form

                #loop through all dependants of the ASPECT TOKEN to find NEGATIVE / ADVERB
                for dependant2 in parsed_sentence.get_dependants(aspect_token):
                    if dependant2.deprel == "neg":
                        neg = True
                    elif dependant2.deprel == "advmod":
                        adv = dependant2.form

                #check if any dependant of the ADJECTIVE token has NEGATIVE / ADVERB
                for dependant3 in parsed_sentence.get_dependants(dependant):
                    if dependant3.deprel == "neg":
                        neg=True
                    if dependant3.deprel == "advmod":
                        adv = dependant3.form

                #find final opinion
                if neg:
                    opinions +=["not-"+adv+" "+ adj]
                else:
                    if adv == "":
                        opinions +=[adj]
                    else:
                        opinions +=[adv+"-"+ adj]


    # STEP3: Find CONJUNCTIONS----------------------------------------------------------------------------

    #check all dependants of the HEAD of ASPECT TOKEN
    for dependant in parsed_sentence.get_dependants(head_of_aspect_token):

        if dependant.deprel == "conj" and dependant != aspect_token:

            #if CONJUNCTION was found, store it.
            conj = dependant.form

            #loop through all dependants of the CONJUNCTION to find NEGATIVE / ADVERB
            for dependant2 in parsed_sentence.get_dependants(dependant):
                if dependant2.deprel == "neg":
                    neg = True
                elif dependant2.deprel == "advmod":
                    adv = dependant2.form

            #find final opinion
            if neg:
                opinions +=["not-"+adv+" "+ conj]
            else:
                if adv == "":
                    opinions +=[conj]
                else:
                    opinions +=[adv+"-"+ conj]

    return opinions



from sussex_nltk.parse import load_parsed_dvd_sentences, load_parsed_example_sentences

save_file_path = r"N:/STUDY/natural laguage engineering/lab8/lab8/dialogueOUTPUT.txt" # Set this to the location of the file you wish to create/overwrite with the saved output.

# Tracking these numbers will allow us to see what proportion of sentences we discovered features in
sentences_with_discovered_features = 0 # Number of sentences we discovered features in
total_sentences = 0 # Total number of sentences

# This is a "with statement", it invokes a context manager, which handles the opening and closing of resources (like files)
with open(save_file_path, "w") as save_file: # The 'w' says that we want to write to the file
    # Iterate over all the parsed sentences
    for parsed_sentence in load_parsed_dvd_sentences(aspect):
        total_sentences += 1 # We've seen another sentence
        opinions = [] # Make a list for holding any opinions we extract in this sentence

        # Iterate over each of the aspect tokens in the sentences (in case there is more than one)
        for aspect_token in parsed_sentence.get_query_tokens(aspect):
            # Call your opinion extractor
            opinions += opinion_extractor(aspect_token, parsed_sentence)
        # If we found any opinions, write to the output file what we know.
        if opinions:
            # Currently, the sentence will only be printed if opinions were found. But if you want to know what you're missing, you could move the sentence printing outside the if-statement
            # Print a separator and the raw unparsed sentence
            save_file.write("--- Sentence: %s ---\n" % parsed_sentence.raw()) # "\n" starts a new line
            # Print the parsed sentence
            save_file.write("%s\n" % parsed_sentence)
            # Print opinions extracted
            save_file.write("Opinions: %s\n" % opinions)
            sentences_with_discovered_features += 1 # We've found features in another sentence
print "%s sentences out of %s contained features" % (sentences_with_discovered_features, total_sentences)

