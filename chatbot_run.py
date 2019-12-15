import pandas as pd
import numpy as np
import matplotlib

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--backend", help="Matplotlib backend. e.g. TkAgg", default=None)
args = parser.parse_args()

from chatbot import Chatbot

if args.backend:
    matplotlib.use(args.backend)
print("Matplotlib backend is", matplotlib.get_backend())


cb = Chatbot(locals())

# some variables
x= [1,2,4,5,6]
y= [1,1,1,1,2,3,4,4,4,4,4,4,4,5]
height = [1,1,1,2,2,]
df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
nn = np.random.normal(size=(2,3))

cb.run()

