import pandas as pd
import numpy as np
import matplotlib
import click

from chatbot import Chatbot


@click.command()
@click.option('--backend', 
                default=None, 
                help='Matplotlib backend. e.g. TkAgg')
def helloBot(backend):
    if backend:
        matplotlib.use(backend)
    print("Matplotlib backend is", matplotlib.get_backend())

    cb = Chatbot(locals())

    # some variables
    x= [1,2,4,5,6]
    y= [1,1,1,1,2,3,4,4,4,4,4,4,4,5]
    height = [1,1,1,2,2,]
    df = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})
    nn = np.random.normal(size=(2,3))

    cb.run()


if __name__ == '__main__':
    helloBot()