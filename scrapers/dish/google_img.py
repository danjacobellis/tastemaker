# Origin: https://github.com/hardikvasa/google-images-download
# 

#Searching and Downloading Google Images/Image Links

#Import Libraries

import time       #Importing the time library to check the time of code execution
import sys    #Importing the System Library

########### Edit From Here ###########

#This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
search_keyword = ['godiva', 
 'grains', 
 'gravy', 
 'groundmeat', 
 'ham', 
 'hamburger', 
 'icings', 
 'jam', 
 'jello', 
 'jelly', 
 'lamb', 
 'marinade', 
 'muffins', 
 'mushrooms', 
 'mutton', 
 'nuts', 
 'pancakes', 
 'pasta', 
 'pastanoodle', 
 'pastries', 
 'peppers', 
 'pie', 
 'pizza', 
 'pork', 
 'potato', 
 'poultry', 
 'preserves', 
 'pudding', 
 'relishes', 
 'rice', 
 'roast', 
 'salad', 
 'salsa', 
 'sandwich', 
 'sausage', 
 'shrimp', 
 'soup', 
 'sourdough', 
 'steak', 
 'stew', 
 'stuffing', 
 'tofu', 
 'tomatoes', 
 'tuna', 
 'turkey', 
 'veal', 
 'venison']

# These keywords will be added to the end of each search term
keywords = [' ']

########### End of Editing ###########


#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print((str(e)))
    else:                        #If the Current Version of Python is 2.x
        import urllib.request, urllib.error, urllib.parse
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            response = urllib.request.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"


#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


############## Main Program ############
t0 = time.time()   #start the timer

import os

#Download Image Links
kw = 0
item_lists = {}
while kw < len(search_keyword):
    items = []
    iteration = "Item no.: " + str(kw+1) + " -->" + " Item name = " + str(search_keyword[kw])
    print (iteration)
    print ("Evaluating...")
    search_keywords = search_keyword[kw]
    search = search_keywords.replace(' ','%20')
    j = 0
    while j<len(keywords):
        pure_keyword = keywords[j].replace(' ','%20')
        print(str(search + pure_keyword))
        url = 'https://www.google.com/search?q=' + search + pure_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html =  (download_page(url))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        j = j + 1
    #print ("Image Links = "+str(items))
    print(("Total Image Links = "+str(len(items))))
    print ("\n")
    item_lists[search_keyword[kw]] = items
    kw = kw+1


t1 = time.time()
total_time = t1-t0
print(("Total time taken: "+str(total_time)+" Seconds"))
print ("Starting Download...")

## To save imges to the same directory
# IN this saving process we are just skipping the URL if there is any error

print(item_lists)

if not os.path.exists('google_dl'):
            os.makedirs('google_dl')

k=0
errorCount=0
for category,items in item_lists.items():
    print("Downloading category: " + category)
    if not os.path.exists('google_dl/' + category):
                os.makedirs('google_dl/' + category)
    k = 0
    while(k<len(items)):
        from urllib.request import Request, urlopen
        from urllib.error import URLError, HTTPError
        
        output_path = ''
        
        try:
            req = Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urlopen(req)
            output_path = 'google_dl/' + category + "/" + str(k+1)+".jpg"
            output_file = open('google_dl/' + category + "/" + str(k+1)+".jpg",'wb')
            data = response.read()
            output_file.write(data)
            response.close();

            print(("completed ====> "+str(k+1)))

            k=k+1;
        except:
            errorCount += 1
            print(("General error " + str(k)))
            if output_path != '':
                os.remove(output_path)
            k = k+1;
            