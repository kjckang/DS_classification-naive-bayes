import sys
import csv
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
import csv



with open('input5.txt', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

with open('output5.txt') as f:
    reader = csv.reader(f)
    a = list(reader)

output = []
for i in a:
    output.append(int(i[0]))

train_data = []
test_data = []


train_data = [list(map(int, i[1:])) for i in data[1:] if i[17] != '-1']
test_data = [list(map(int, i[1:])) for i in data[1:] if i[17] == '-1']

N = len(train_data)

train_label = list(zip(*train_data))[-1]
label = defaultdict(int)
py = defaultdict(float)
feature_key = OrderedDict()
feature_count = defaultdict(int)

for i in train_label:
    for j in range(1,8):
        if i == j:
            label[j] += 1
        else:
            label[j] += 0




for key, item in label.items():
    py[key] = (item+0.1)/(N + 0.1*item)

for index, item in enumerate(train_data[0]):
    if index == 12:
        feature_key[index] = list([0,2,4,5,6,8])
    elif index == 16:
        feature_key[index] = [i for i in range(1,8)]
    else:
        feature_key[index] = list([0,1])

for line in train_data:
    for (key,i) in zip(feature_key.items(),line):
        for j in key[1]:
            if j == i:
                feature_count[(key[0],j)] += 1


label_data = OrderedDict()

for lab in range(1,8):
    label_data[lab] = []
for j in train_data:
    label_data[j[-1]].append(j)


pxy_count = defaultdict(int)

for key,item in label_data.items():
    if not item:
        for idx, features in feature_key.items():
            for q in features:
                pxy_count[(key,idx,q)] = 0
    for i in item:
        for cj,j in feature_key.items():            
            for k in j:
                if i[cj] == k:                   
                    pxy_count[(key,cj,k)] += 1
                else:
                    pxy_count[(key,cj,k)] += 0
                
            
pxy = dict()

for key,item in pxy_count.items():
    c,f,q = key
    pxy[(c,f,q)] = (item+0.1)/(label[c]+len(feature_key[f])*0.1)



pred_prob = defaultdict(list)
max_l = []

for ci, i in enumerate(test_data):
    argmax_l = dict()
    for lab in label.keys():
        j = i[:-1]
        temp = 1
        for cp, p in enumerate(j):
            temp *= pxy[(lab,cp,p)]
        argmax_l[temp*py[lab]] = lab
    max_l.append(argmax_l[max(argmax_l.keys())])

diff = 0

for (i,j) in zip(max_l,output):
    print("Predicted: ", int(i)," Labels: ",int(j))
    diff = int(i) - int(j)

print("Naive Bayes Model Accuracy: ", (1-diff)*100, "%")

        
        




