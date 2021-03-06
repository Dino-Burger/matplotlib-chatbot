import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from editdistance import eval as lev_dist

import spacy

try:
    spacy_model = spacy.load("spacy-model")
except:
    from spacy_model_create import save_spacy_file
    save_spacy_file()
    spacy_model = spacy.load("spacy-model")


# -------------------------
# these are all variables that are used while running the bot, very important!
all_variables = {
    'csv_list': None,
    'variables_to_plot': [ ],
    'plotting_style': 'seaborn',
    'legend_location': None,
    'plotting_command': 'plot', # vs 'scatter', 'hist'    
    'xkcd': False,
}
# -------------------------


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
            state_in['variables_to_plot'].append((name, temp_var))
            print("adding", name, "to the plot")
        else:
            print(name, "does not seem to be a printable variable")
    else:
        print("Found either too few or too many potential variables", names)
    exec(plotting_code['plot'], local_vars, state_in)
    return state_in

def list_csv_parser(state_in, user_input, local_vars):
    try:
        state_in['csv_list'] = [ file for file in os.listdir("./data/") 
                                                if file.endswith(".csv")
                                                or file.endswith(".csv.zip")][:5]
        print("we found the following files for you:")
        for ind, csv in enumerate(state_in['csv_list']):
            print(ind+1, ":", csv) # we start counting at 1.
    except:
        state_in['csv_list'] = None
        print("something went wrong")
    return state_in

def load_csv_parser(state_in, user_input, local_vars):
    if state_in['csv_list'] is None:
        print("please list the files first!")
        return state_in
    doc = spacy_model(user_input)
    variable_candidates = [ ent.text for ent in doc.ents 
                            if ent.label_ == '$ordinal' ]
    if len(variable_candidates) != 1:
        print("Sorry cannot find this file number", variable_candidates)
    else:
        file_number = variable_candidates[0]
        possible_numbers = [ ('first',0), ('second',1), ('third',2),
                                ('fourth',3), ('fifth',4),
                                ('1.',0), ('2.',1), ('3.',2), ('4.',3), ('5.',4),]
        possible_numbers_with_distance = [ (rn,lev_dist(sn,file_number)) 
                                            for sn, rn in possible_numbers ]
        rn, rn_dist = min(possible_numbers_with_distance, key=lambda x: x[1])
        if rn_dist > 3:
            print("sorry, I could not find this number", file_number)
        else:
            file_to_open = state_in['csv_list'][rn]
            print(file_to_open)
            my_plot_var = pd.read_csv("data/" + file_to_open) 
            state_in['variables_to_plot'].append(('loaded_var', my_plot_var))
    exec(plotting_code['plot'], local_vars, state_in)
    return state_in            
    
def list_variables_parser(state_in, user_input, local_vars):
    variable_names = [name for name,var in state_in['variables_to_plot']]
    print("You're currently plotting", ', '.join(variable_names))
    return state_in    

def remove_variable_parser(state_in, user_input, local_vars):
    doc = spacy_model(user_input)
    variable_candidates = [ ent.text for ent in doc.ents 
                            if ent.label_ == '$variable' ]
    if len(variable_candidates) != 1:
        print("Sorry cannot find this variable")
    else:
        del_var = variable_candidates[0]
        if del_var in [ name for name, var in state_in['variables_to_plot']]:
            state_in['variables_to_plot'] = [ (name,var) for name,var 
                                                in state_in['variables_to_plot']
                                                if name != del_var]
        else:
            print("Sorry this variable seems not to be plottet so far")
    exec(plotting_code['plot'], local_vars, state_in)
    return state_in

def add_legend_upper_left_parser(state_in, user_input, local_vars):
    print("adding legend to the left")
    state_in['legend_location'] = "upper left"
    exec(plotting_code['plot'], globals(), state_in)
    return state_in

def add_legend_upper_right_parser(state_in, user_input, local_vars):
    print("adding legend to the right")
    state_in['legend_location'] = "upper right"
    exec(plotting_code['plot'], globals(), state_in)
    return state_in

def xkcd_on_parser(state_in, user_input, local_vars):
    state_in['xkcd'] = True
    exec(plotting_code['plot'], local_vars, state_in)
    return state_in

def xkcd_off_parser(state_in, user_input, local_vars):
    state_in['xkcd'] = False
    exec(plotting_code['plot'], local_vars, state_in)
    return state_in

def style_parser(state_in, user_input, local_vars):
    doc = spacy_model(user_input)
    style_candidates = [ ent.text for ent in doc.ents if ent.label_ == '$style' ]
    if len(style_candidates) != 1:
        print("sorry, could not parse this", style_candidates)
    else:
        style_candidate = style_candidates[0]
        styles_available = plt.style.available
        styles_available_with_distance = [ (sa,lev_dist(sa,style_candidate)) 
                                            for sa in styles_available ]
        sa, sa_dist = min(styles_available_with_distance, key=lambda x: x[1])
        if sa_dist > 5:
            print("sorry, I could not find this style", style_candidate)
        else:
            state_in['plotting_style'] = sa
            print("Applying new style", sa)
    exec(plotting_code['plot'], globals(), state_in)
    return state_in

