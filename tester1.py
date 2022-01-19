dicts = [
    { "name": "Tom", "age": 10 },
    { "name": "Mark", "age": 5 },
    { "name": "Pam", "age": 7 },
    { "name": "Dick", "age": 12 }
]
print(dicts)

new = [d for d in dicts if d.get('name') != 'Pam']
print(new)

print(new[0]['name'])

keys = ['Dick', 'Piet', 'Mark', 'Dave']

for key in keys:
    if key not in [d['name'] for d in dicts]:
        print(f'{key} is not in the list')