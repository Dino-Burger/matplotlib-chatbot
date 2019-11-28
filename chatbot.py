import pandas as pd
import numpy as np
import importlib

conf = importlib.import_module('chatbot_config')

def process_input_data(input_data):
    # replace ["*"] in start_states by actual list of all states
    all_intents = [member["intent"] for member in input_data if "intent" in member]
    for member in input_data:
        if "start_states" in member and member["start_states"] == ["*"]:
            member["start_states"] = all_intents
    return input_data

input_data = process_input_data(conf.input_data_raw)
input_data_edges = [ member for member in input_data if "start_states" in member]
input_data_nodes = [ member for member in input_data if "intent" in member]


# cosine tfidf model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

word_vectorizer = TfidfVectorizer()
all_patterns = [pat for edge in input_data_edges for pat in edge["patterns"]]
word_vectorizer.fit(all_patterns)

# add tfidf vectors to input_data_edges
for edge in input_data_edges:
    patterns = edge["patterns"]
    pattern_vectors = word_vectorizer.transform(patterns)
    edge["pattern_vectors"] = pattern_vectors

def get_possible_next_pattern_vectors_old(curr_state):
    # returns [(pat_vec, pat, end_state)]
    next_states = [ (member["pattern_vectors"][i_vec], 
                    member["patterns"][i_vec],
                    member["end_state"]) 
                    for member in input_data_edges 
                    for i_vec in range(member["pattern_vectors"].shape[0])
                    if curr_state in member["start_states"]]
    return next_states

def get_possible_next_pattern_vectors(curr_state, curr_contexts):
    # returns [(pat_vec, pat, end_state)]
    next_states = [ (edge["pattern_vectors"][i_vec], 
                    edge["patterns"][i_vec],
                    edge["end_state"]) 
                    for edge in input_data_edges 
                    for i_vec in range(edge["pattern_vectors"].shape[0])
                    if curr_state in edge["start_states"]
                    and set(get_context_require_from_intent(edge["end_state"])).issubset(set(curr_contexts))]
    return next_states

def get_closest_command(possible_next_pattern_vectors: list, inp:str):
    input_vector = word_vectorizer.transform([inp])
    all_distances = [(cosine_similarity(input_vector, pat_vec)[0][0], pat, end_state)
                        for pat_vec, pat, end_state in possible_next_pattern_vectors ]
    max_command = max(all_distances, key = lambda l: l[0])
    return max_command

def get_response_from_intent(intent):
    response = [ node.get("response", "") for node in input_data_nodes
                    if node['intent'] == intent]
    assert(len(response)==1)
    return response[0]

def get_context_require_from_intent(intent):
    response = [ node.get("context_require", []) for node in input_data_nodes
                    if node['intent'] == intent]
    assert(len(response)==1)
    return response[0]

def get_context_set_from_intent(intent):
    response = [ node.get("context_set", []) for node in input_data_nodes
                    if node['intent'] == intent]
    assert(len(response)==1)
    return response[0]

def get_field_from_intent(field_name, intent, default=[]):
    response = [ node.get(field_name, default) for node in input_data_nodes
                    if node['intent'] == intent]
    assert(len(response)==1)
    return response[0]





class Chatbot:
    def __init__(self,local_vars):
        self.local_vars = local_vars
    def run(self):
        from matplotlib import pyplot as plt
        curr_state = "entry"
        curr_contexts = []

        all_variables = {
            'csv_list': None,
            'variables_to_plot': [ ],
            'plotting_style': 'seaborn',
            'legend_location': None,
            'plotting_command': 'plot', # vs 'scatter', 'hist'    
            'all_commands': ['from matplotlib import pyplot as plt'],
        }
        continue_flag = True


        while(continue_flag):
            print("-----------------------------------")
            print("current State", curr_state)
            print("current Contexts", curr_contexts)

            # possible_next_pattern_vectors = get_possible_next_pattern_vectors_old(curr_state)
            possible_next_pattern_vectors = get_possible_next_pattern_vectors(curr_state, curr_contexts)
            possible_next_states = list(set([ns for pat_vec, pat, ns in possible_next_pattern_vectors]))
            print(possible_next_states)

            inp = input()
            rating, pat, next_state = get_closest_command(possible_next_pattern_vectors, inp)
            required_contexts = get_context_require_from_intent(next_state)

            if inp == 'end':
                continue_flag = False
                continue
            if rating < 0.6:
                print("sry, didn't understand you!")
                continue
            if not set(required_contexts).issubset(set(curr_contexts)):
                lacking_context = list(set(required_contexts)-set(curr_contexts))
                print("sry, you lack context", lacking_context, "to do this")
                continue

            parser = get_field_from_intent("code_command",
                                            next_state, 
                                            default=lambda all_variables, inp, local_vars: all_variables)
            all_variables = parser(all_variables, inp, self.local_vars)
            
            curr_state = next_state
            curr_contexts.extend(get_context_set_from_intent(next_state))
            print(get_response_from_intent(curr_state))
        print("bye")


#######################################################################################################
# Future



# create similar code blocks for scatter plot, histogram, etc. 
#######################################################################################################
# Future structure
# create 
# - a class file
# - a file with all the helper functions
# - a config file with the graph
# - the spacy_train_data.py which is called in case test.spacy is not present

#######################################################################################################
# Graveyard

def get_possible_next_states(curr_state):
    edges = [ member for member in input_data if "start_states" in member]
    next_states = [ member["end_state"] for member in edges 
                    if curr_state in member["start_states"]]
    return next_states


def get_possible_next_patterns(curr_state):
    edges = [ member for member in input_data if "start_states" in member]
    next_states = [ (patt, member["end_state"]) for member in edges for patt in member["patterns"]
                    if curr_state in member["start_states"]]
    return next_states