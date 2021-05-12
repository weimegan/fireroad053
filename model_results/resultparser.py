import csv
import numpy as np

with open('model_results/results_stud1.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

with open('Class_List.csv', newline='') as csvfile2:
    data2 = list(csv.reader(csvfile2))

results = np.array(data[1:])
classes = np.array(data2)

S,T = np.shape(results)

for t in range(T):
    sem_classes = []
    for s in range(S):
        if results[s, t] == "1.0":
            sem_classes.append(s)
    class_names = []
    for s in sem_classes:
        class_names.append(classes[s,0])
    print("for semester", t+1, "the student takes classes:", class_names)


