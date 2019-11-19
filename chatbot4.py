input_data = [
    {
        "intent": "entry",
        "patterns": [],
        "responses": [],
        "code_command": lambda x: ([],True),
        "context_set": [],
        "context_require" : [],
        "context_remove": [],
        },
    {
        "intent": "plot",
        "patterns": ["make a line plot", "draw a line plot", "create a line plot", "Plot x"],
        "responses": [],
        "code_command": lambda x: ([],True),
        "context_set": ["has_plotted"],
        "context_require" : [],
        "context_remove": [],
        },
    {
        "intent": "bar",
        "patterns": ["make a bar chart", "create a bar plot", "bar plot"],
        "responses": [],
        "code_command": lambda x: (["plt.bar(x, height)"],True),
        "context_set": ["has_plotted"],
        "context_require" : [],
        "context_remove": [],
        },
    {
        "intent": "hist",
        "patterns": ["make a histogram of x"],
        "responses": [],
        "code_command": lambda x: ([],True),
        "context_set": ["has_plotted"],
        "context_require" : [],
        "context_remove": [],
        },
    {
        "intent": "hist_with_bins",
        "patterns": ["make a histogram of x with y bins"],
        "responses": [],
        "code_command": lambda x: ([],True),
        "context_set": ["has_plotted"],
        "context_require" : [],
        "context_remove": [],
        },
    {
        "intent": "add_legend",
        "patterns": ["add legend", "add description"],
        "responses": ["Would you like to place the legend to the left or the right?"],
        "code_command": lambda x: ([],True),
        "context_set": ["add_legend"],
        "context_require" : ["has_plotted"],
        "context_remove": [],
        },
    {
        "intent": "add_legend_top_right",
        "patterns": ["add legend top right", "add description top right"],
        "responses": [],
        "code_command": lambda x: (["plt.legend(['test'], loc='upper right')"],True),
        "context_set": [],
        "context_require" : ["has_plotted", "add_legend"],
        "context_remove": ["add_legend"],
        },
    {
        "intent": "add_legend_top_left",
        "patterns": ["add legend top left", "add description top left"],
        "responses": [],
        "code_command": lambda x: (["plt.legend(['test'], loc='upper left')"],True),
        "context_set": [],
        "context_require" : ["has_plotted", "add_legend"],
        "context_remove": ["add_legend"],
        },
]

pattern_to_intent = [ (pattern, x["intent"]) for x in input_data for pattern in x["patterns"] ]



def get_possible_next_states(current_state: str, current_context: dict):
    # *all* of context_require must be in current_context
    result = [ x['intent'] for x in input_data 
                            if set(x['context_require']).issubset(current_context)]
    return result


get_possible_next_states("entry", {})

get_possible_next_states("entry", {"has_plotted"})




