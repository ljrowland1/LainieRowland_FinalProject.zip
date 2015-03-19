## program compares vocab and syntax of political speeches with the vocab and syntax of the songs of a user inputted
## musician. It outputs xy coordinates into a csv file that a macro excel program will make into a graph that visually represents the 
## comparison

import csv
import urllib
import urllib2
import re
import os

Politicians = "/Users/lainierowland/Desktop/Politicians"  ## gives location of folder containing textfiles of speeches

#TODO
def Main():
    '''sets program in motion
    .--> csv'''
    artist = input('enter the name of a musician who you want to compare to politicians: ')
    artistList = []
    data = {}
    data['q']= artist
    url_values = urllib.urlencode(data)
    url = 'http://search.azlyrics.com/search.php?'
    full_url = url + url_values
    data = urllib2.urlopen(full_url)
    s = data.read()
    m = re.search('Artist(.*)Album', s, re.DOTALL)
    if m == None:    ## if artist doesn't show up in search results, program prompts you to enter another artist
        print('no results for that artist, the program will now restart')
        Main()
    a = m.groups(0)
    a = str(a)
    f = re.findall('\.html\">.[A-Z \.]*', a, re.DOTALL) 
    for item in f:
        item = item.replace('.html">', '')
        artistList.append(item)
    print(artistList)
    chosenArtistNumber = input('enter a number 1 through ' + str(len(artistList)) + ' corresponding to the placement of the artist you want in the list above: ')
    chosenArtistNumber = int(chosenArtistNumber)
    if chosenArtistNumber not in range(0, len(artistList)+1):
        print('Number not within range. Program will now restart.')
        Main()
    a = chosenArtistNumber - 1
    chosenArtist = artistList[a]
    chosenArtist = chosenArtist.lower()
    chosenArtist = chosenArtist.replace(' ', '')
    lyricList = getLyrics(chosenArtist)
    if lyricList == None:
        print('could not find lyrics for that artist. program will now restart.')
        Main()
    WLMusician = avgWLMusician(lyricList)
    SLMusician = avgSLMusician(lyricList)
    createOutput(artist, WLMusician, SLMusician, chosenArtist)
    print('now open workbook1 and press button to run macro code')
    
def removePunc(text):
    '''returns string with punctuation removed'
     string-->string   '''
    text=text.replace('-', "")
    text=text.replace('.', "")
    text=text.replace(',', "")
    text=text.replace('!', "")
    text=text.replace(':', "")
    text=text.replace('?', "")
    text=text.replace(';', "")
    text=text.replace('/', "")
    text=text.replace('"', "")
    text=text.replace(')', "")
    text=text.replace('(', "")
    text=text.replace("'", "")
    return text    
        
def getLyrics(chosenArtist):
    '''returns list of lyrics for songs by chosenArtist
    string --> list of strings'''
    songList = []
    finalSongList = []
    lyricList = []
    songListURL = 'http://www.azlyrics.com/' + chosenArtist[0] + '/' + chosenArtist + '.html' ## link that contains all songs by chosenArtist
    data = urllib.urlopen(songListURL)
    h = data.read()
    t = re.findall('s:.*.h:', h) ## retrieves all song names for chosenArtist
    for item in t:
        item = item.replace('s:"', '')
        item = item.replace('", h:', '')
        songList.append(item)
    for item in songList:
        if item not in finalSongList:
            finalSongList.append(item)
    for song in finalSongList:
        song = song.lower()
        song = song.replace(' ', '')
        song = removePunc(song)
        song = song.replace('&amp', '')
        songURL = 'http://www.azlyrics.com/lyrics/' + chosenArtist + '/' + song + '.html' # retrieves lyrics for each song by chosenArtist
        data = urllib2.urlopen(songURL)
        s = data.read()
        x = re.search('<!-- start of lyrics -->(.*)<!-- end of lyrics -->', s, re.DOTALL)
        lyrics = x.groups(0)
        lyrics = str(lyrics)
        lyrics = lyrics.replace('<!-- start of lyrics -->', '')
        lyrics = lyrics.replace('<!-- end of lyrics -->', '')
        lyrics = lyrics.replace('<br />', '')
        lyrics = lyrics.replace('\n', ' ')
        lyrics = lyrics.replace('\\r\\n', ' ')
        lyrics = lyrics.replace('\\n', '')
        lyricList.append(lyrics)
        return(lyricList)           

def avgWLMusician(lyricList):
    '''returns average word length for lyrics by given artist
    .--> float'''
    WLlist = []
    for lyrics in lyricList:
        lyrics = removePunc(lyrics)
        lyrics = lyrics.lower()
        lyrics = lyrics.split(' ')
        lyrics = removeStopWords(lyrics)
        for word in lyrics:
            wordLength = len(word)
            WLlist.append(wordLength)
    total = sum(WLlist)
    totalWords = len(WLlist)
    avg = float(total)/float(totalWords)
    return avg

