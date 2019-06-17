from lzzy import lzzy
import time,datetime
from bs4 import BeautifulSoup
import AliSend
from apscheduler.schedulers.blocking import BlockingScheduler

def get_weekday():
	dt = datetime.datetime.now()
	weekday = dt.weekday()
	return str(int(weekday)+1)

def get_week():
	startDay = '2019-03-11'
	sd = datetime.datetime.strptime(startDay, '%Y-%m-%d')
	now = datetime.datetime.now()
	nowDay = now.strftime('%Y-%m-%d')
	nd = datetime.datetime.strptime(nowDay,'%Y-%m-%d')
	return int(((nd-sd).days/7))+1

def get_period():
	#时间段
	Morning = datetime.datetime.strptime(str(datetime.datetime.now().date())+'12:10', '%Y-%m-%d%H:%M')
	Night = datetime.datetime.strptime(str(datetime.datetime.now().date())+'18:10', '%Y-%m-%d%H:%M')
	Tomorrow = datetime.datetime.strptime(str(datetime.datetime.now().date())+'22:30', '%Y-%m-%d%H:%M')
	#当前时间
	nowTime = datetime.datetime.now()
	#早上	00:00-12:10
	if nowTime < Morning:
		return 1
	#下午	12:10-18:10
	elif nowTime > Morning and nowTime < Night:
		return 2
	#晚上	18:10-22:30
	elif nowTime > Night and nowTime < Tomorrow:
		return 3
	#明天	22:30-23:59
	elif nowTime > Tomorrow:
		return -1
	else:
		return -2


def main():
	uid = "20170309007"
	pwd = uid
	lz = lzzy('Ts',uid,pwd)
	day = "今天，"#今天||明天

	#获取当前周数的课表
	timeTable = lz.get_timeTable_ToWeek(get_week())
	soup = BeautifulSoup(timeTable,"html5lib")
	#周几
	wd = int(get_weekday())
	#时间段
	period = get_period()
	#明天早上的提醒
	if period < 0:
		period = 1
		wd = wd + 1
		day = "明天，"
	#构造查找HTML id串
	strfind = "Label_%d_%d"%(wd,period)
	'Test'
	#strfind = "Label_2_1"
	Course = soup.find(id=strfind).get_text()
	#无课提示并且跳出
	if Course == '' and len(Course) == 0:
		print("没有课哦~")
		return False
	#提取详细信息
	Course = Course.replace('时间：','')
	Course = Course.replace('课程名称：','')
	Course = Course.replace('课室：','')
	Course = Course.replace('任课老师：','')
	ArrayCourse = Course.strip().split(" ")
	'Test'
	#print(ArrayCourse)
	#删除Lable_里的空元素
	count = 0
	while count < len(ArrayCourse):
#		print(ArrayCourse[count])
		if ArrayCourse[count] == '' or len(ArrayCourse[count]) == 0:
			del ArrayCourse[count]
#			print (count)
			count = count - 1
		count = count + 1
	count = 0

	'Test'
	#print ('Test ArrayCourse:\n')
	#print (ArrayCourse)

	'构造参数，使用阿里云发送短信提示'
	Class = ArrayCourse[2]
	Location = ArrayCourse[5]
	Time = day+ArrayCourse[0]+ArrayCourse[1]

	'Test'
	#print('-------------')
	#for i in ArrayCourse:
	#	print(i)
	print('-------------')
	print("课程:"+Class)
	print("教室:"+Location)
	print("时间:"+Time)
	print('-------------')
	#调用阿里云接口
	print("---用阿里云接口---")
	AliSend.send(Class,Location,Time)	


if __name__ == '__main__':
	try:
		print("---初始化定时任务列队---")
		scheduler = BlockingScheduler()
		print("注册任务：每天13点45分提醒")
		#每天13点10分提醒
		scheduler.add_job(main, 'cron', hour=13,minute=10)
		print("注册任务：每天22点25分提醒 提醒内容为明天早上")
		#每天22点25分提醒 提醒内容为明天早上
		scheduler.add_job(main, 'cron', hour=22,minute=40)
		print("执行中")
		scheduler.start()
	except (KeyboardInterrupt, SystemExit):
		print("\n---删除所有作业并退出---")
		scheduler.remove_all_jobs(jobstore=None)#删除所有作业
