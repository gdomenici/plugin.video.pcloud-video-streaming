import pcloudapi

p = pcloudapi.PCloudApi()
#auth = p.PerformLogon("username", "password")
p.SetAuth("9TjCk7Z5OzzZsQpGms1VD804JuJtJaful5Fi4Jb7")
folder = p.ListFolderContents("/Vcast")
allFileIDs = [ oneItem["fileid"] for oneItem in folder["metadata"]["contents"] if not oneItem["isfolder"] ]
thumbs = p.GetThumbnails(allFileIDs)
print thumbs
print thumbs[381321361]