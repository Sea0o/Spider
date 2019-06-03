import requests
import os

#爬取的url
def open_url(url):
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }

    req = requests.get(url, headers=Headers)
    html = req.text

    return html

#页面的num，如41，42等，一共10页
def get_page(url):
    html=open_url(url)

    a = html.find("current-comment-page") +23  #找到页面数，str='<span class="current-comment-page">[41]</span>'，+23刚好到了4的位置
    b = html.find("]",a)    #从a开始，找到]的索引位置

    return  html[a:b]


#找到图片地址，即img src=""
def find_img(url):
    html=open_url(url)
    c = html.find('img src=')
    image_add=[]

# 爬取一个页面内所有的图片
    while c!=-1:    #c!=-1，即页面内存在img src

        d = html.find('.jpg', c, c + 255)
        if d!=-1: #即页面内还存在.jpg
            image_add.append(html[c+9:d+4]) #将图片的地址存放到一个列表中

        c=html.find('img src=',d)#从上一次结束的位置开始查找,即上一次的d的位置

    return image_add


#保存图片
def save_img(folder,image_add):
    for each in image_add:
        #each=" //wx2.sinaimg.cn/mw600/0076BSS5ly1g342u4px23j30u018z7wh.jpg "

        req=requests.get('http:'+each)
        image_get=req.content
        filename=each.split('/')[4] #filename即为爬取图片的名字，以此命名爬取的文件
        with open(filename,'wb') as picture:
            picture.write(image_get)


def download_num(folder='ooxx',pages=10):   #创建文件夹，并抓取10页的图片

    os.mkdir(folder)
    os.chdir(folder)    #创建一个文件夹，并将爬取的图片放在此文件夹中

    url = "http://jandan.net/ooxx/"
    page_num=int(get_page(url))

    for i in range(pages):
        page_num-=i
        #http://jandan.net/ooxx/page-41#comments
        page_url=url + "page-" + str(page_num) + "#comments"

        image_add=find_img(page_url)
        save_img(folder,image_add)

if __name__=='__main__':
    download_num()



