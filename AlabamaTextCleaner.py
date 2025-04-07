"""
AlabamaTextCleaner.py
This program takes pdf files obtained from alabama and rewrites it as a .txt file
It also removes some stuff like whitespace and line numbers
"""
import pymupdf
from string import digits,whitespace
import os
for file in os.listdir("bills/alabama"):
    if file.endswith(".pdf"):
        doc = pymupdf.open("bills/alabama/"+file)
        #page 1 seems to be this pattern
        """
        1   billnumber
        2   billversion
        3   By Representative(s) xyz,abc,...
        4   RFD: xyz...
        5   First Read: 04-Feb-25
        """
        page:pymupdf.Page
        tripwire=True
        sectionflag=True
        sectionText=""
        bypassed_first_line=False
        with open("bills-plaintext/alabama/"+file[:-4]+".txt","w") as f:
            for page in doc:
                if tripwire:
                    tripwire=False
                    continue
                text = page.get_text(sort=True)
                newlinesplit=text.split("\n")
                for line in newlinesplit:
                    line = line.lstrip(whitespace)
                    lineold=line
                    line = line.lstrip(whitespace)
                    line = line.lstrip(digits)
                    if lineold==line:
                        continue
                    else: # part of the bill
                        if not bypassed_first_line:
                            bypassed_first_line=True
                            continue
                        f.write(line+'\n')