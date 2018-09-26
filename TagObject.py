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

"""This file is a single class object used by QTI-in-Style to black-box all tag formatting and style creation."""

from re import finditer
class TagObject:
    def __init__(self, newOriginal, newID):
        styleRegex = '(style=\"\"|clear=\"\"|border=\"\"|bordercolor=\"\"|cellpadding=\"\"|cellspacing=\"\"|width=\"\"|height=\"\"|align=\"\"|valign=\"\"|hspace=\"\"|vspace=\"\"|bgcolor=\"\"|color=\"\"|text=\"\"|background=\"\"|style=\".+?\"|clear=\".+?\"|border=\".+?\"|bordercolor=\".+?\"|cellpadding=\".+?\"|cellspacing=\".+?\"|width=\".+?\"|height=\".+?\"|align=\".+?\"|valign=\".+?\"|hspace=\".+?\"|vspace=\".+?\"|bgcolor=\".+?\"|color=\".+?\"|text=\".+?\"|background=\".+?\"|nowrap|noshade|STYLE=\"\"|CLEAR=\"\"|BORDER=\"\"|BORDERCOLOR=\"\"|CELLPADDING=\"\"|CELLSPACING=\"\"|WIDTH=\"\"|HEIGHT=\"\"|ALIGN=\"\"|VALIGN=\"\"|HSPACE=\"\"|VSPACE=\"\"|BGCOLOR=\"\"|COLOR=\"\"|TEXT=\"\"|BACKGROUND=\"\"|STYLE=\".+?\"|CLEAR=\".+?\"|BORDER=\".+?\"|BORDERCOLOR=\".+?\"|CELLPADDING=\".+?\"|CELLSPACING=\".+?\"|WIDTH=\".+?\"|HEIGHT=\".+?\"|ALIGN=\".+?\"|VALIGN=\".+?\"|HSPACE=\".+?\"|VSPACE=\".+?\"|BGCOLOR=\".+?\"|COLOR=\".+?\"|TEXT=\".+?\"|BACKGROUND=\".+?\"|NOWRAP|NOSHADE)'
        idRegex = '^(?!--|-[0-9])[-_a-zA-z][-_0-9a-zA-Z]*$'
        #Initialize all variables        
        self.Original = newOriginal
        #Validate that ID is accurate
        testID = finditer(idRegex, newID)
        try:
            next(testID)[0]
            self.ID = newID
        except StopIteration:
            raise ValueError('Invalid CSS ID. Refer to W3C specifications.')
        self.Formatted = self.Original
        self.Style = ''
        self.Attributes = []
        #Create list of all HTML attributes in tag
        searchResults =  finditer(styleRegex, self.Original)
        while searchResults:
            try:
                self.Attributes.append(next(searchResults)[0])
            except StopIteration:
                break
        #If list isn't empty,
        if self.Attributes:
            #strip attributes in list from tag and delete extra spaces.
            for attribute in self.Attributes:
                self.Formatted = self.Formatted.replace(attribute, '')
                self.Formatted = self.Formatted.replace('  ', ' ')
                self.Formatted = self.Formatted.replace(' >', '>')
            if self.Formatted[-2:] == '/>':
                self.Formatted = self.Formatted.replace('/>', ' id="' + self.ID + '" />')
            else:
                self.Formatted = self.Formatted.replace('>', ' id="' + self.ID + '">')
            #and write them into a CSS block
            self.Style = '#' + self.ID + ' {'
            for attribute in self.Attributes:
                if attribute[:7].lower() == 'style="':
                    if attribute[7:-1] != '':
                        self.Style = self.Style + '\n\t' + attribute[7:-1].replace(';', ';\n\t') + ';'
                elif attribute[:7].lower() == 'clear="':
                    if attribute[7:-1] != '':
                        self.Style = self.Style + '\n\t' + 'clear: ' + attribute[7:-1].replace('all', 'both') + ';'
                elif attribute[:13].lower() == 'bordercolor="':
                    if attribute[13:-1] != '':
                        self.Style = self.Style + '\n\t' + 'border-color: ' + attribute[13:-1] + ';'   
                elif attribute[:7].lower() == 'align="':
                    if attribute[7:-1] != '':
                        self.Style = self.Style + '\n\t' + 'text-align: ' + attribute[7:-1] + ';'
                elif attribute[:8].lower() == 'valign="':
                    if attribute[8:-1] != '':
                        self.Style = self.Style + '\n\t' + 'vertical-align: ' + attribute[8:-1] + ';'
                elif attribute[:9].lower() == 'bgcolor="':
                    if attribute[9:-1] != '':
                        self.Style = self.Style + '\n\t' + 'background-color: ' + attribute[9:-1] + ';'
                elif attribute[:7].lower() == 'color="':
                    if attribute[7:-1] != '':
                        self.Style = self.Style + '\n\t' + 'color: ' + attribute[7:-1] + ';'
                elif attribute[:12].lower() == 'background="':
                    if attribute[12:-1] != '':
                        self.Style = self.Style + '\n\t' + 'background-image:url(' + attribute[12:-1] + ')f;'
                elif attribute[:6].lower() == 'text="':
                    if attribute[6:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'color: ' + str(int(attribute[6:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'color: ' + attribute[6:-1] + ';'
                elif attribute[:8].lower() == 'border="':
                    if attribute[8:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'border-width: ' + str(int(attribute[8:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'border-width: ' + attribute[8:-1] + ';'
                elif attribute[:13].lower() == 'cellpadding="':
                    if attribute[13:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'padding: ' + str(int(attribute[13:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'padding: ' + attribute[13:-1] + ';'
                elif attribute[:13].lower() == 'cellspacing="':
                    if attribute[13:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'border-spacing: ' + str(int(attribute[13:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'border-spacing: ' + attribute[13:-1] + ';'
                elif attribute[:7].lower() == 'width="':
                    if attribute[7:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'width: ' + str(int(attribute[7:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'width: ' + attribute[7:-1] + ';'
                elif attribute[:8].lower() == 'height="':
                    if attribute[8:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'height: ' + str(int(attribute[8:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'height: ' + attribute[8:-1] + ';'
                elif attribute[:8].lower() == 'hspace="':
                    if attribute[8:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'margin-left: ' + str(int(attribute[8:-1])) + 'px;'
                            self.Style = self.Style + '\n\t' + 'margin-right: ' + str(int(attribute[8:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'margin-left: ' + attribute[8:-1] + ';'
                            self.Style = self.Style + '\n\t' + 'margin-right: ' + attribute[8:-1] + ';'
                elif attribute[:8].lower() == 'vspace="':
                    if attribute[8:-1] != '':
                        try:
                            self.Style = self.Style + '\n\t' + 'margin-top: ' + str(int(attribute[8:-1])) + 'px;'
                            self.Style = self.Style + 'margin-bottom: ' + str(int(attribute[8:-1])) + 'px;'
                        except:
                            self.Style = self.Style + '\n\t' + 'margin-top: ' + attribute[8:-1] + ';'
                            self.Style = self.Style + '\n\t' + 'margin-bottom: ' + attribute[8:-1] + ';'
                elif attribute[:6].lower() == 'nowrap':
                    self.Style = self.Style + '\n\t' + 'white-space: nowrap' + ';\n\t'
                elif attribute[:7].lower() == 'noshade':
                    self.Style = self.Style + '\n\t' + 'height: 2px;\n\tborder-width: 0;\n\tcolor: gray;\n\tbackground-color: gray' + ';'    
            self.Style = self.Style + '\n}'
            self.Unchanged = False
        else:
            self.Unchanged = True
        self.AlreadyInitialized = True
                    
    def __setattr__(self, attributeName, valueAttempt):
        #If the program attempts to change self.Original or self.ID, reinitialize with the updated value. This method is not advised but still supported.
        if hasattr(self, 'AlreadyInitialized'):
            if attributeName == 'Original':
                del self.AlreadyInitialized
                self.__init__(valueAttempt, self.ID)
            if attributeName == 'ID':
                del self.AlreadyInitialized
                self.__init__(self.Original, valueAttempt)
            if attributeName == 'Formatted' or attributeName == 'Attributes' or attributeName == 'Regex' or attributeName == 'Style' or attributeName == 'AlreadyInitialized':
                raise RuntimeError('The attribute "' + attributeName + '" cannot be manually assigned.')
        else:
            object.__setattr__(self, attributeName, valueAttempt)
