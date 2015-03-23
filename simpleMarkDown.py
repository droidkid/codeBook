#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 yuvaraj <yuvaraj@eee-pc>
#
# Distributed under terms of the MIT license.

"""
Ultra Simple MarkDown Parser

*bold*
/italics/
[link 'text' source]

"""

import re;


class Parser:
    def __init__(self, pInput, pOutput):
        self.pInput = pInput;
        self.pOutput = pOutput;
        self.pos = 0;

    def read(self, till=1):
        ret = self.pInput[self.pos : self.pos + till];
        return ret;

    def hasNext(self):
        if(self.pos >= len(self.pInput)):
            return False;
        else:
            return True;

    def consume(self, till=1):
        self.pos = self.pos + till;

    def consumeLine(self):
        ret = "";
        while self.hasNext():
            c = self.read();
            if c == '\n':
                self.consume();
                break;
            ret = ret + c;
            self.consume();
        return ret;

    def readLine(self):
        ret = "";
        mark = self.pos;
        ret = self.consumeLine();
        self.pos = mark;
        return ret;

    def append(self, toAdd):
        self.pOutput = self.pOutput + str(toAdd);


    def parseList(self):
        listLevel = [-1];
        while True:
            line = self.readLine();
            if(re.match('^\s*-',line)==None):
                break;
            c = self.read();
            indent = 0;
            while c!='-':
                self.consume();
                c = self.read();
                indent = indent + 1;
            self.consume();

            while listLevel[-1] > indent:
                self.append(" "*listLevel[-1] + "<ol/>\n");
                listLevel.pop();

            if listLevel[-1] < indent:
                listLevel.append(indent);
                self.append(" "*listLevel[-1] + "<ol>\n");
            
            self.append(" "*listLevel[-1]+" <li>")
            self.parseLine(appendMarker=False);
            self.append("</li>\n");


        numOpen = len(listLevel);
        self.append("</ol>\n"*(numOpen-1));
        
            
            


    def parseHeading(self):
        headLevel = -1;
        while True:
            c = self.read();
            if c == '=':
                headLevel = headLevel + 1;
                self.consume();
            else:
                break;

        if headLevel > 7:
            headLevel = 7;
        if(headLevel <= 0):
            headLevel = 1;
        heading = '';

        self.append('<h'+str(headLevel)+'>');
        self.parseLine(endMarker=['=','\n'], appendMarker=False);

        self.append('</h'+str(headLevel)+'>\n');
        self.consumeLine();

            
    def sanitizeCode(self, line):
        ret = '';
        for c in line:
            if c == '<':
                ret= ret + '&lt';
            elif c == '&':
                ret = ret + '&amp'
            elif c == '>':
                ret = ret + '&gt';
            else:
                ret = ret + c;
        return ret;


    '''
    parseSourceCode() parses a Source Code Block

    A Source Code Block looks like

    ````````            //Atleast one `
    This is Code Here.
    Serious Code.       
    `````````           //Atleast one ` 



    and wraps it in a <pre class='prettyprint'> block.
    
    '''
    def parseSourceCode(self):
        self.append("<pre class='prettyprint'>\n");
        self.consumeLine();
        while self.hasNext():
            line = self.readLine();
            if(re.match('^`+', line)):
                self.append("</pre>\n");
                self.consumeLine();
                return;
            self.append(self.sanitizeCode(line)+"\n");
            self.consumeLine();
    

    '''
    
        parses and EmptyBlock of lines.
        If there is one empty line, then a <p/> is added.
        If there are more then corresponding number of <br/> are added.
    '''
    def parseEmptyBlock(self):
        self.consumeLine();
        numLine = 1;
        while(self.hasNext()):
            line = self.readLine();
            if(re.match('^\s*$', line )):
                self.consume();
                numLine = numLine + 1;
            else:
                break;
        if numLine == 1:
            self.append("<p/>\n");
        else:
            self.append("<br/>\n"*numLine);

    '''
        parses a inline anchor element.

        An anchor element looks like [link text here url]

        The url should not contain any spaces.

        ToADD: [img width: height: href];

    '''
    def parseAnchor(self):
        self.consume();
        insideBrackets = '';
        while(self.hasNext()):
            c = self.read();
            if c == '\\':
                self.consume();
                if self.hasNext():
                    c = self.read();
                else:
                    break;
            if c == ']':
                self.consume();
                break;
            else:
                self.consume();
                insideBrackets = insideBrackets + c;
            
        words = insideBrackets.split();
        if words[0] == 'link':
            url = words[-1];
            text = " ".join(words[1:-1]);
            self.append('<a href=\''+url+'\'>'+text+'</a>');

    '''
    Parses a Single Lines

    *bold*
    /italic/

    escape sequences with \

    links are added with [link], see parseAnchor()


    '''
    def parseLine(self, endMarker=['\n'], appendMarker=True):
        bFlag = 0;
        iFlag = 0;
        while self.hasNext():
            c = self.read();
            if c in endMarker:
                if appendMarker:
                    self.append(c);
                self.consume();
                break;
                
            if c=='*':
                if bFlag == 0:
                    self.append("<b>");
                else:
                    self.append("</b>");
                bFlag = 1-bFlag;
                self.consume();

            elif c=='/':
                if iFlag == 0:
                    self.append("<i>");
                else:
                    self.append("</i>");
                iFlag = 1-iFlag;
                self.consume();

            elif c=='[':
                self.parseAnchor();

            elif c=='\\':
                self.consume();
                if self.hasNext():
                    c = self.read();
                    self.append(c);
                    self.consume();

            else:
                self.append(c);
                self.consume();


    def parse(self):
        while(self.hasNext()):
            line = self.readLine();
            if (re.match('^\s*$', line)):
                self.parseEmptyBlock();
            elif (re.match('^`+', line)):
                self.parseSourceCode();
            elif (line[0]=='='):
                self.parseHeading();
            elif (line[0]=='-'):
                self.parseList();
            else:
                self.parseLine();



if __name__ == "__main__":

    try:
        pIn = "";
        while True:
            test = input();
            pIn = pIn + test + "\n";
    except EOFError:
        p = Parser(pIn, "");
        p.parse();
        print(p.pOutput);

