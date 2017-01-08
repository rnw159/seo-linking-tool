
import argparse
import csv
import string
import glob, os

import shutil

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='do shit.')

parser.add_argument('--sheet', action="store", dest="sheet")
parser.add_argument('--ignore', action="store", dest="ignore")

args = parser.parse_args()
sheetFileName = args.sheet
fileToIgnore = args.ignore

def csvToDict(fileName):
    with open(fileName, 'rt') as f:
        reader = csv.DictReader(f)
        result = []
        for row in reader:
            slug = ''
            if row['Website URL']:
                slug = row['Website URL'].split('//')[1].split('/')[1]
            # print slug
            result.append({'url':row['Website URL'],'keyword':row['Keyword(s)'],'slug':slug})
        return result

def getFilesToEdit(fileToIgnore):
    # os.chdir("")
    files = []
    for file in glob.glob("*.html"):
        if file != fileToIgnore:
            with open(file) as f:
                text = f.read()
                files.append({'name':file,'text':text,'soup':BeautifulSoup(text,'html.parser')})
    return files



def isStringInLinkTextInFile(file,string):
    for link in file['soup'].findAll('a'):
        if string.lower() in link.text.lower():
            return True
    return False



def editFiles(files,sheet):
    editedFiles = []
    for file in files:
        print '----'
        print file['name']
        name = file['name']
        text = file['text']
        for row in sheet:
            keyword = row['keyword']
            url = row['url']
            slug = row['slug']
            if slug.lower() != name.replace('.html','').lower():
                if isStringInLinkTextInFile(file,keyword) == False:
                    additionalChars = ""
                    n = text.lower().find(' '+keyword.lower())
                    if n != -1:
                        # print text[n+len(keyword)]
                        i = 0
                        while text[n+len(keyword)+i] in string.ascii_letters:
                            additionalChars += text[n+len(keyword)+i]
                            i = i + 1
                        # print n
                        # print len(keyword)
                        # print i
                        stringToBeReplaced = text[n:n+len(keyword)+i]
                        print stringToBeReplaced

                        replacementString = '<a href="'+url+'" meaning_of_life="42" target="_blank">'+stringToBeReplaced+'</a>'

                        text = text.replace(stringToBeReplaced,replacementString,1)

        editedFiles.append({'text':text,'name':name})
    return editedFiles

def outputFiles(files):
    if os.path.exists('output'):
        shutil.rmtree('output')
    if not os.path.exists('output'):
        os.makedirs('output')

    # oldFiles = glob.glob('output')
    # for f in oldFiles:
    #     print f
    #     os.remove(f)


    for file in files:
        text_file = open('output/'+file['name'], "w")
        text_file.write(file['text'])
        text_file.close()


sheet = csvToDict(sheetFileName)
files = getFilesToEdit(fileToIgnore)
editedFiles = editFiles(files,sheet)
outputFiles(editedFiles)


#might fuck up if the keyword contains none-ascii characters
# print files
# print sheet