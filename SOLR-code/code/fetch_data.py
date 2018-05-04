import json
import pprint
import pandas as pd
import locale
import numpy as np
from locale import atof
locale.setlocale(locale.LC_NUMERIC, '')
import random
import time
import sys
from collections import OrderedDict
import operator

def months(data):
    months_count = dict()
    time_of_day = dict()
    time_months_map = dict()
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    months_map2 = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}
    for item in data:
        date = str(item["sighted_at"]).strip()

        if date == "0000" or date == " ":
            continue
        if date != "" or date != None:

            if len(date) == 8:
                try:
                    n = int(date)  # to see if date is numeric
                    month = months_map2[int(date[-4:][:-2])]
                    if month in months_count:
                        months_count[month] += 1
                    else:
                        months_count[month] = 1
                    # print(month)

                except:
                   pass
            elif len(date) > 8:
                # print("*******EPOCH*******")
                try:
                    epoch = int(date)  # to see if date is numeric
                    if epoch > 0:
                        # print(epoch)
                        _time_ = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
                        # print(_time_)
                        list_time = _time_.split("-")
                        month = months_map2[int(list_time[1])]
                        # print(month)
                        hour = int(list_time[2].split(" ")[1].strip()[:2])
                        # print(hour)
                        # print(len(hour))
                        # a = input("ENTER: ")
                       # month = months_map2[int(date[-4:][:-2])]
                        if month in months_count:
                            months_count[month] += 1
                        else:
                            months_count[month] = 1

                        if hour > 0 and hour < 25:
                            if hour in time_of_day:
                                time_of_day[hour] += 1
                            else:
                                time_of_day[hour] = 1
                            # print(month)

                            if hour in time_months_map:
                                if month in time_months_map[hour]:
                                    time_months_map[hour][month] += 1
                                else:
                                    time_months_map[hour][month] = 1
                            else:
                                time_months_map[hour] = dict()
                                time_months_map[hour][month] = 1

                except:
                   pass
            else:

                try:
                    # print(len(date))
                    #print(date)
                    for m in months:
                        if date.lower().find(m.lower()) != -1:
                            # print(m)
                            if m in months_count:
                                months_count[m] += 1
                            else:
                                months_count[m] = 1
                            break

                except:
                    # a = input("Enter: ")
                    pass
    return months_count, time_of_day, time_months_map

def dynamic(data):
    new_dynamic = []
    for item in data:
        i = dict()
        try:
            if item["shape"] != "" and item["image-objects"] != [] and item["longitude"]!= None:
                # pprint.pprint(item)
                #a = input()
                
                i["shape"] = item["shape"]
                i["lat"] = item["latitude"]
                i["lon"] = item["longitude"]
                i["objects"] = item["image-objects"]
                i["captions"] = item["image-captions"]
                i["url"] = item["image-url"]
    f            new_dynamic.append(i)
        except:
            pass
    # pprint.pprint(new_dynamic)
    print(len(new_dynamic))
    return new_dynamic

def writeJson(data, outputfile):
    json.dump(data, open(outputfile, "w"), indent=4)


if __name__ == "__main__":

    inputfile = sys.argv[1]
    arg = sys.argv[2]
    fetched_data = json.load(open(inputfile, 'r'))
    data = fetched_data["response"]["docs"]
    if arg=="shape":
        dynamic_data = dynamic(data)
        shapes = dict()
        clean_shapes = []
        for item in dynamic_data:
            list_shapes = item["shape"].strip(",").split(" ")
            if len(list_shapes) >= 1:
                for shape in list_shapes:
                    i = dict()
                    if shape == "" or shape=="A":
                        continue
                    try:
                        i["shape"] = shape
                        i["lat"] = item["lat"]
                        i["lon"] = item["lon"]
                        i["objects"] = item["objects"]
                        i["captions"] = item["captions"]
                        i["url"] = item["url"]
                        clean_shapes.append(i)
                    except:
                        pass
        # if item["shape"] not in shapes:
        #     shapes[item["shape"]] = 1
        # else:
        #     shapes[item["shape"]] += 1
        pprint.pprint(clean_shapes)
        print(len(clean_shapes))
        #json.dump(clean_shapes, open("../data/cleaned_dynamic.json", "w"), indent=4)
        for item in clean_shapes:
            try:
                if item["shape"] not in shapes:
                    shapes[item["shape"]] = 1
                else:
                    shapes[item["shape"]] += 1
            except:
                pass
        pprint.pprint(shapes)
        print(len(shapes))
        json.dump(shapes, open("../solr-data/shapes.json", "w"), indent=4)

        sorted_shapes = OrderedDict(sorted(shapes.items(), key=operator.itemgetter(1)))
        writeJson(sorted_shapes, "../solr-data/dynamic.json")

    elif arg=="month":
        monthCount, timeCount, timeMonths = months(data)
        months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
        final = OrderedDict()
        for i in range(1,24):
            final[str(i)] = OrderedDict()
        final["total"] = OrderedDict()
        for d in timeMonths:
            result = OrderedDict(sorted(timeMonths[d].items(), key=lambda x:months.index(x[0])))
            final[d] = result
        writeJson(monthCount, "../solr-data/months.json")
        writeJson(timeCount, "../solr-data/times.json")
        writeJson(final, "../solr-data/timeMonths.json")

