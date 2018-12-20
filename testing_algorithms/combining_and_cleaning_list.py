list2 = ["entry 1", "entry 2", "entry 2", "entry 3", "entry 3", "entry 2", "entry 2", "entry 2"]
list1 = ["10", "20", "30", "40", "50", "60", "70", "80"]

# result should be
# output_list2 = ["entry 1", "entry 2", "entry 3"]
# output_list1 = ["10", "20,30,60", "40,50"]

output_list2 = []
output_list1 = []
while (list2):

    element_list2 = list2.pop(0)
    str_element_to_merge = str(list1.pop(0))

    indices = [i for i,x in enumerate(list2) if x == element_list2]
    if not (indices == []):

        for _index in indices:
            list2[_index] = ''

        clean_list2 = []
        for _entry in list2:
            if not (_entry == ''):
                clean_list2.append(_entry)
        list2 = clean_list2

        list_element_to_merge = [str(list1[i]) for i in indices]

        str_element_to_merge += "," + (",".join(list_element_to_merge))

        for _index in indices:
            list1[_index] = ''

        clean_list1 = []
        for _entry in list1:
            if not (_entry == ''):
                clean_list1.append(_entry)
        list1 = clean_list1

    output_list2.append(element_list2)
    output_list1.append(str_element_to_merge)


import pprint
print("output_list2: ")
pprint.pprint(output_list2)
print("output_list1: ")
pprint.pprint(output_list1)