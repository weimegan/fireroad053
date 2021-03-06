import json
import csv
import pandas as pd
import itertools
import numpy as np

# json extracted from http://coursews.mit.edu/coursews/?term=2021SP

f = open('sp21classes.json')
data = json.load(f)['items']

f20 = open('f20classes.json')
dataf20 = json.load(f20)['items']

gir = {"BIO", "CHEM", "CAL1", "CAL2", "PHY1", "PHY2", "BIO"}
gir_to_course = {
    'GIR:CAL1': 'Calculus I (GIR)',
    'GIR:CAL2': 'Calculus II (GIR)',
    'GIR:PHY1': 'Physics I (GIR)',
    'GIR:PHY2': 'Physics II (GIR)',
    'GIR:CHEM': 'Chemistry (GIR)',
    'GIR:BIOL': 'Biology (GIR)',
}

# extract essential F20 classes
essentialf20 = {'5.13', '15.780', '15.312', '5.07', '8.01'}
def extract_f20():
    f20c = filter_classes(dataf20)
    f20d = dict()
    for c in essentialf20:
        f20d[c] = f20c[c]
    return f20d

# filter for id, total-units, prereqs, offering, semester, hass_attribute, gir_attribute, sections
def filter_classes(data, timearr=True):
    class_set = set()
    output = dict()
    for d in data:
        if 'offering' in d:
            if d['offering'] == 'Y':
                new_dict = parse_class(d)
                class_set.add(d['id'])
                output[d['id']] = new_dict

    for d in data:
        if 'section-of' in d:
            sec = d['section-of']
            if sec in class_set:
                if 'sections' not in output[sec]:
                    output[sec]['sections'] = dict()
                # create dictionary of recitation : time(s) / lab : time(s) / lecture : time(s)
                if d['type'] not in output[sec]['sections']:
                    output[sec]['sections'][d['type']] = []
                class_time = parse_time(d['timeAndPlace'], d['section-of'])
                if timearr:
                    class_vec = convert_time_to_vector(class_time)
                    output[sec]['sections'][d['type']].append(class_vec)
                else:
                    output[sec]['sections'][d['type']].append(class_time)
    return output

def parse_class(class_dict):
    d = dict()
    d['id'] = class_dict['id']
    d['total-units'] = class_dict['total-units']
    d['prereqs'] = class_dict['prereqs']
    d['semester'] = class_dict['semester']
    d['hass_attribute'] = class_dict['hass_attribute']
    d['gir_attribute'] = class_dict['gir_attribute']
    return d

# parse prereqs
def parse_prereq(prereq):
    if len(prereq) == 0:
        return []
    permission = 'permission of instructor' 
    if permission in prereq:
        prereq = prereq.replace(permission, '')
    pass

# parse time
def convert_time_to_vector(class_time):

    if len(class_time) > 0:
        vecs = []
        for time in class_time:
            vec = np.zeros(150)
            vec[time[0]:time[0]+time[1]] = 1
            vecs.append(vec.tolist())
        return vecs
    else:
        return np.zeros(150).tolist()

timeslots = 30
days = {'M': 0,
        'T': timeslots,
        'W': timeslots * 2,
        'R': timeslots * 3,
        'F': timeslots * 4}
times = {'8': 0,
         '8.30': 1,
         '9': 2,
         '9.30': 3,
         '10': 4,
         '10.30': 5,
         '11': 6,
         '11.30': 7,
         '12': 8,
         '12.30': 9,
         '1': 10,
         '1.30': 11,
         '2': 12,
         '2.30': 13,
         '3': 14,
         '3.30': 15,
         '4': 16,
         '4.30': 17,
         '5': 18,
         '5.30': 19,
         '6': 20,
         '6.30': 21,
         '7': 22,
         '7.30': 23}

eve_times = {'1': 10,
             '1.30': 11,
             '2': 12,
             '2.30': 13,
             '3': 14,
             '3.30': 15,
             '4': 16,
             '4.30': 17,
             '5': 18,
             '5.30': 19,
             '6': 20,
             '6.30': 21,
             '7': 22,
             '7.30': 23,
             '8': 24,
             '8.30': 25,
             '9': 26,
             '9.30': 27,
             '10': 28,
             '10.30': 29}

def parse_time_eve(t, number):
    wdays = t.split()[0]
    t = t[t.find("(")+1:t.find(")")].rstrip(' PM')
    
    slots = []
    startendtime = t.split('-')
    try:
        for d in wdays:
            if len(startendtime) > 1:
                length = eve_times[startendtime[1]] - times[startendtime[0]]
            else:
                length = 2
            slots.append((days[d] + eve_times[startendtime[0]], length))
    except Exception as e:
        #print(e, t, number)
        return [] #skipping the few classes that have weird grammar
    return slots

