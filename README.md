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

## Load data in chatbot
You can load a pandas dataframe from within the chatbot. For this to work, you need csv files in a subdirectory called `data`. Note that this is a very experimental feature and the chatbot will crash if there are any non-numeric columns in a file (like strings or dates).