def avgSLMusician(lyricList):
    ''' returns average sentence length (average number of words per sentence) for lyrics by given artist
    . --> float'''
    SLlist = []
    lengthList = []
    for lyrics in lyricList:
        lyrics = re.split('[?.!]', lyrics)
        for sentence in lyrics:
            sentence = sentence.split()
            SLlist.append(sentence)        
    for item in SLlist:
        if item == []:
            SLlist.remove(item)
    for sentence in SLlist:
        a = len(sentence)
        lengthList.append(a)
    b = sum(lengthList)
    c = len(lengthList)
    avg = (float(b))/(float(c))
    return avg    

def readFiles():
    ''' opens and reads files containing speeches/lyrics, return list of
    speeches in form ['all speeches by one person', 'all speeches by one person'...]
    .--> list of strings'''
    allSpeeches = []
    import os
    peopleList = os.listdir(Politicians)
    peopleList.remove('.DS_Store')
    for person in peopleList:
        speech = Politicians + '/' + person
        speech = open(speech, 'r')
        text = speech.read()
        text = text.replace('\n', '')
        text = text.replace('\r', '')
        speech.close
        allSpeeches.append(text)
    return allSpeeches

def removeStopWords(wordList):
    '''given a list of lower case words, returns a new list without stop words
    list of strings --> list of strings'''
    stopWords = '/Users/lainierowland/Desktop/stopwords.txt'
    myFile = open(stopWords,'r')
    myString = myFile.read()
    myFile.close()
    stopList = myString.split(',')
    for word in wordList:
        if word == word in stopList:
            wordList.remove(word)
    return wordList
    
def avgWordLength():
    '''returns a list of floats, each corresponding to the average word length
    of a politicians (not including stop words)
    .--> list of floats'''
    WLlist = []
    avgList = []
    allSpeeches = readFiles() 
    for personSpeeches in allSpeeches:
        speech = removePunc(personSpeeches)
        speech = speech.lower()
        listOfWords = speech.split(' ')
        listOfWords = removeStopWords(listOfWords)
        personLengths = []
        for word in listOfWords:
            wordLength = len(word)
            if wordLength != 0:
               personLengths.append(wordLength)
        WLlist.append(personLengths)
    for item in WLlist:
        avgWL = float(sum(item))/float(len(item))
        avgList.append(avgWL)
    return avgList

def avgSentLength():
    '''returns a list of floats, each corresponding to the average sentence length
(average number of words per sentence) of politicians
    .--> list of floats'''
    import re
    SLlist = []
    avgList = []
    allSpeeches = readFiles() # list of strings - each string represents all speeches of a politicitan
    for personSpeeches in allSpeeches:
        personLengths = []
        personSpeeches = re.split('[?.!]', personSpeeches)
        for item in personSpeeches: # item represents a sentence
            item = item.split()
            sentLength = len(item)
            if sentLength != 0:
               personLengths.append(sentLength)
        SLlist.append(personLengths)
    for item in SLlist:
        avgSL = float(sum(item))/float(len(item))
        avgList.append(avgSL)
    return avgList


def testSentLength():
    '''tests function avgSentLength, returns false if not working'''
    if avgSentLength() != [18.014890282131663, 19.108445297504797, 21.70493358633776, 24.054172767203514, 17.245205479452054]:
        return False

def testWordLength():
    '''tests function avgWordLength, returns false if not working'''
    if avgWordLength() != [5.728459348746789, 5.881334691000235, 5.985706580366775, 5.686571428571429, 5.3567737870195336]:
        return False
                           
def createOutput(artist, WLMusician, SLMusician, chosenArtist):
    '''creates list of lists - each list within the list contains a string of the musician/politician's name, followed by two floats,
    which are that person's average sentence length and word length. The function creates and opens a CSV file that contains the list
    .--> .'''
    data = []
    realPeopleList = []
    peopleList = os.listdir(Politicians)
    peopleList.remove('.DS_Store')
    PolSLlist = avgSentLength()
    PolWLlist = avgWordLength()
    for item in peopleList:
        item = item.replace('.txt', '')
        item = [item]
        realPeopleList.append(item)
    for item in realPeopleList:
        data.append(item) ## creates list of lists - each list containing the name of a politician
    for index in range(len(PolSLlist)):
        data[index].append(PolSLlist[index])
    for index in range(len(PolWLlist)):
        data[index].append(PolWLlist[index]) ## at this point there is a list of lists, each list in the format [name of politician, avg SL, avg WL]
    a = [chosenArtist, SLMusician, WLMusician]
    data.append(a)
    myfile = open('data.csv', 'w')
    c=csv.writer(myfile, dialect = 'excel')
    c.writerows(data)
    myfile.close()

testWordLength()
testSentLength()
Main()
