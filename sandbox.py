import os
import re
import random
import xml.etree.ElementTree as ET

articles_filename ='enwiki-20231001-pages-articles-multistream.xml'
articles_index_filename = 'enwiki-20231001-pages-articles-multistream-index.txt'

import os

def index_binary_search(file_path, title_part):
    with open(file_path, 'r', encoding='utf-8') as file:
        low = 0
        high = os.path.getsize(file_path)
        
        while low <= high:
            mid = (low + high) // 2
            file.seek(mid)
            
            # Consume the rest of the current line if in the middle
            if mid > 0:
                file.readline()
            
            try:
                line = file.readline().strip()
            except:
                return None

            # Safeguard against invalid format
            if len(line.split(':')) < 3:
                return None

            _, id_, title = line.split(':', 2)
            id_ = int(id_)

            if title.startswith(title_part):
                return id_
            elif title_part < title:
                high = mid - 1
            else:
                low = mid + 1

    return None


def binary_search_xml(file_path, target_id):
    with open(file_path, 'r', encoding='utf-8') as file:
        low = 0
        # file size in bytes
        max = os.path.getsize(file_path)
        high = max
        while low <= high:
            mid = (low + high) // 2
            if mid >= max:
                return None
            file.seek(mid)
            try:
                file.readline()
                line = file.readline()
            except:
                return None
            

            line = ""
            # read the next line
            while '<page>' not in line:
                #if line contains end of file character, break
                if file.tell() >= max:
                    return None           
                line = file.readline()
            page_start_idx = file.tell() - len(line)

            # move three lines down
            for i in range(3):
                line = file.readline()
            # get the id from the line
            id = int(re.search(r'<id>(\d+)</id>', line).group(1))
            if id == target_id:
                # seek to the start of the page, get all text between <page and </page>
                file.seek(page_start_idx)
                page = ""
                while '</page>' not in page:
                    page += file.readline()
                return page                   
            elif id < target_id:
                low = mid + 1
            else:
                high = mid - 1

    return None

id = index_binary_search(articles_index_filename, 'AssistiveTechnology')
print(id)
'''
# do it 10 times
for i in range(10):
    random_id = random.randint(0, 74955154)
    article = binary_search_xml(articles_filename, random_id)
    # parse the article xml into a dictionary
    if article:
        root = ET.fromstring(article)
        article = {}
        for child in root:
            article[child.tag] = child.text
    if(article):
        print("Article found for id: ", random_id, " with title: ", article['title'])
    else:
        print("No article found for id: ", random_id)
'''
