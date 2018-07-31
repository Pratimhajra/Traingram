def stn_name_to_stn_code(stnName):
    """Returns station code (stnCode) for a given Station Name"""
    stnName = stnName.upper()
    with open("stnCodeswithStnNames.txt", "r", encoding='utf8') as f:
        data_stream = f.read()
        list_of_elems = []
        # Load every comma separated string into list
        for elem in data_stream.strip(';').split(','):
            list_of_elems.append(elem)
        #print(len(list_of_elems))
        # Remove unicode string items
        #list_of_elems = [list_of_elems.remove(elem) for elem in list_of_elems if len(elem) != len(elem.encode())]
        for elem in list_of_elems:
            if len(elem) != len(elem.encode()):
                list_of_elems.remove(elem)
        #print(list_of_elems)
        #list_of_elems = [x for x in list_of_elems if not isinstance(x, float)]
        while '' in list_of_elems:
            list_of_elems.remove('')
        #print(list_of_elems)
        for elem in list_of_elems:
            if elem.isdigit():
                list_of_elems.remove(elem)
        
        #print(len(list_of_elems))
        #for elem in list_of_elems:


            #stnName_index = list_of_elems.index(stnName)
            #stnCode = list_of_elems[stnName_index-1]
            #print(stnCode)

if __name__ == '__main__':
    stn_name_to_stn_code("Mumbai Central L")
