import pandas as pd
import numpy as np
from chatbot import Chatbot

import matplotlib
matplotlib.use('TkAgg')

cb = Chatbot(locals())

# some variables
x= [1,2,4,5,6]
y= [1,1,1,1,2,3,4,4,4,4,4,4,4,5]
height = [1,1,1,2,2,]
df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
nn = np.random.normal(size=(2,3))

cb.run()
