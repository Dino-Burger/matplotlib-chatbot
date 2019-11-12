# Intent classification for matplotlib
The goal is to create an intent classifier for matplotlib. It should enhance matplotlib by a function that allows to give an intent in natural lanuguage and get back the code to do the appropriate action. Examples would be "Add a legend", or "Change the color of the points to red". See more examples below.

# Goal
In a first iteration, only closed commands should be given; this also makes it easy to call it from notebooks. The (probably unreachable) goal would be that the bot is discussion enabled like below: 
- Human: Add a legend
- Bot: where would you like the legend to be? Options are top, bottom, right, left.
- Human: letf
- Bot: Sorry I did not understand this. Did you mean left?
- Human: yes
- Bot generates code.

# Questions to clarify
- Which plotting library to use? Matplotlib, plotly, plotly express? What would be good decision criteria? --> Don't know
- Just write use cases myself? Use stack overflow as inspiration? --> I guess so. 
- Basic neural network structure. I have NO clue.
- Slot Filling and Intent Detection may be modeled differently.
- M0, research, is already quite challenging. Where to start?
- M0: use a chatbot framework? do it all by hand? (I guess latter).
- Adam: Where can I learn (ML) what? How much would be hardcoded?
- Use ATIS (Airline Travel Information Systems) data set?

# Questions 2: more technical
- Can I create multiple intents from a single sentence like: "Plot x vs y, with red and blue markers, respectively"? I should get two chained intents:
    - first: plot x vs y,
    - second: make x red,
    - third: make y blue.

# Design points
- Subplots are out of scope
- Can I somehow define a dictionary of synonyms to make training less sparse? E.g. "point" == "marker".

# Potential milestones (tbd)
- M01: Research infrastructure. Output: Small written overview over existing frameworks with pros and cons.
- M02: Write training data for the intents used in M03.
- M03: Select a first simple architecture for a POC. There should be few (4-5) possible intents without parameters. These should be around line plots.
- M04: Research on how to read out a parameter with an intent, e.g. "make the markers red" has to trigger a color change event with parameter "red".
- M05: make a simple implementation of what was found in M04.
- M > 5: Open for discussion, add more intents.
- M > 10: Enable conversations.

# Examples
| Input |
|-------|
|Add a legend|
|Change the color of the points to red|
|plot variable X|
|make the markers bigger|
|Add a title|
|Change markers (color, size, etc...)|
|Add a label for the x-Axis|
|Add a label for the y-axis|
|Have more axis ticks|
|have less axis ticks|
|plot an image|
|plot an image ontop of the previous image|

# Literature
- [Building a Simple Chatbot from Scratch in Python (using NLTK)](https://medium.com/analytics-vidhya/building-a-simple-chatbot-in-python-using-nltk-7c8c8215ac6e)
- [Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling](papers/1609.01454v1.pdf)
- [Attention-Based Recurrent Neural Network Models for Joint Intent Detection and Slot Filling Webpage](https://paperswithcode.com/paper/attention-based-recurrent-neural-network)
- [Natural Language Processing with Python](http://www.nltk.org/book/)
- [Potential dataset: docstring to function](https://github.com/github/CodeSearchNet)
- [Airline Travel Information Systems data set](https://github.com/howl-anderson/ATIS_dataset)

## Less important literature
- [Many nlp datasets](https://github.com/niderhoff/nlp-datasets)

## Stuff to look at
- RasaNLU and RasaCore (on top of spacy)
- [Build a Rasa NLU Chatbot with spaCy and FastText](https://medium.com/strai/build-a-rasa-nlu-chatbot-with-spacy-with-fasttext-240e192082bd)
- [Chatterbot framework](https://spacy.io/universe/project/Chatterbot)
- [Rules of ml](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [markdown wiki](http://dynalon.github.io/mdwiki/#!index.md)

# First call with Tristan

## Given references
- [1](https://ai-guru.de/chatbots-auf-hindi/)
- [2](https://github.com/AI-Guru/stateful-conversational-agent)
- [3](https://github.com/zalandoresearch/flair)
- [4](https://github.com/zalandoresearch/flair/blob/master/resources/docs/TUTORIAL_5_DOCUMENT_EMBEDDINGS.md)
- [5](https://ai-guru.de/deep-learning-and-psychology-character-typing-reddit-bert-and-fast-ai/)
- [6](https://stackabuse.com/python-for-nlp-creating-a-rule-based-chatbot/)

## Goal