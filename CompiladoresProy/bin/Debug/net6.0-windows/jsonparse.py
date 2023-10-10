import json
import nltk
from nltk.tree import Tree


def transform_json(tree):
    tree_json=validation_tree(tree)
    path="tree.json"
    with open(path,"w") as arch:
        json.dump(tree_json,arch)


def struct_tree(tree):
    r={}
    r['name']=tree.label()
    r['children']=[]

    for subtree in tree:
        if isinstance(subtree,nltk.Tree):
            child=validation_tree(subtree)
            r['children'].append(child)
        else:
            l={'name':subtree}
            r['children'].append(l)
    return r


def validation_tree(tree):
    r={}
    r['name']=tree.label()
    if isinstance(tree,nltk.Tree) and len(tree)>0:
        r['children']=[]

        for subtree in tree:
            if isinstance(subtree,nltk.Tree):
                child=validation_tree(subtree)
                r['children'].append(child)
            else:
                l={'name': subtree}
                r['children'].append(l)
    else:
        r['children']=[]
    return r
    


