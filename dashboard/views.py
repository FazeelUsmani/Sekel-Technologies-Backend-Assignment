from django.shortcuts import render

# Create your views here.

import requests
import json


def display(request):
   
    url = "http://www.mocky.io/v2/5d403d913300003a209d2ad3"
    # dummyurl = "https://run.mocky.io/v3/cf6835dc-7d21-4cd7-add0-45b7221ebf43"
    response = requests.get(url)

    json_response = response.json()

    json_response_list = json_response.split(",")

    data = json_response_list

    name_latestMessage = {}  # dictionary: name --> latestMessage
    name_messageCount = {}   # dictionary: name --> messageCount

    for record in data:

        name_message = record.split(":")       
        
        name = name_message[0]
        message = name_message[1]

        name = name.lstrip()
        name = name.rstrip()       

        name_latestMessage[name] = message
        name_messageCount[name] = name_messageCount.get(name, 0) + 1


    # Implementing min heap    Time Complexity: O(N log K)
    # min heap format: [count, name]
    from heapq import heapify, heappush, heappop

    heap = []
    heapify(heap)

    cnt = 0

    for name in name_messageCount:        
        if (cnt >= 5):
            if (heap[0][0] < name_messageCount[name]):
                ele = heappop(heap)
                heappush(heap, [name_messageCount[name], name])       
            
        else:        
            heappush(heap, [name_messageCount[name], name])
            cnt += 1


    allData = []
    # popping out all elements from heap and adding to a list
    while heap:
        ele = heappop(heap)
        print(ele)
        currDict = {}
        currDict["name"] = ele[1]
        currDict["messageCount"] = ele[0]
        currDict["latestMessage"] = name_latestMessage[ele[1]]
        allData.append(currDict)
    
    # reversing the list to print elements in descending order
    allData = allData[::-1]    
        
    context = {'data': allData}
    
    return render(request, 'display.html', context)
