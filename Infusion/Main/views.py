from django.shortcuts import render, redirect
import os, json, logging, datetime, shutil, zipfile


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from infusionsoft.library import Infusionsoft

import requests
from infusionsoft.library import InfusionsoftOAuth

logger = logging.getLogger(__name__)

client_id = 'wvgef5dvca2a97pz3wk9yzua'
auth_redirect_uri = 'https://164889b3.ngrok.io/authorized'
client_secret = 'mkPsSgSwrb'

# carguruleads1@gmail.com
# Carguru11

def index(request):
	if 'infusionsoft_token' not in request.session:
		return render(request, 'index.html')
	isAuthenticated = request.session['infusionsoft_token']
	logger.error(isAuthenticated)	
	if isAuthenticated == '':
		return render(request, 'index.html')
	else:
		return redirect(home)

def home(request):
	return render(request, 'home.html')
def authorized(request):
	url = "https://api.infusionsoft.com/token"
	grant_type = 'authorization_code'
	
	req_dict = request.GET.dict()
	logger.error(req_dict.get('code'))
	logger.error(req_dict)
	auth_code = req_dict.get('code')
	payload_token = {
	'client_id':client_id,
        'grant_type':grant_type, 
	'redirect_uri':auth_redirect_uri,
	'code':auth_code, 		
	'client_secret': client_secret
	}
	logger.error(payload_token)
	r = requests.post(url, data=payload_token)
	logger.error(r.json())
	
	result = r.json()
	logger.error(dir(r))
	logger.error(dir(r.request))
	logger.error(r.status_code)
	if r.status_code == 400:
		logger.error('error')
		strRet = 'Access denied: reason=%s error=%s resp=%s' % (
            		result['error'],
		        result['error_description'],
	               	result
	        )
		logger.error(strRet)
		response = HttpResponse(strRet, content_type='text/plain')
		response.status_code = 404
		return response
#	logger.error(result['access_token'])
	access_token = result['access_token']
	request.session['infusionsoft_token'] = access_token
	return redirect(home)
def login(request):
	response_type = "code"
	url = "https://signin.infusionsoft.com/app/oauth/authorize?" + 		"client_id="+client_id + "&response_type="+response_type		+"&redirect_uri="+auth_redirect_uri + "&scope=full"
	logger.error(url)
	return redirect(url)	

def addcontact(request):
	if 'infusionsoft_token' not in request.session:
		return redirect(index)
	access_token = request.session['infusionsoft_token']
	contact = {'FirstName' : request.POST.get('given_name'), 'LastName' : 	request.POST.get('family_name'), 'Email' : request.POST.get('email')}
	logger.error(contact)
	infusionsoft = InfusionsoftOAuth(access_token)

	result = infusionsoft.ContactService('add', contact)
	
	response = HttpResponse(result, content_type='text/plain')
	response.status_code = 200
	return response


