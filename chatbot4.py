data = [
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
        "patterns": [],
        "responses": ["Would you like to place the legend to the left or the right?"],
        "code_command": lambda x: ([],True),
        "context_set": [],
        "context_require" : ["has_plotted"],
        "context_remove": [],
        },
    {
        "intent": "add_legend_top_right",
        "patterns": [],
        "responses": [],
        "code_command": lambda x: (["plt.legend(['test'], loc='upper right')"],True),
        "context_set": [],
        "context_require" : ["has_plotted"],
        "context_remove": [],
        },
    {
        "intent": "add_legend_top_left",
        "patterns": [],
        "responses": [],
        "code_command": lambda x: (["plt.legend(['test'], loc='upper left')"],True),
        "context_set": [],
        "context_require" : ["has_plotted"],
        "context_remove": [],
        },
]











