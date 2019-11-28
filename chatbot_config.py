import pandas as pd
import numpy as np
import os

def is_number(x):
    result = isinstance(x, float) or isinstance(x, int)
    return result

def all_numbers(my_list):
    return all(map(is_number, my_list))

def get_plotting_candidates(local_vars):
    candidates = []
    for n,v in local_vars.items():
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

def plot_parser(state_in, user_input, local_vars):
    names = var_names_by_regex(user_input)
    if len(names)==1:
        name = names[0]
        if name in get_plotting_candidates(local_vars):
            temp_var = local_vars[name]
            state_in['variables_to_plot'].append(temp_var)
            print("adding", name, "to the plot")
        else:
            print(name, "does not seem to be a printable variable")
    else:
        print("Found either too few or too many potential variables", names)
    exec(plotting_code['plot'], globals(), state_in)
    return state_in

def list_csv_parser(state_in, user_input, local_vars):
    try:
        state_in['csv_list'] = [ file for file in os.listdir("./testdata/") 
                                                if file.endswith(".csv")]
        print("we found the following files for you:")
        for ind, csv in enumerate(state_in['csv_list']):
            print(ind, ":", csv)
    except:
        state_in['csv_list'] = None
        print("something went wrong")
    return state_in
    
def add_legend_top_left_parser(state_in, user_input, local_vars):
    print("adding legend to the left")
    state_in['legend_location'] = "top left"
    exec(plotting_code['plot'], globals(), state_in)
    return state_in

def add_legend_top_right_parser(state_in, user_input, local_vars):
    print("adding legend to the right")
    state_in['legend_location'] = "top right"
    exec(plotting_code['plot'], globals(), state_in)
    return state_in

# on calling plot
plotting_code = { 
    'plot': """
from matplotlib import pyplot as plt
import matplotlib
plt.clf()
matplotlib.interactive(True)
with plt.style.context(plotting_style):
    for plot_var in variables_to_plot:
        plt.plot(plot_var)
    plt.show()
""",
    'scatter': """

""",
    'hist': """
""",
    'list_files':"""
[ file for file in os.listdir("./testdata/") if file.endswith(".csv") ]
""",

}

input_data_raw = [
    # entry
    # No incoming connections for "entry"
    {   "intent": "entry",
        "response": "Welcome!", },

    # list_csv
    {   "start_states": ["*"],
        "end_state": "list_csv",
        "patterns": ["list files", "list csv",] },

    {   "intent": "list_csv",
        "response": "", 
        "code_command": list_csv_parser, },

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
        "code_command": add_legend_top_left_parser,},    

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
        "code_command": add_legend_top_right_parser,},    

    # add Styles -- this is really bad without parametrization!!
    ## start with xkcd
     {   "start_states": ["*"],
        "end_state": "xkcd_on",
        "patterns": ["draw in xkcd style", "xkcd on"] },

    {   "intent": "xkcd_on",
        "response": "", 
        "code_command": lambda x: (["plt.xkcd(scale=1, length=100, randomness=2)"],True),},    
   

]