def list_styles_parser(state_in, user_input, local_vars):
    print("Available styles are:", ", ".join(plt.style.available))
    return state_in

def list_vars_parser(state_in, user_input, local_vars):
    candidates = get_plotting_candidates(local_vars)
    print("Available variables are:", ", ".join(candidates))
    return state_in


# on calling plot
plotting_code = { 
    'plot': """
import matplotlib
from matplotlib import pyplot as plt
plt.clf()
matplotlib.interactive(True)
if xkcd:
    cm = plt.xkcd()
else:
    cm = plt.style.context(plotting_style)
with cm:
    axes = []
    axes_descr = []
    for plot_var_name, plot_var in variables_to_plot:
        ax=plt.plot(plot_var, label=plot_var_name)
        axes.extend(ax)
        if isinstance(plot_var, pd.DataFrame):
            axes_descr.extend(list(plot_var.columns))
        else:
            axes_descr.append(plot_var_name)
    if legend_location:
        plt.legend(axes, axes_descr, loc=legend_location)
    plt.show()
""",
    'scatter': """

""",
    'hist': """
""",

}

graph_data_raw = [
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
        "context_set": ["csv_listed"],
        "code_command": list_csv_parser, },

    # load_csv
    {   "start_states": ["*"],
        "end_state": "load_csv",
        "patterns": ["load", "load the file"] },

    {   "intent": "load_csv",
        "response": "", 
        "code_command": load_csv_parser, 
        "context_set": ["has_plotted"],
        "context_require" : ["csv_listed"],},

    # list_variables
    {   "start_states": ["*"],
        "end_state": "list_variables",
        "patterns": ["list variables",] },

    {   "intent": "list_variables",
        "response": "", 
        "code_command": list_variables_parser, },

    # remove_variable
    {   "start_states": ["*"],
        "end_state": "remove_variable",
        "patterns": ["remove", "delete",] },

    {   "intent": "remove_variable",
        "response": "", 
        "code_command": remove_variable_parser, },

    # plot
    {   "start_states": ["*"],
        "end_state": "plot",
        "patterns": ["make a line plot", "draw a line plot", "create a line plot", "Plot x"] },

    {   "intent": "plot",
        "response": "", 
        "context_set": ["has_plotted"],
        "code_command": plot_parser, },
   
    # add_legend
    {   "start_states": ["*"],
        "end_state": "add_legend",
        "patterns": ["add legend", "add description"] },

    {   "intent": "add_legend",
        "response": "Would you like to place the legend to the left or the right?", 
        "context_require" : ["has_plotted"],},    

    # add_legend_upper_left
    {   "start_states": ["add_legend"],
        "end_state": "add_legend_upper_left",
        "patterns": ["upper left", ] },
    {   "start_states": ["*"],
        "end_state": "add_legend_upper_left",
        "patterns": ["add legend upper left", "add description upper left"] },

    {   "intent": "add_legend_upper_left",
        "response": "", 
        "context_require" : ["has_plotted"],
        "code_command": add_legend_upper_left_parser,},    

    # add_legend_upper_right
    {   "start_states": ["add_legend"],
        "end_state": "add_legend_upper_right",
        "patterns": ["upper right", ] },
    {   "start_states": ["*"],
        "end_state": "add_legend_upper_right",
        "patterns": ["add legend upper right", "add description upper right"] },

    {   "intent": "add_legend_upper_right",
        "response": "", 
        "context_require" : ["has_plotted"],
        "code_command": add_legend_upper_right_parser,},    

    # xkcd_on
    {   "start_states": ["*"],
        "end_state": "xkcd_on",
        "patterns": ["draw in xkcd style", "xkcd on", "use xkcd"] },

    {   "intent": "xkcd_on",
        "response": "", 
        "code_command": xkcd_on_parser,},    

    # xkcd_off
    {   "start_states": ["*"],
        "end_state": "xkcd_off",
        "patterns": ["turn off xkcd", "xkcd off", "no xkcd"] },

    {   "intent": "xkcd_off",
        "response": "", 
        "code_command": xkcd_off_parser,},    

    # style 
    {   "start_states": ["*"],
        "end_state": "style",
        "patterns": ["set style as", "enable style as", "change style to"] },

    {   "intent": "style",
        "response": "", 
        "code_command": style_parser,},    

    # list_styles 
    {   "start_states": ["*"],
        "end_state": "list_styles",
        "patterns": ["list styles", "show me all styles"] },

    {   "intent": "list_styles",
        "response": "", 
        "code_command": list_styles_parser,},    

    # list_vars 
    {   "start_states": ["*"],
        "end_state": "list_vars",
        "patterns": ["what data do I have", "show me all data", "show me all variables"] },

    {   "intent": "list_vars",
        "response": "", 
        "code_command": list_vars_parser,},    


]
