__author__ = 'yw221'

from sussex_nltk.parse import load_parsed_dvd_sentences
aspect = "dialogue"
parsed_sentences = load_parsed_dvd_sentences(aspect)

for parsed_sentence in parsed_sentences:
    aspect_tokens = parsed_sentence.get_query_tokens(aspect)
    dependants = parsed_sentence.get_dependants(aspect_token)
    for dependant in dependants:
        print dependant

