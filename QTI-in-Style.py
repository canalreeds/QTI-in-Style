"""
Copyright 2018 Brian Dean.

This file is part of QTI-in-Style.

    QTI-in-Style is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    QTI-in-Style is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with QTI-in-Style.  If not, see <https://www.gnu.org/licenses/>.

"""

"""This program opens an XML file, strips out the CSS
and HTML style formatting, and creates a new stripped
down HTML file with external CSS."""

from os.path import isfile, join, exists
from os import makedirs, listdir
from re import search, sub, finditer
from TagObject import TagObject

outputFolder = "output"                                                         #Specifies the subfolder for the output files
SentinelTag = "<itemBody>"                                                      #Sets the tag before which the stylesheet tag should be placed
CSSIDPrefix = 'QTI-in-Style'
CSSPattern = 'style=\".+?\"'                                                    #Regex to find CSS to strip out
TagPattern = '<.+?>'
FullSearchPattern = '(border=\".+?\"|style=\".+?\"|cellpadding=\".+?\"|cellspacing=\".+?\"|height=\".+?\"|width=\".+?\"|align=\".+?\"|bgcolor=\".+?\"|hspace=\".+?\"|vspace=\".+?\"|valign=\".+?\")'

def ValidateFile(fileName):
    """
    Validates if the file exists and is the right type
    """
    if isfile(fileName) == False:                                               #Does the desired file exist?
        print("File does not exist, try again.")
        return False    
    elif fileName.endswith(".xml") == False:                                    #Is it an XML file?
        print("File is not valid type, try again.")
        return False
    else:
        return True

def DoOutputsExist(fileName):
    """
    This function tests to see whether the output files for the specified input file exists
    """
    eitherExists = False
    newXMLName = join(outputFolder, fileName)
    newCSSName = join(outputFolder, fileName[:-3] + "css")
    if isfile(newXMLName) or isfile(newCSSName):                                #If either output file exists, return true, else return false
        eitherExists = True
    return eitherExists

def ClearOutputFiles(fileName):
    """
    This function is only called if the output files already exist and the user agrees to overwrite them.
    """
    newXMLName = join(outputFolder, fileName)
    newCSSName = join(outputFolder, fileName[:-3] + "css")
    newXMLFile = open(newXMLName, "w")                                          #Clear out XML file
    newXMLFile.close()
    newCSSFile = open(newCSSName, "w")                                          #Clear out CSS file
    newCSSFile.close()

def FormattedID(currentID):
    #blank comment for minimize button
    return CSSIDPrefix + str(currentID)                                         #ID to send to CSS parser
    
def IDAttribute(currentID):
    #blank comment for minimize button
    return 'id="' + FormattedID(currentID) + '"'                                #ID to put in XML code

def ParseXMLLine(fileName, lineString, currentID):
    """
    Takes the line of XML and writes a modified version to an output file
    """
    lineString = CleanUpLine(fileName, lineString)                              #Simple find/replace methods, no extraction
    listOfTags = MakeListFromSearch(TagPattern, lineString)                     #Break down line into tags
    for tag in listOfTags:
        newTag = TagObject(tag, FormattedID(currentID))                            #Make new TagObject object which creates its own style and formatted tag
        if newTag.Unchanged == False:                                           #If TagObject changes the contents...
            lineString = lineString.replace(tag, newTag.Formatted, 1)           #Replace the old with the new
            newCSSName = join(outputFolder, fileName[:-3] + "css")              #Path for output file, intelligent by OS
            newCSSFile = open(newCSSName, "a")                                  #append to end of file or create if new
            print(newTag.Style, file = newCSSFile, end = '')                    #Put new CSS ID info in stylesheet
            newCSSFile.close()
            currentID += 1
    newXMLName = join(outputFolder, fileName)                                   #Path for output file, intelligent by OS
    newXMLFile = open(newXMLName, "a")                                          #Append to end of file or create if new
    print(lineString, file = newXMLFile, end = '')                              #Write finished line to file
    newXMLFile.close()
    return currentID

def CleanUpLine(fileName, lineString):
    """
    Takes the line of XML, adds the stylesheet tag where needed, then removes unneccessary items
    """
    lineString = lineString.replace(SentinelTag, '<stylesheet href="' + 
                                    str(fileName)[:-4] + '.css" type="text/css" />\n\t' +
                                   SentinelTag)                                 #Put a CSS stylesheet reference in code
    lineString = lineString.replace('&nbsp;', '')                               #Remove non-breaking spaces
    lineString = lineString.replace("&rsquo;", "'")                             #Remove special apostrophes
    return lineString

def MakeListFromSearch(searchPattern, targetString):
    listOfThings = []                                                           #List of things to return
    thingsFound = finditer(searchPattern, targetString)                         #MatchObject of extracted substrings from string
    while thingsFound:                                                          #If collection is not empty, loop until done
        try:
            listOfThings.append(next(thingsFound)[0])                           #Pull next item from MatchObject and add to list
        except StopIteration:                                                   #Stop when all items used
            break
    return listOfThings                                                         #Send back a clean list of things to extract


def main():
    """
    Main body of code
    """
    if not exists(outputFolder):
        makedirs(outputFolder)
    stillContinuing = True
    while stillContinuing:
        listOfFiles = []
        askIfAll = ""
        while askIfAll != "y" and askIfAll != "n":
            askIfAll = input("Do you want to process ALL .xml files in this folder (y/n)?").lower()
            if askIfAll != "y" and askIfAll != "n":
                print("Invalid entry.")
        if askIfAll == "y":
            rawList = listdir()
            for possibleFile in rawList:
                if possibleFile.endswith(".xml"):
                    if possibleFile != "imsmanifest.xml":
                        listOfFiles.append(possibleFile)
        if askIfAll == "n":
            isValid = False
            fileName = ""
            while isValid == False:                                                     #Keeps trying until valid file selected
                fileName = input("Enter the file name: ")
                isValid = ValidateFile(fileName)
            listOfFiles.append(fileName)
        for eachFile in listOfFiles: 
            if DoOutputsExist(eachFile):
                askIfOverwrite = ""
                while askIfOverwrite != "y" and askIfOverwrite != "n":
                    askIfOverwrite = input("Outputs already exist for " + eachFile + ", overwrite (y/n)?").lower()
                    if askIfOverwrite != "y" and askIfOverwrite != "n":
                        print("Invalid entry.")
                if askIfOverwrite == "n":
                    stillContinuing = False
                    break
                else:
                    ClearOutputFiles(eachFile)
            currentFile = open(eachFile, "r")
            currentFileLines = currentFile.readlines()
            currentID = 0
            for lineString in currentFileLines:                                #Read each line of file and send it to the CSS and XML parsers
                currentID = ParseXMLLine(eachFile, lineString, currentID)
            currentFile.close()
        if stillContinuing == True:
            askIfDone = ""
            while askIfDone != "y" and askIfDone != "n":
                askIfDone = input("File(s) complete. Continue (y/n)?")
                if askIfDone != "y" and askIfDone != "n":
                    print("Invalid entry.")
            if askIfDone == "n":
                stillContinuing = False


if __name__ == "__main__":
    main()
