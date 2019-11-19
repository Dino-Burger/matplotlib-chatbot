input_data_raw = [
    # entry
    # No incoming connections for "entry"
    {   "intent": "entry",
        "response": "Welcome!", },

    # plot
    {   "start_states": ["*"],
        "end_state": "plot",
        "patterns": ["make a line plot", "draw a line plot", "create a line plot", "Plot x"] },

    {   "intent": "plot",
        "response": "", },
   
    # hist
    {   "start_states": ["*"],
        "end_state": "hist",
        "patterns": ["make a histogram of x"] },

    {   "intent": "hist",
        "response": "", },    

    # hist_with_bins
    {   "start_states": ["*"],
        "end_state": "hist_with_bins",
        "patterns": ["make a histogram of x with y bins"] },

    {   "intent": "hist_with_bins",
        "response": "", }, 

    # add_legend
    {   "start_states": ["*"],
        "end_state": "add_legend",
        "patterns": ["add legend", "add description"] },

    {   "intent": "add_legend",
        "response": "Would you like to place the legend to the left or the right?", },    

    # add_legend_top_left
    {   "start_states": ["add_legend"],
        "end_state": "add_legend_top_left",
        "patterns": ["top left", ] },
    {   "start_states": ["*"],
        "end_state": "add_legend_top_left",
        "patterns": ["add legend top left", "add description top left"] },

    {   "intent": "add_legend_top_left",
        "response": "", },    

    # add_legend_top_right
    {   "start_states": ["add_legend"],
        "end_state": "add_legend_top_right",
        "patterns": ["top right", ] },
    {   "start_states": ["*"],
        "end_state": "add_legend_top_right",
        "patterns": ["add legend top right", "add description top right"] },

    {   "intent": "add_legend_top_right",
        "response": "", },    

]

def process_input_data(input_data):
    # replace ["*"] in start_states by actual list of all states
    all_intents = [member["intent"] for member in input_data if "intent" in member]
    for member in input_data:
        if "start_states" in member and member["start_states"] == ["*"]:
            member["start_states"] = all_intents
    return input_data

input_data = process_input_data(input_data_raw)
input_data_edges = [ member for member in input_data if "start_states" in member]
input_data_nodes = [ member for member in input_data if "intent" in member]


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

def get_possible_next_pattern_vectors(curr_state):
    next_states = [ (member["pattern_vectors"][i_vec], 
                    member["patterns"][i_vec],
                    member["end_state"]) 
                    for member in input_data_edges 
                    for i_vec in range(member["pattern_vectors"].shape[0])
                    if curr_state in member["start_states"]]
    return next_states




# versuch für etwas interaktives

curr_state = "entry"
continue_flag = True

while(continue_flag):
    print("current State", curr_state)
    possible_next_pattern_vectors = get_possible_next_pattern_vectors(curr_state)
    possible_next_states = [ns for pat_vec, pat, ns in possible_next_pattern_vectors]
    print(possible_next_states)

    inp = input()

    if inp == 'end':
        continue_flag = False
    else:
        curr_state = inp

