import matplotlib
import matplotlib.colors
import spacy
import random

sentences = [
    "show me all files in the current directory",
    "show me all files",
    "plot $variable",
    "remove $variable",
    "delete $variable",
    "Change the color of the markers to $color",
    "plot column $columnname from variable $variable",
    "show me all csv files",
    "load the $ordinal",
    "load the $ordinal file",
    "add a legend",
    "add a legend to the $position",
    "set style as $style", 
    "set style $style", 
    "enable style $style", 
    "change style to $style"
]

variable_train_values = {
    '$color': ['red', 'green'], #list(matplotlib.colors.CSS4_COLORS.keys()),
    '$columnname': ['a', 'b'],
    '$variable': ['df', 'dg', ],
    '$ordinal': ['first', 'second', 'third', 'fourth', 'fifth', 
                    '1.', '2.', '3.', '4.', '5.' ],
        # does spacy provide something for numbers already?
    '$position': [ 'upper left', 'upper right', 'bottom left', 'bottom right', ],
    '$style': ['dark_background', 'grayscale', 'seaborn-ticks', 'seaborn dark palette'],
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


def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  # create blank Language class
    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)

    # add labels
    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text],  # batch of texts
                    [annotations],  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    sgd=optimizer,  # callable to update weights
                    losses=losses)
            print(losses)
    return nlp


def save_spacy_file():
    train_data_raw = fill_examples_variables(sentences, variable_train_values)
    train_data_spacy = [ (sent, {'entities': var }) for sent, var in train_data_raw]

    mynlp = train_spacy(train_data_spacy, 20)
    #  relies on working directory to save in correct place
    mynlp.to_disk("test.spacy")

    test_text = "change style to ggplot"
    doc = mynlp(test_text)
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

if __name__ == '__main__':
    save_spacy_file()
