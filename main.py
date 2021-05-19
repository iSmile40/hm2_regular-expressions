import re
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)

for line in contacts_list:

  if len(line[0].split(' ')) == 3:
    for i in reversed(range(3)):
      line[i] = re.findall(r'\w+', line[0])[i]

  if len(line[0].split(' ')) == 2:
    for i in reversed(range(2)):
      line[i] = re.findall(r'\w+', line[0])[i]

  if len(line[1].split(' ')) == 2:
    for i in reversed(range(1, 3)):
      line[i] = re.findall(r'\w+', line[1])[i-1]

  pattern = re.compile(r'([+][7]|8)?\s*-*\s*\(*\s*(\d{1,5})\s*\)*\s*-*\s*(\d{1,3})\s*-*\s*(\d{1,3})\s*-*\s*(\d{1,3})'
                       r'\s*\(?\s*[д.|доб.]*\s*(\d*)\s*\)?\s*')
  result = re.match(pattern, line[5])
  if result:
    tel = ''.join(result.groups()[1:5])
    tel = '{}({}){}-{}-{}{}'.format('+7', tel[:3], tel[3:6], tel[6:8], tel[8:],
                                    f' доб.{result.group(6)}' if result.group(6) else '')
    line[5] = tel

persons = []
contacts = []
for line in contacts_list:
    person = f'{line[0]} {line[1]}'
    if person not in persons:
      persons.append(person)
      contacts.append([])
      for i in range(7):
        contacts[persons.index(person)].append(line[i])
    else:
      for i in range(7):
        if contacts[persons.index(person)][i] == '':
          contacts[persons.index(person)][i] = line[i]

with open("phonebook.csv", "w", newline="", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(contacts)
