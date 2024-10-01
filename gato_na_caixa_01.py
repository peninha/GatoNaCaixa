import random

def cat_move(catState, boxes=5):
    if catState == 0:
        return random.randint(1, boxes)
    if catState == 1:
        return 2
    if catState == boxes:
        return catState - 1
    return catState + random.randint(-1, 0) * 2 + 1

def open_box(box, catState, boxes=5):
    return catState==box

#random.seed(42)
boxes = 5
catState = 0
runs = 10

#%% Estratégia 2, 3, 4, 4, 3, 2

strategy = [2,3,4,4,3,2]

found = 0
tries = 0
for run in range(runs):
    while found == 0:
        catState = cat_move(catState, boxes)
        found = open_box(strategy[run%len(strategy)], catState, boxes)
        if found:
            