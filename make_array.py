import sys

# make line-by-line txt file to js array
# also remove duplicated data

input_file = sys.argv[1]
file_name = sys.argv[2]

f = open(f'./{input_file}')
fw = open(f'./{file_name}', 'w', encoding='utf-8')
lines = f.readlines()
fw.write('[')
input_list = []
result_list = []
for name in lines:
    input_list.append(name[:-1])
for el in input_list:
    if el not in result_list:
        result_list.append(el)
        fw.write("\'")
        fw.write(el)
        fw.write("\',")
fw.write(']')
f.close()
fw.close()