def parse_time(time, number):
    if '*' in time or 'TBD' in time or 'TBA' in time or 'null' in time or 'Scheduled' in time: 
        return []
    
    if 'EVE' in time:
        return parse_time_eve(time, number)

    time = time.split()[0]
    slots = []
    
    try:
        for t in time.split(','):

            split = [''.join(x) for _, x in itertools.groupby(t, key=str.isalpha)]
            startendtime = split[1].split('-')

            for d in split[0]:
                if len(startendtime) > 1:
                    length = times[startendtime[1]] - times[startendtime[0]]
                else:
                    length = 2
                slots.append((days[d] + times[startendtime[0]], length))
    except Exception as e:
        #print(e, time, number)
        return [] #skipping classes with weird grammar

    return slots

# n (string): course number
def filter_by_course(n, data):
    output = dict()
    for d in data:
        course_num = d.split('.')[0]
        if course_num == n:
                output[d] = data[d]
    return output

def filter_gir(data):
    output = dict()
    for d in data:
        if 'gir_attribute' in data[d]:
            if data[d]['gir_attribute'] in gir:
                output[d] = data[d]
    return output

def filter_hass(data):
    output = dict()
    for d in data:
        if 'hass_attribute' in data[d]:
            if len(data[d]['hass_attribute']) > 0:
                output[d] = data[d]
    return output

def write_json_parsed():
    new_dict = filter_classes(data)
    with open('data/parsedsp21.json', 'w') as output_file:
        json.dump(new_dict, output_file)

# n (string): course number
def write_json_parsed_course(n):
    d = filter_classes(data)
    new_dict = filter_by_course(n, d)
    with open(f'data/parsedsp21_{n}.json', 'w') as output_file:
        json.dump(new_dict, output_file)

def write_json_parsed_gir():
    d = filter_classes(data)
    new_dict = filter_gir(d)
    with open('data/parsedsp21_gir.json', 'w') as output_file:
        json.dump(new_dict, output_file)

def write_json_parsed_hass():
    d = filter_classes(data)
    new_dict = filter_hass(d)
    with open('data/parsedsp21_hass.json', 'w') as output_file:
        json.dump(new_dict, output_file)

#write_json_parsed()
#write_json_parsed_course("15")
#write_json_parsed_course("6")
#write_json_parsed_course("5")
#write_json_parsed_gir()
#write_json_parsed_hass()

def convert_json_to_csv(filename, ordered_like_class_list=False):
    df = pd.read_json(filename)
    df = df.T
    filename_head = filename.split('.')[0]
    if ordered_like_class_list:
        df1 = pd.DataFrame()
        with open('Class_List.csv') as f:
            classes = list(csv.reader(f))
            classes = [c[0] for c in classes]
            for c in classes:
                df1 = df1.append(df.loc[c])
        df = df1

    df.to_csv(f'{filename_head}.csv')

#convert_json_to_csv('data/parsedsp21_gir.json')
#convert_json_to_csv('data/parsedsp21_hass.json')
#convert_json_to_csv('data/parsedsp21_15.json')
#convert_json_to_csv('data/parsedsp21_5.json')
#convert_json_to_csv('data/parsedsp21_6.json')
#convert_json_to_csv('data/parsedsp21.json')

# ACTUAL CLASSES
def filter_actual_classes(classes, data):
    output = dict()
    for d in data:
        if d in classes:
            output[d] = data[d]
    f20classes = extract_f20()
    output.update(f20classes)
    return output

def write_json_parsed_final(path):
    with open('Class_List.csv') as f:
        classes = list(csv.reader(f))
        classes = [c[0] for c in classes]
        d = filter_classes(data)
        new_dict = filter_actual_classes(classes, d)
        with open(path, 'w') as output_file:
            json.dump(new_dict, output_file)
#write_json_parsed_final('finaldata/parsedsp21_actual_classes.json')
#write_json_parsed_final('finaldata/parsedsp21_dummy.json')
#convert_json_to_csv('finaldata/parsedsp21_actual_classes.json', True)
#convert_json_to_csv('finaldata/parsedsp21_dummy.json', True)

def replace_column(in_csv, out_csv):
    df_in = pd.read_csv(in_csv)
    df_out = pd.read_csv(out_csv)
    for i in range(len(df_out)):
        df_out.loc[i, 'sections'] = df_in.loc[i, 'sections']
    df_out.to_csv('finaldata/parsedclasses.csv', index=False)

#replace_column('finaldata/parsedsp21_dummy.csv', 'finaldata/parsedsp21_actual_classes.csv')
#check missing data from f20
"""
fi = open('finaldata/parsedsp21_actual_classes.json')
datas = json.load(fi)
k = set(datas.keys())
with open('Class_List.csv') as f:
        classes = list(csv.reader(f))
        cl = [c[0] for c in classes]
        cl = set(cl)
        print(cl-k)
"""

def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
      
    #read csv file
    with open(csvFilePath, encoding='utf-8') as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader: 
            #add this python dict to json array
            jsonArray.append(row)
  
    #convert python jsonArray to JSON String and write to file
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(jsonArray, indent=4)
        jsonf.write(jsonString)

#csv_to_json('finaldata/students_data.csv', 'finaldata/students_data.json')

#csv_to_json('finaldata/parsedclasses.csv', 'finaldata/parsedclasses.json')
