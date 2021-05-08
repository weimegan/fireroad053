import json

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
                class_time = parse_time(d['timeAndPlace'])
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

def parse_time(s):
    s = s.split(' ')[:-1] # extract time from timeAndPlace
    if s == 'TBD':
        return ""
    else:
        return s

# n (string): course number
def filter_by_course(n, data):
    output = []
    for d in data:
        course_num = d.split('.')[0]
        if course_num == n:
                output.append(data[d])
    return output

def filter_gir(data):
    output = []
    for d in data:
        if 'gir_attribute' in data[d]:
            if data[d]['gir_attribute'] in gir:
                output.append(data[d])
    return output

def filter_hass(data):
    output = []
    for d in data:
        if 'hass_attribute' in data[d]:
            if len(data[d]['hass_attribute']) > 0:
                output.append(data[d])
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