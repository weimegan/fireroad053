import json
import csv
import pandas as pd
import itertools

# json extracted from http://coursews.mit.edu/coursews/?term=2021SP

f = open('sp21classes.json')
data = json.load(f)['items']
gir = {"BIO", "CHEM", "CAL1", "CAL2", "PHY1", "PHY2"}


# filter for id, total-units, prereqs, offering, semester, hass_attribute, gir_attribute, sections
def filter_classes(data):
    class_set = set()
    output = dict()
    for d in data:
        if 'offering' in d:
            if d['offering'] == 'Y' and d['level'] == 'Undergraduate':
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
                if 'type' not in output[sec]['sections']:
                    output[sec]['sections'][d['type']] = []
                class_time = tsp(d['timeAndPlace'], d['section-of'])
                output[sec]['sections'][d['type']].append(class_time) # TODO: parse timeAndPlace
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

def tsp_eve(t, number):
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
        print(e, t, number)

    return slots

def tsp(t, number):
    if '*' in t:
        return []
    
    if 'EVE' in t:
        return tsp_eve(t, number)

    t = t.split()[0]
    slots = []
    
    try:
        for t in t.split(','):

            split = [''.join(x) for _, x in itertools.groupby(t, key=str.isalpha)]
            startendtime = split[1].split('-')

            for d in split[0]:
                if len(startendtime) > 1:
                    length = times[startendtime[1]] - times[startendtime[0]]
                else:
                    length = 2
                slots.append((days[d] + times[startendtime[0]], length))
    except Exception as e:
        print(e, t, number)

    return slots

def parse_time(s):
    s = s.split(' ')[:-1] # extract time from timeAndPlace
    if s == 'TBD':
        return ""
    else:
        return s

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

def convert_json_to_csv(filename):
    df = pd.read_json(filename)
    filename_head = filename.split('.')[0]
    df.to_csv(f'{filename_head}.csv')

