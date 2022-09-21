import json

label_map = {
        0: 'negative',
        1: 'positive'
    }

read_file = open('incorrect_convert.json', 'r')
data = json.load(read_file)
read_file.close()

for row in data:
    if 'reg_scores' in row:
        continue

    for key in row:
        print(key, ": ", row[key])

    lst = []
    for i in range(0, len(row['tokens'])):
        print(row['tokens'][i], row['scores'][i], label_map[row['prediction']])
        ele = float(input())
        lst.append(ele)  # adding the element
    row['reg_scores'] = lst

    write_file = open('incorrect_convert.json', 'w')
    json.dump(data, write_file, ensure_ascii=False, indent=2)
    write_file.close()

