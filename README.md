# Matplotlib-chatbot
This is a simple chatbot to plot via matplotlib.

## Installation via git
```bash
git clone https://github.com/Dino-Burger/matplotlib-chatbot
cd matplotlib-chatbot
pip install -r requirements.txt
```

## Installation via .zip file
- Go to [https://github.com/Dino-Burger/matplotlib-chatbot/releases]
- Download the latest .zip file
- Unpack it
- Execute 
```bash
cd matplotlib-chatbot-X.X.X
pip install -r requirements.txt
```

## Remark regarding audio input
There are two packages in the requirements.txt file that are only needed to use the *experimental* audio support:
- PyAudio
- SpeechRecognition

The chatbot works without them. Remarks: 
- PyAudio might need some additional system libraries. 
- PyAudio works on my Ubuntu only with system python3, in Anaconda it seems to be broken.

If you managed to install these, you can press enter in the chatbot and as soon as the chatbot says "Say something!" you can do so.

## Run in jupyter
```python
cd matplotlib-chatbot

import pandas as pd
import numpy as np
from chatbot import Chatbot
%matplotlib inline

# some demo variables: use your own
y = [1,1,1,1,2,3,4,4,4,4,4,4,4,5]
df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
nn = np.random.normal(size=(2,3))

cb = Chatbot(locals())
cb.run()
```

## Run from command line
```bash
python chatbot_run.py
```
This starts the bot with the default matplolib backend of your system, which should be fine in most cases. I had some trouble with `GTK3Agg`, so if necessary, you can provide a specific backend:
```bash
python chatbot_run.py --backend TkAgg
```

## Things to do when the bot started

First you need to get some data. You can either use variables that are loaded, e.g. df, and just say `plot df`. Alternatively you can load data from a csv or a csv.zip file. For this to work, you need csv files in a subdirectory called `data`. Then you can first type something like `list all files` to get an enumerated list of files. Then you can load a file by typing `load 1` to load the first file.

Note that the support for pandas dataframes is experimental and that **the chatbot will crash if there are any non-numeric columns in a dataframe** (like strings or dates), coming either from a variable or a file .

After loading the data you can add a legend, or change the style, or make it an xkcd plot. You can for example say `list styles` to get a list of styles and then `set style as fast` to set the style 'fast'. 

An example conversation would be as follows:
- what data
- plot y
- list all files
- load 1
- list my variables
- remove y
- turn on xkcd
- add a legend to the left
- xkcd off
- exit
