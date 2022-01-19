dicts = [
    { "name": "a", "age": 10 },
    { "name": "b", "age": 10 },
    { "name": "c", "age": 10 },
    { "name": "d", "age": 12 },
    { "name": "e", "age": 10 },
    { "name": "f", "age": 5 },
    { "name": "g", "age": 10 },
    { "name": "h", "age": 12 },
]
print(dicts)
pop_list = []
for c, d in enumerate(dicts[:]):
    if d['age'] == 10:
        dicts.pop(c)
        dicts.insert(c, {'name': d['name'], 'age': 11})
        print(c)

print(dicts)


# pop_list = []
# for c, d in enumerate(dicts, start=0):
#     if d['age'] == 11:
#         dicts.append({'name': d['name'], 'age': 0})
#         print(c)
#         pop_list.append(c)
        
# pop_list.reverse()
# for c in pop_list:
#     dicts.pop(c)
    
# print(dicts)
# print(next(x for x in dicts if x["name"] == "Pam"))

# new = [d for d in dicts if d.get('name') != 'Pam']
# print(new)

# print(new[0]['name'])

# keys = ['Dick', 'Piet', 'Mark', 'Dave']

# for key in keys:
#     if key not in [d['name'] for d in dicts]:
#         print(f'{key} is not in the list')