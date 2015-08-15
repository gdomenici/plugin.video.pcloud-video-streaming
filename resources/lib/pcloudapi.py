import urllib2
import json
import hashlib
from numbers import Number # to check whether a certain variable is numeric

PCLOUD_BASE_URL = 'https://api.pcloud.com/'

def GetErrorMessage(errorCode):
	if errorCode == 1000:
		errorText = "Log in required."
	elif errorCode == 1002:
		errorText = "No full path or folderid provided."
	elif errorCode == 1004:
		errorText = "No fileid or path provided"
	elif errorCode == 1076:
		errorText = "Please provide 'tokenid'"
	elif errorCode == 2000:
		errorText = "Log in failed"
	elif errorCode == 2002:
		errorText = "A component of parent directory does not exist"
	elif errorCode == 2003:
		errorText = "Access denied. You do not have permissions to preform this operation"
	elif errorCode == 2005:
		errorText = "Directory does not exist"
	elif errorCode == 2009:
		errorText = "File not found"
	elif errorCode == 2010:
		errorText = "Invalid path."
	elif errorCode == 2102:
		errorText = "Provided 'tokenid' not found."
	elif errorCode == 4000:
		errorText = "Too many login tries from this IP address."
	elif errorCode == 5000:
		errorText = "Internal error. Try again later."
	else:
		errorText = "Unknown error"
	return errorText

def PerformLogon(username, password):
	url = PCLOUD_BASE_URL + 'getdigest'
	outputStream = urllib2.urlopen(url)
	response = json.load(outputStream)
	outputStream.close()
	if response["result"] != 0:
		errorMessage = GetErrorMessage(response["result"])
		print 'Error calling getdigest: ' + errorMessage
		exit()
	
	TOKEN_EXPIRATION_SECONDS = 14 * 86400 # 14 days
	authUrl = PCLOUD_BASE_URL + "userinfo?getauth=1&logout=1&username=" + username + "&digest=" + response["digest"] + \
				"&authexpire=" + `TOKEN_EXPIRATION_SECONDS` # this backtick affair is a to-string conversion
	sha1 = hashlib.sha1()
	sha1.update(username)
	usernameDigest = sha1.hexdigest() # hexdigest outputs hex-encoded bytes
	sha1 = hashlib.sha1()
	sha1.update(password + usernameDigest + response["digest"])
	passwordDigest = sha1.hexdigest()
	authUrl += "&passworddigest=" + passwordDigest
	outputStream = urllib2.urlopen(authUrl)
	response = json.load(outputStream)
	outputStream.close()
	if response["result"] != 0:
		errorMessage = GetErrorMessage(response["result"])
		print 'Error calling userinfo: ' + errorMessage
		exit()
	auth = response["auth"]
	return auth

def ListFolderContents(folderNameOrID):
	url = PCLOUD_BASE_URL + "listfolder?auth=" + auth
	if isinstance (folderNameOrID, Number):
		url += "&folderid=" + `folderNameOrID` # string coercion
	else:
		url += "&path=" + folderNameOrID
	outputStream = urllib2.urlopen(url)
	response = json.load(outputStream)
	outputStream.close()
	if response["result"] != 0:
		errorMessage = GetErrorMessage(response["result"])
		print 'Error calling listfolder: ' + errorMessage
		exit()
	return response

	
	
auth = PerformLogon("guido.domenici@gmail.com", "qei835GD")
#ListFolderContents("/Vcast")
#ListFolderContents(34719254)
#ListFolderContents(4684587) # random number, probably invalid
folderContents = ListFolderContents("/Vcast")
for oneItem in folderContents["metadata"]["contents"]:
	print oneItem["name"]
