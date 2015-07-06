# -*- coding: utf-8 -*-
import urllib2
from pyquery import PyQuery as pyq
from urlparse import urlparse


def get_url():
    __site = 'https://www.ptt.cc'
    __req_url = __site + '/bbs/Tech_Job/index.html'
    __idx= 1
    all_url = []
    while True:
        #print "this page1 = %s" % __req_url
        try:
            __response = urllib2.urlopen(__req_url, timeout=9999)
            __the_page = __response.read()
            doc = pyq(__the_page)

        except:
            continue

        doc.make_links_absolute(base_url=__site)

        for __i in doc('div.title a'):
            #print doc(__i).text()
            #print 'https://www.ptt.cc' + doc(__i).attr('href')
            all_url.append(doc(__i).attr('href'))

        __req_url = doc('.btn.wide').eq(1).attr('href')

        __idx += 1

        if __idx > 2:
            break

        if __req_url is None:
            break
    return all_url


all_link = get_url()
#print all_link
#print len(all_link)

result=[]
for __j in all_link[:3]:
    __response = urllib2.urlopen(__j, timeout=9999)
    __the_page = __response.read()
    doc = pyq(__the_page)
    post_id = urlparse(__j).path.split('/')[-1]
    dict={}
    dict['post_id']=post_id
    dict['url']=__j
    dict['text']=doc('#main-content').remove('.article-metaline').remove('.article-metaline-right').remove('.f2').text()
    result.append(dict)

print result

