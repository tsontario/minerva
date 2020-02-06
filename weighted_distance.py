# from os import path

# from pkg.context import Context
from pkg.editdistance import EditDistance

ed = EditDistance()

src = "conluter"
tgt = "computer"

d = ed.distance(src, tgt)

print(src + " --> " + tgt + " = " + str(d))