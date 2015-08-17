import resources.lib.pcloudapi

import sys
import urllib
import urlparse
import xbmcplugin
import xbmcgui
import xbmcaddon

myAddon = xbmcaddon.Addon()
#customSettingsPath = xbmc.translatePath( __addon__.getAddonInfo("profile") ).decode("utf-8")
#customSettingsFilename = customSettingsPath + "customSettings.xml"

base_url = sys.argv[0] 						# The base URL of your add-on, e.g. 'plugin://plugin.video.pcloud-video-streaming/'
addon_handle = int(sys.argv[1])				# The process handle for this add-on, as a numeric string
xbmcplugin.setContent(addon_handle, 'movies')

args = urlparse.parse_qs(sys.argv[2][1:])	# The query string passed to your add-on, e.g. '?foo=bar&baz=quux'

pcloud=resources.lib.pcloudapi

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

'''	
auth = myAddon.getSetting("auth")

if auth == "":
	myAddon.openSettings()
	#xbmcgui.Dialog().notification("Info", auth, time=10000)
	username = myAddon.getSetting("username")
	xbmcgui.Dialog().notification("Info", username, time=10000)
'''
	
authList = args.get("auth", None)
if authList is None:
	auth = pcloud.PerformLogon("guido.domenici@gmail.com", "qei835GD") # and so will the credentials
else:
	auth = authList[0]

mode = args.get("mode", None)

# Mode is None when the plugin gets first invoked - Kodi does not pass a query string to our plugin's base URL
if mode is None:
	folderID = None
	mode = [ "folder" ]

if mode[0] == "folder":
	folderID = args.get("folderID", None)
	if folderID is None:
		folderID = 0
	else:
		folderID = int(folderID[0])
	
	folderContents = pcloud.ListFolderContents(folderID, auth)
	for oneItem in folderContents["metadata"]["contents"]:
		if oneItem["isfolder"] == True:
			#url = build_url({'mode': 'folder', 'folderID': 'Folder One'})
			url = base_url + "?mode=folder&folderID=" + `oneItem["folderid"]` + "&auth=" + auth
			li = xbmcgui.ListItem(oneItem["name"], iconImage='DefaultFolder.png')
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
									listitem=li, isFolder=True)
		else:
			contentType = oneItem["contenttype"]
			if contentType != "video/mp4": #TODO: add more content types
				continue
			li = xbmcgui.ListItem(oneItem["name"], iconImage='DefaultVideo.png')
			#fakeUrl = "http://192.168.1.250/video.mp4" # TODO: call PCloud's streaming API to get real URL
			li.addStreamInfo(
				"video", 
				{ 	"duration": int(float(oneItem["duration"])),
					"codec": oneItem["videocodec"],
					"width": oneItem["width"],
					"height": oneItem["height"]
				}
			)
			li.addStreamInfo(
				"audio",
				{ 	"codec", oneItem["audiocodec"] }
			)
			fileUrl = base_url + "?mode=file&fileID=" + `oneItem["fileid"]` + "&auth=" + auth
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=fileUrl, listitem=li)
			
	xbmcplugin.endOfDirectory(addon_handle)
	
elif mode[0] == "file":
	fileID = int(args["fileID"][0])
	auth = args["auth"][0]
	# Get streaming URL from pcloud
	streamingUrl = pcloud.GetStreamingUrl(fileID, auth)
	player = xbmc.Player()
	player.play(streamingUrl)
