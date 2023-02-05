import requests
import json
import time

def run(JsonApiKey, EngineID, query):
    url = "https://www.googleapis.com/customsearch/v1?key=" + JsonApiKey + "&cx=" + EngineID + "&q=" + query
    response = requests.get(url)
    GoogleResults = json.loads(response.text)['items']

    # STORE THE REQUIRED INFORMATION AS A LIST OF MAP
    i = 1
    res = []
    print("Google Search Results: ")
    print("======================")
    for entry in GoogleResults:
        title, link, website, snippet = "", "", "", "--(empty)--"
        if 'title' in entry.keys ():
            title = entry['title']
        if 'link' in entry.keys():
            link = entry['link']
        if 'snippet' in entry.keys():
            snippet = entry['snippet']
        entry = {"title": title, "link": link, "snippet": snippet, "relevance": False}
        res.append(entry)
    for entry in res:
        print("RESULT " + str(i))
        print("[")
        i += 1
        print("URL: " + entry['link'])
        print("Title: " + entry['title'])
        print("Summary: " + entry['snippet'])
        print("]")
        print("Relevant (Y/N)? ")
        check = input()
        print()
        if check == 'Y' or check == 'y':
            entry ['relevance'] = True
        else:
            entry ['relevance'] = False
    return res

def calculate(res):
    #calculates precision@10
    #returns precision
    count = 0.0
    for entry in res:
        if entry['relevance'] == True:
            count += 1
    return count/10

def main():
    JsonApiKey, EngineID = "AIzaSyDI07bUpnPo2QrQaNRza54wYpz3BlldbRY", "e6d037c2c6089967e"
    print("ENTER THE SEARCH QUERY: ")
    query = input()
    print("ENTER THE Precision: ")
    precision = float(input())
    print()
    time.sleep(1)
    currentPrecision = 0.0
    while currentPrecision < precision:
        res = run(JsonApiKey, EngineID, query)
        currentPrecision = float(calculate(res))
        if currentPrecision == 0.0:
            print("NO RELEVANT DOCUMENT FOUND TO EXPAND THE QUERY WITH")
            exit()
        print("Current Precision: ",currentPrecision)
        exit()
        #TODO


if __name__ == '__main__':
    main()