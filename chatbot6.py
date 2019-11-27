import pandas as pd
import numpy as np

def is_number(x):
    result = isinstance(x, float) or isinstance(x, int)
    return result

def all_numbers(my_list):
    return all(map(is_number, my_list))

def get_plotting_candidates():
    candidates = []
    for n,v in globals().items():
        if isinstance(v, pd.DataFrame):
            candidates.append(n)
            candidates.extend(n + "['" + field + "']" for field in v.columns)
            candidates.extend(n + '["' + field + '"]' for field in v.columns)
        elif isinstance(v, list):
            if all_numbers(v) and len(v)>0:
                candidates.append(n)
        elif isinstance(v, np.ndarray):
            if len(v.shape)==1:
                candidates.append(n)
            elif len(v.shape)==2:
                candidates.append(n)
            else:
                pass 
    return candidates

import re
def var_names_by_regex(in_string):
    import re
    pattern1 = re.compile(r"""of +([a-z\[\]'"0-9]+)""", re.IGNORECASE)
    match1 = pattern1.findall(in_string)
    result1 = match1
    
    pattern2 = re.compile(r"""plot +([a-z\[\]'"0-9]+)""", re.IGNORECASE)
    match2 = pattern2.findall(in_string)
    result2 = [x for x in match2 if x.lower() != 'of']

    result = result1 + result2
    return result

def plot_parser(in_string):
    names = var_names_by_regex(in_string)
    if len(names)==1:
        name = names[0]
        if name in get_plotting_candidates():
            result = ["plt.plot("+name+")"]
            return result, True
        else:
            print(name, "does not seem to be a printable variable")
            return [], False
    else:
        print("Found either too few or too many potential variables", names)
        return [], False


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
        "response": "", 
        "context_set": ["has_plotted"],
        "code_command": plot_parser, },
   
    # hist
    {   "start_states": ["*"],
        "end_state": "hist",
        "patterns": ["make a histogram of x"] },

    {   "intent": "hist",
        "response": "", 
        "context_set": ["has_plotted"],},    

    # hist_with_bins
    {   "start_states": ["*"],
        "end_state": "hist_with_bins",
        "patterns": ["make a histogram of x with y bins"] },

    {   "intent": "hist_with_bins",
        "response": "", 
        "context_set": ["has_plotted"],}, 

    # add_legend
    {   "start_states": ["*"],
        "end_state": "add_legend",
        "patterns": ["add legend", "add description"] },

    {   "intent": "add_legend",
        "response": "Would you like to place the legend to the left or the right?", 
        "context_require" : ["has_plotted"],},    

    # add_legend_top_left
    {   "start_states": ["add_legend"],
        "end_state": "add_legend_top_left",
        "patterns": ["top left", ] },
    {   "start_states": ["*"],
        "end_state": "add_legend_top_left",
        "patterns": ["add legend top left", "add description top left"] },

    {   "intent": "add_legend_top_left",
        "response": "", 
        "context_require" : ["has_plotted"],
        "code_command": lambda x: (["plt.legend(['test'], loc='upper left')"],True),},    

    # add_legend_top_right
    {   "start_states": ["add_legend"],
        "end_state": "add_legend_top_right",
        "patterns": ["top right", ] },
    {   "start_states": ["*"],
        "end_state": "add_legend_top_right",
        "patterns": ["add legend top right", "add description top right"] },

    {   "intent": "add_legend_top_right",
        "response": "", 
        "context_require" : ["has_plotted"],
        "code_command": lambda x: (["plt.legend(['test'], loc='upper right')"],True),},    

    # add Styles -- this is really bad without parametrization!!
    ## start with xkcd
     {   "start_states": ["*"],
        "end_state": "xkcd_on",
        "patterns": ["draw in xkcd style", "xkcd on"] },

    {   "intent": "xkcd_on",
        "response": "", 
        "code_command": lambda x: (["plt.xkcd(scale=1, length=100, randomness=2)"],True),},    
   

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

# versuch für etwas interaktives
## some variables
x= [1,2,4,5,6]
height = [1,1,1,2,2,]
df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
nn = np.random.normal(size=(2,3))



from matplotlib import pyplot as plt
curr_state = "entry"
curr_contexts = []
all_commands = ['from matplotlib import pyplot as plt']
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

    parser = get_field_from_intent("code_command",next_state, default=lambda x: ([],True))
    new_commands, success_flag = parser(inp)
    
    if not success_flag:
        print("soory, something went wrong")
        continue

    all_commands.extend(new_commands)

    print('\n'.join(all_commands))
    [ exec(bla) for bla in all_commands ]
    plt.show()

    curr_state = next_state
    curr_contexts.extend(get_context_set_from_intent(next_state))
    print(get_response_from_intent(curr_state))
print("bye")
print('\n'.join(all_commands))

#######################################################################################################
# Future

# Change the thing to operate more on variables and fixed code blocks as follows:
# Fill somehow:
variables_to_plot = [ df['a'], df['b'], x ]
plotting_style = 'seaborn'
plotting_command = 'plot' # vs 'scatter', 'hist'

# on calling plot
plotting_code = { 
    'plot': """
with plt.style.context(plotting_style):
    for plot_var in variables_to_plot:
        plt.plot(plot_var)
""",
    'scatter': """

""",
    'hist': """
""",
    'list_files':"""
os.listdir("./testdata/")
""",

}

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