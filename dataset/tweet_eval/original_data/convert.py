import sys

split = sys.argv[1]

mapping = {
    '0':	'negative',
    '1':	'neutral',
    '2':	'positive'
}

skip_label = set(['1'])

label_file = open("./%s_labels.txt" % split, "r")
text_file = open("./%s_text.txt" % split, "r")

out_file = open("../%s.tsv" % split, "w")

for text, label in zip(text_file, label_file):
    label = label.strip("\n")
    if label in skip_label:
        continue
    out_file.write(text.strip("\n") + "\t" + mapping[label] + "\n")

label_file.close()
text_file.close()
out_file.close()
