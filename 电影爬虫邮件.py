import requests,csv,random,smtplib,schedule,time
from bs4 import BeautifulSoup
from urllib.request import quote
from email.mime.text import MIMEText
from email.header import Header

def get_movielist():
    csv_file=open('movieTop.csv', 'w', newline='',encoding='utf-8')
    writer = csv.writer(csv_file)
    for x in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(x*25) + '&filter='
        res = requests.get(url)
        bs = BeautifulSoup(res.text, 'html.parser')
        bs = bs.find('ol', class_="grid_view")
        for titles in bs.find_all('li'):
            title = titles.find('span', class_="title").text
            list1 = [title]
            writer.writerow(list1)
    csv_file.close()

def get_randommovie():
    movielist=[]
    csv_file=open('movieTop.csv','r',newline='',encoding='utf-8')
    reader=csv.reader(csv_file)
    for row in reader:
        movielist.append(row[0])
    three_movies=random.sample(movielist,3)
    contents=''
    for movie in three_movies:
        gbkmovie = movie.encode('gbk')
        urlsearch = 'http://s.ygdy8.com/plus/s0.php?typeid=1&keyword='+quote(gbkmovie)
        res = requests.get(urlsearch)
        res.encoding='gbk'
        soup_movie = BeautifulSoup(res.text,'html.parser')
        urlpart=soup_movie.find(class_="co_content8").find_all('table')
        if urlpart:
            urlpart=urlpart[0].find('a')['href']
            urlmovie='https://www.ygdy8.com/'+urlpart
            res1=requests.get(urlmovie)
            res1.encoding='gbk'
            soup_movie1=BeautifulSoup(res1.text,'html.parser')
            urldownload=soup_movie1.find('div',id="Zoom").find('span').find('table').find('a')['href']
            content=movie+'\n'+urldownload+'\n\n'
            print(content)
            contents=contents+content
        else:
            content='没有'+movie+'的下载链接'
            print(content)
    return contents

def send_movielink(contents):
    mailhost='smtp.qq.com'
    qqmail = smtplib.SMTP()
    qqmail.connect(mailhost,25)
    account = '×××××××××@qq.com' # 因为是自己发给自己，所以邮箱账号、密码都可以提前设置好，当然，也可以发给别人啦
    password = '×××××××××××××××' # 因为是自己发给自己，所以邮箱账号、密码都可以提前设置好，当然，也可以发给别人啦。
    qqmail.login(account,password)
    receiver='×××××××××@qq.com'  # 因为是自己发给自己，所以邮箱账号、密码都可以提前设置好，当然，也可以发给别人啦。
    message = MIMEText(contents, 'plain', 'utf-8')
    subject = '电影链接'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        qqmail.sendmail(account, receiver, message.as_string())
        print ('邮件发送成功')
    except:
        print ('邮件发送失败')
    qqmail.quit()

def job():
    get_movielist()
    contents=get_randommovie()
    send_movielink(contents)

schedule.every().friday.at("18:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)