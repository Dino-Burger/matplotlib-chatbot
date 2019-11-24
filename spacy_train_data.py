import matplotlib
import matplotlib.colors

sentences = [
    "Change the color of the markers to $color",
    "plot column $columnname from variable $variable",
    "show me all csv files",
    "plot me the $ordinal",
    "add a legend",
    "add a legend to the $position",
]

variable_train_values = {
    'color': list(matplotlib.colors.CSS4_COLORS.keys()),
    'columnname': ['a', 'b'],
    'variable': ['df', 'dg', ],
    'ordinal': ['first', 'second', 'third', 'fourth', 'fifth', ],
        # does spacy provide something for numbers already?
    'position': [ 'top left', 'top right', 'bottom left', 'bottom right', ],
}



result = []
sentence = "plot column $columnname from variable $variable"
sentence_as_tokens = sentence.split()
variables_in_sentence = [(i,x) for i,x in enumerate(sentence_as_tokens) if x[0]=='$']
var_index, var_name_raw = variables_in_sentence[0]
var_name = var_name_raw[1:]

sentence_structure = { 
    'sentence_list': ['plot', 'column', '$columnname', 'from', 'variable', '$variable'],
    'replaced_tags': [],
}

import copy

def explode_single_variable(sentence_structure, var_name, var_index):
    # sentence_structure -> [ sentence_structure ]
    result = []
    for var_value in variable_train_values[var_name]:
        new_inp_val = copy.deepcopy(sentence_structure)
        new_inp_val['sentence_list'][var_index] = var_value
        new_inp_val['replaced_tags'].append((var_index, var_name))
        result.append(new_inp_val)
    return result








def blabla(string_list, found_tag_list):
    pass



#for curr_variable in variables_in_sentence:
#    start_position = sentence.find



def explode_sentences(sentences, variable_train_values):
    pass