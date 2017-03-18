from random import randint
import json
import requests
import urllib


# opens up the files for reading and writing
with open('Albums.txt', 'r') as inFile, open('artists.txt', 'w') as outFile:
    albumIDs = []
    searchBase ="https://api.spotify.com/v1/search?q="
    searchType ="&type=album"
    while True:
        artist = inFile.readline().strip()
        album = inFile.readline().strip()
        if not artist or not album:
            break
        qstring = ("album:%s artist:%s" % (album, artist))
        search = requests.get(searchBase + urllib.quote(qstring) + searchType)
        #error handling
        if search.status_code != 200:
            print search.status_code
            continue
        data = json.loads(search.text)
        # gets the albums from the search
        albumMatches = data["albums"]["items"]
        # if there are no albums then skip
        if len(albumMatches) == 0:
            print 'no matches for %s' % album
            continue
        # if there are multiple albums from the search choose the first
        if len(albumMatches) > 1:
            print "multiple matches for %s" % album
            print 'choosing %s' % albumMatches[0]['artists'][0]['name']
        
        albumID = albumMatches[0]["id"]
        albumIDs.append(albumID)
        print "%s: %s" % (album, albumID)
    getAlbumBase = "https://api.spotify.com/v1/albums/"
    getAlbumEnd = "/tracks"
    for ID in albumIDs:
        getAlbum = requests.get(getAlbumBase + ID + getAlbumEnd)
        albumData = json.loads(getAlbum.text)
        tracks = albumData["items"]
        listArtists = []
        for track in tracks:
            for artist in track["artists"]:
                if artist["name"] not in listArtists:
                    listArtists.append(artist["name"])
                    if artist["name"] not in artistCoords:
                        xCoord = randint(0, 300)
                        yCoord = randint(0, 300)
                        artistCoords[artist["name"]] = (xCoord, yCoord)
                    else:
                        xCoord, yCoord = artistCoords[artist["name"]]
                    
                    try: 
                        outFile.write(artist["name"] + "," + str(xCoord) + "," + str(yCoord) + "," + listArtists[0] + "," + str(xCoord)  + "," + str(yCoord) + "\n")
                    except UnicodeEncodeError:
                        print(artist["name"] + "Unicode")
