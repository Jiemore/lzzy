#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

def send(class_,location,time):

	#构造Json数据
	#str_param_json='{"class":"%s","location":"%s","time":"%s"}'%(class_,location,time)
	'Test'
	str_param_json={"class":class_,"location":location,"time":'2019-6-13 下午'}

	client = AcsClient('', '', 'default')
	request = CommonRequest()
	request.set_accept_format('json')
	request.set_domain('dysmsapi.aliyuncs.com')
	request.set_method('POST')
	request.set_protocol_type('https') # https | http
	request.set_version('2017-05-25')
	request.set_action_name('SendSms')

	request.add_query_param('TemplateParam', str_param_json)
	request.add_query_param('PhoneNumbers', "")
	request.add_query_param('SignName', "")
	request.add_query_param('TemplateCode', "")

	response = client.do_action(request)
	print(str_param_json)
	print(str(response, encoding = 'utf-8'))

