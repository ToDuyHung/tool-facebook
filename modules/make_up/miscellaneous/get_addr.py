from math import sin, cos, sqrt, atan2, radians, asin
import time
import re
import timeout_decorator
TAG_URL = 'http://35.240.240.251/api/v1/real-estate-extraction'
GMAP_URL = 'https://maps.googleapis.com/maps/api/geocode/json?&address='
GMAP_KEY = 'AIzaSyARFbwnqTzxsfWosJ6fTyEDKeMriFiAlIY'
E_RAD = 6378.1
time_out = 60
def getDistance(p0, p1):
    (lat1, lon1) = p0
    (lat2, lon2) = p1
    rad_lat1 = radians(lat1)
    rad_lon1 = radians(lon1)
    rad_lat2 = radians(lat2)
    rad_lon2 = radians(lon2)
    def haversin(x):
        return sin(x/2)**2 
    return E_RAD* 2 * asin(sqrt(
      haversin(rad_lat2-rad_lat1) +
      cos(rad_lat1) * cos(rad_lat2) * haversin(rad_lon2-rad_lon1)))

def add_street_num_to_addr(prev_tag):
    print("\n --- prev_tag:{} --- \n".format(prev_tag))
    reg = '\s(\/|-)\s'
    second_has_num = False
    last_has_num = False
    regged_str = re.sub(reg, r'\1', prev_tag)
    list_str = regged_str.split()
    if len(list_str) < 2:
        for i in list_str[-1]:
            if i.isdigit():
                last_has_num = True
            if i=='m':
                last_has_num = False
                break

    else:
        for i in list_str[-1]:
            if i.isdigit():
                last_has_num = True
            if i=='m':
                last_has_num = False
                break  
        for i in list_str[-2]:
            if i.isdigit():
                second_has_num = True

        
    if second_has_num:
        return list_str[-2]+' '+list_str[-1]
    if last_has_num:
        return list_str[-1]
    return ''

@timeout_decorator.timeout(time_out, timeout_exception=StopIteration)
def updateTagsCollection(collection_dest, data):
    list_messages = list(map(lambda x: x['message'], data))
    
    list_tags = getTags(list_messages)
    tag_post = []
    for index1, tag in enumerate(list_tags):
        valid_tag = data[index1]
        for index2, c in enumerate(tag['tags']):
            cc = 2
            if c['type'] == 'addr_street':
                num_str = add_street_num_to_addr(tag['tags'][index2 - 1]['content'])
                if num_str:
                    tag['tags'].append({'type': 'num_street', 'content': num_str})
                # c['content'] = num_str + c['content']
            if c['type']!='normal':
                valid_tag['attr_'+c['type']] = c['content']

        
        tag_post.append(valid_tag)
    print('start insert')
    try:
        collection_dest.insert_many(tag_post, ordered= False)
    except Exception as es:
        print('error at insert', es)
        pass


def batchUpdateTags(colleciton_source, collection_dest, batch_size):
    cursor_source = colleciton_source.find()
    batch_sz = batch_size
    total = 0
    data = []
    batch_count = 0
    message_field = 'description'
    post_id = 'url'
    for doc in cursor_source:
        
        if total>batch_sz:
            print(batch_count)
            try:
                updateTagsCollection(collection_dest, data)
            except StopIteration as es:
                print(es)
                pass
            total = 0
            batch_count+=1
            data = []
        try:
            data.append({'post_id_mongo': doc['_id'], 'post_id': doc[post_id], 'message': doc[message_field]})
        except Exception as es:
            print(es)
            pass
        total+=1
    
    
    return 1