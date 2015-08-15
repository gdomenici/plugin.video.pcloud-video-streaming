import sys
import urllib
import urlparse
import xbmcplugin
import xbmcgui


''' PLUGIN_NAME = 'pcloud-video-streaming'
 PLUGIN_ID = 'plugin.video.pcloud-video-streaming'
 plugin = Plugin(PLUGIN_NAME, PLUGIN_ID, __file__)
'''

base_url = sys.argv[0] 						# The base URL of your add-on, e.g. 'plugin://plugin.video.myaddon/'
addon_handle = int(sys.argv[1])				# The process handle for this add-on, as a numeric string
xbmcplugin.setContent(addon_handle, 'movies')

args = urlparse.parse_qs(sys.argv[2][1:])	# The query string passed to your add-on, e.g. '?foo=bar&baz=quux'

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)
	
mode = args.get('mode', None)

# Mode is None when the plugin gets first invoked - Kodi does not pass a query string to our plugin's base URL
if mode is None:
	# creates a URL like plugin://plugin.video.pcloud-video-streaming/?mode=folder&foldername=Folder+One
    url = build_url({'mode': 'folder', 'foldername': 'Folder One'})
    li = xbmcgui.ListItem('Folder One', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

    url = build_url({'mode': 'folder', 'foldername': 'Folder Two'})
    li = xbmcgui.ListItem('Folder Two', iconImage='DefaultFolder.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)

# Mode is 'folder' when the user, after clicking on one of the dir entries created above, directs Kodi
# to reinvoke us with mode=folder on the query string
elif mode[0] == 'folder':
    foldername = args['foldername'][0]
    url = 'http://192.168.1.250/video.mp4'
    li = xbmcgui.ListItem(foldername + ' Video', iconImage='DefaultVideo.png')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)


'''
url = 'http://192.168.1.250/video.mp4'
li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png')
xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
xbmcplugin.endOfDirectory(addon_handle)
'''