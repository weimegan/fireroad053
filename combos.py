import json
import csv
import pandas as pd
import numpy as np
import itertools

f = open('finaldata/parsedsp21_dummy.json')
data = json.load(f)

classescsv = pd.read_csv('finaldata/parsedsp21_actual_classes.csv')

#print(classescsv['id'])
indToId = dict()
for i in range(len(classescsv)):
    indToId[i] = classescsv['id'][i]
#print(indToId)

#s = np.sum(data["6.006"]["sections"]["RecitationSession"][0], axis=0)


def add_times():
    new_data = dict()
    for i in range(len(indToId)):
        c = indToId[i]
        new_data[c] = dict()
        for sec in data[c]["sections"].keys(): # section: lec, rec, lab
            new_data[c][sec] = []
            for j in range(len(data[c]["sections"][sec])): # timeslots per section
                summed_sec = np.sum(data[c]["sections"][sec][j], axis=0)
                new_data[c][sec].append(summed_sec.tolist())

    with open('finaldata/addedtimes.json', 'w') as output_file:
            json.dump(new_data, output_file)

#add_times()
f1 = open('finaldata/addedtimes.json')
added_data = json.load(f1)

#print(np.shape(added_data["8.01"]["LectureSession"]))

#a = [[[1,0],[0,1]],[[1,0]],[[1,1],[0,0]]]
def combos(a):
    ls = list(itertools.product(*a))
    lscombos = [np.sum(i, axis=0).tolist() for i in ls]
    return lscombos

def create_combo_dict():
    combo_dict = dict()
    for i in range(len(indToId)):
        c = indToId[i]
        l = []
        for sec in added_data[c].keys():
            l.append(added_data[c][sec])
        combo_dict[c] = combos(l)
    with open('finaldata/combodict.json', 'w') as output:
        json.dump(combo_dict, output)

#create_combo_dict()

f2 = open('finaldata/combodict.json')
comb_data = json.load(f2)

#print(comb_data["8.01"][0][0]) # access binary value at timeslot 0 for the 0th combo of 8.01