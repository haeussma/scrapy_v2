from scrapy import do_something
import time
import json

if __name__ == "__main__":

    data = do_something(time.ctime())

    with open("output/out.json") as f:
        list_obj = json.load(f)

    list_obj.append(data)

    with open("output/out.json", 'w') as json_file:
        json.dump(list_obj, json_file, 
                            indent=4,  
                            separators=(',',': '))
