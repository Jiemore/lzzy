#lzzy3x 支持Python3.x的校园访问模块
import urllib
from urllib import request
import http.cookiejar
from bs4 import BeautifulSoup

class lzzy():
    def __init__(self,filename,account,password):
        #储存Cookie
        cookie = http.cookiejar.MozillaCookieJar(filename)
        self.opener = urllib.request.build_opener(request.HTTPCookieProcessor(cookie))
        #设置请求头，模拟浏览器访问
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0')]
        self.get_connect_login(account,password)
        cookie.save(ignore_discard=True, ignore_expires=True)
        
    def get_connect_login(self,account,password):
        loginUrl = 'http://jw.lzzy.net/st/login.aspx'
        post_data = {
                        "__VIEWSTATE":"/wEPDwUJOTYxNDY3OTc0D2QWAgIBD2QWAgIHDxBkDxYBAgEWAQUJ6L6F5a+85ZGYZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFDUJ1dHRvbl/nmbvpmYY5+nSLBhHqz30JO3nWw0VfDqWktA==",
                        "__EVENTVALIDATION":"/wEWCQLeuKaSDQLep8vjCAKu8uE5AvKm2soEAvLJzeAMAvWZ8TkC6fHPnw8CwsjN4QICyKiipgEA9oXb2ioPAMKqh7by35bI/EDoHg==",
                        "txt_卡学号":"",
                        "txt_密码":"",
                        "Button_登陆.x":"72",
                        "Button_登陆.y":"35",
                        "Rad_角色":"学生"
                } 
        post_data["txt_卡学号"] = account
        post_data["txt_密码"] = password
        self.opener.open(loginUrl,urllib.parse.urlencode(post_data).encode(encoding='UTF8'))

    def get_connect_url(self,gradeUrl,fcode):
        result = self.opener.open(gradeUrl)
        return result.read().decode(fcode)


    def get_timeTable_lastWeek(self):
        timeTable_url='http://jw.lzzy.net/st/student/st_p.aspx'
        result = self.opener.open(timeTable_url)
        soup = BeautifulSoup(result,"html5lib")
        post_data = {
			"__EVENTTARGET":"LinkButton_上一周",
			"__VIEWSTATE":soup.find('input',id='__VIEWSTATE')['value'],
			"__VIEWSTATEGENERATOR":soup.find('input',id='__VIEWSTATEGENERATOR')['value'],
			"__EVENTVALIDATION":soup.find('input',id='__EVENTVALIDATION')['value'],
			"cbo_学年学期":"2018-2019学年第二学期"
}
        return self.opener.open(timeTable_url,urllib.parse.urlencode(post_data).encode(encoding='UTF8')).read().decode('UTF8')


    def get_timeTable_nextWeek(self):
        timeTable_url='http://jw.lzzy.net/st/student/st_p.aspx'
        result = self.opener.open(timeTable_url)
        soup = BeautifulSoup(result,"html5lib")
        post_data = {
                        "__EVENTTARGET":"LinkButton_下一周",
                        "__VIEWSTATE":soup.find('input',id='__VIEWSTATE')['value'],
                        "__VIEWSTATEGENERATOR":soup.find('input',id='__VIEWSTATEGENERATOR')['value'],
                        "__EVENTVALIDATION":soup.find('input',id='__EVENTVALIDATION')['value'],
                        "cbo_学年学期":"2018-2019学年第二学期"
}
        return self.opener.open(timeTable_url,urllib.parse.urlencode(post_data).encode(encoding='UTF8')).read().decode('UTF8')


    def get_timeTable_ToWeek(self,week):
        timeTable_url='http://jw.lzzy.net/st/student/st_p.aspx'
        result = self.opener.open(timeTable_url)
        soup = BeautifulSoup(result,"html5lib")

        nowWeek = int(soup.find(id='lbl_b_周次').get_text())

        if(week == nowWeek):
            result.read().decode('UTF8')
        if(week > nowWeek):
            To_week = "LinkButton_下一周"
        else:
            To_week = "LinkButton_上一周"

        while(week!=nowWeek):
            post_data = {
                            "__EVENTTARGET":To_week,
     	                    "__VIEWSTATE":soup.find('input',id='__VIEWSTATE')['value'],
        	                "__VIEWSTATEGENERATOR":soup.find('input',id='__VIEWSTATEGENERATOR')['value'],
                            "__EVENTVALIDATION":soup.find('input',id='__EVENTVALIDATION')['value'],
                            "cbo_学年学期":"2018-2019学年第二学期"
}
            print(week,"/",nowWeek)
            result = self.opener.open(timeTable_url,urllib.parse.urlencode(post_data).encode(encoding='UTF8'))
            soup = BeautifulSoup(result,"html5lib")
            nowWeek = int(soup.find(id='lbl_b_周次').get_text())
	#日你妈的python  BeautifulSoup 玄学大傻逼BUG，无缘无故清理参数result
        result = self.opener.open(timeTable_url,urllib.parse.urlencode(post_data).encode(encoding='UTF8'))
        return result.read().decode('UTF8')
