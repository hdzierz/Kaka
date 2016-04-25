from django.shortcuts import render
from mongcore.http_data_download_response import *
from mongcore.connectors import *
from .models import *



def add_item(lst, item, value):
    try:
        lst[item] = value
        return lst
    except KeyError:
        return False


def build_tree():
    trees = Tree.objects.all()
    tree = {}

    for t in trees:
        if not t.Level_1 in tree:
            tree[t.Level_1] = {}

        if t.Level_2 and not t.Level_2 in tree[t.Level_1]:
            tree[t.Level_1][t.Level_2] = {}

        if t.Level_3 and not t.Level_3 in tree[t.Level_1][t.Level_2]:
            tree[t.Level_1][t.Level_2][t.Level_3] = {}

        if t.Level_4 and not t.Level_4 in tree[t.Level_1][t.Level_2][t.Level_3]:
            tree[t.Level_1][t.Level_2][t.Level_3][t.Level_4] = {}

        if t.Level_5 and not t.Level_5 in tree[t.Level_1][t.Level_2][t.Level_3][t.Level_4]:
            tree[t.Level_1][t.Level_2][t.Level_3][t.Level_4][t.Level_5] = {}

    return tree


def page_seafood(request):
    tree = build_tree()
    

    return render(request, "page_seafood.html", {"tree": tree, })

    
