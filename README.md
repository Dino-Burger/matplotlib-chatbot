# Matplotlib-chatbot
This is an attempt to build a simple chatbot to plot via matplotlib.

## Installation

```bash
git clone https://github.com/Dino-Burger/matplotlib-chatbot

cd matplotlib-chatbot

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