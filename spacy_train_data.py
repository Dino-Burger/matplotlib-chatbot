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
    '$color': ['red', 'green'], #list(matplotlib.colors.CSS4_COLORS.keys()),
    '$columnname': ['a', 'b'],
    '$variable': ['df', 'dg', ],
    '$ordinal': ['first', 'second', 'third', 'fourth', 'fifth', ],
        # does spacy provide something for numbers already?
    '$position': [ 'top left', 'top right', 'bottom left', 'bottom right', ],
}


def fill_examples_variables(sentences, variable_train_values):
    import itertools
    import copy
    import numpy as np

    tokenized_sentences = [ t.split() for t in sentences ]

    def get_vars(str_list):
        return [(i,x) for i,x in enumerate(str_list) if x[0]=='$']

    # all tokenized sentences with a tuple of all variables it contains
    tok_sent_vars = [ (t,get_vars(t)) for t in tokenized_sentences ]

    # replace the variable names (e.g. $color) in the tokenized sentence 
    # with values (e.g. red)
    exploded_sentences = []
    for tok_sent, vars_ind_val in tok_sent_vars:
        ti_vars = [ variable_train_values[ti_var] for ti_i, ti_var in vars_ind_val ]
        ti_is = [ ti_i for ti_i, ti_var in vars_ind_val ]
        for element in itertools.product(*ti_vars):
            #print(tok_sent, ti_is, element)
            new_t = copy.deepcopy(tok_sent)
            for overwrite_index, overwrite_string in zip(ti_is, element):
                new_t[overwrite_index] = overwrite_string
            exploded_sentences.append((new_t, vars_ind_val))


    # join sentences to astring together and output the indexes 
    # where each variable is sitting
    joined_sentences = []
    for tokenized_sentence, variable_list in exploded_sentences:
        # the +1 is for the spaces we insert
        token_lenghts = [ len(ts)+1 for ts in tokenized_sentence ]
        token_cum_lengths = [0,] + list(np.cumsum(token_lenghts))
        
        sentence = ' '.join(tokenized_sentence)
        # the -1 is to ignore the trailing space
        containded_tokens = [ (token_cum_lengths[var_index], 
                                token_cum_lengths[var_index+1]-1, 
                                var_name) 
                                for var_index, var_name in variable_list ]

        joined_sentences.append((sentence, containded_tokens))


    return joined_sentences



