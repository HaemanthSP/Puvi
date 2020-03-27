import spacy
import networkx as nx
import io
from networkx_viewer import Viewer


def plot(input_graph):
    app = Viewer(input_graph)
    app.mainloop()


# Read the story form file
with io.open('clever_thief.txt', 'r', encoding='utf8') as ip_file:
    story = ip_file.read()

# Initialize a graph
g_story = nx.Graph()


# Simple pronoun resolution

# Get triplets from the story
nlp = spacy.load('en_core_web_sm')
story_obj = nlp(story)
for sent in story_obj.sents:
    subs, verb, objs = [], '', []
    for word in sent:
        if word.dep_ == 'nsubj':
            subs.append(word.text)
        if word.dep_ == 'ROOT':
            verb = word.text
        if word.dep_ in ['dobj', 'attr', 'acomp']:
            objs.append(word.text)
    print('S/V/O:', subs, verb, objs)
    if subs and verb and objs:
        for subj in subs:
            for obj in objs:
                g_story.add_edge(subj, obj, relation=verb)
print(g_story.edges(data=True))

question = ''
while question != str('exit'):
    question = str(input())
    ques_obj = nlp(question)
    for sent in ques_obj.sents:
        subs, verb, objs = [], '', []
        for word in sent:
            if word.dep_ == 'nsubj':
                subs.append(word.text)
            if word.dep_ == 'ROOT':
                verb = word.text
            if word.dep_ in ['dobj', 'attr', 'acomp']:
                objs.append(word.text)
        print('S/V/O:', subs, verb, objs)
        q = objs + subs
        print(g_story.edges(q[0], data=True))
