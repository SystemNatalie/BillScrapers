"""
AlaskaTextCleaner.py
This program takes txt files obtained from alaska and rewrites it as a .txt file
It also removes some stuff like whitespace and line numbers
"""
import os
from string import digits
format_to_clean = ".pdf"

if format_to_clean == ".txt":
    for in_file in os.listdir("bills/alaska"):
        if in_file.endswith(".txt"):

                try:
                    with open(os.path.join("bills/alaska", in_file), "r", encoding="utf-8") as f:
                        with open("bills-plaintext/alaska/" + in_file, "w", encoding="utf-8") as out_file:
                            tripwire=False
                            for line in f:
                                if not tripwire:#skip "HOUSE BILL NO. 2                                                                           "
                                    tripwire = True
                                    continue
                                line = line.lstrip(digits)
                                line = line[1:]
                                out_file.write(line)
                except UnicodeDecodeError:
                    try:
                        with open(os.path.join("bills/alaska", in_file), "r", encoding="cp1252") as f:
                            with open("bills-plaintext/alaska/" + in_file, "w", encoding="cp1252") as out_file:
                                tripwire = False
                                for line in f:
                                    if not tripwire:  # skip "HOUSE BILL NO. 2                                                                           "
                                        tripwire = True
                                        continue
                                    line = line.lstrip(digits)
                                    line = line[1:]
                                    out_file.write(line)
                    except Exception as e:
                        print(e)

elif format_to_clean == ".pdf":
    import pymupdf
    from string import digits, whitespace
    import os

    for file in os.listdir("bills/alaska"):
        if file.endswith(".pdf"):
            doc = pymupdf.open("bills/alaska/" + file)
            page: pymupdf.Page
            tripwire = False
            with open("bills-plaintext/alaska/" + file[:-4] + ".txt", "w") as f:
                for page in doc:
                    text = page.get_text(sort=True)
                    newlinesplit = list(filter(('').__ne__, text.split("\n")[1:]))
                    for idx, line in enumerate(newlinesplit):
                        lineold = line.lstrip(whitespace)
                        line = line.lstrip(whitespace)  # remove whitespace used for padding
                        line = line.lstrip(digits)  # remove line number (if any)
                        if lineold != line:  # if we removed a digit from the first line, most likely meaning its a line of the bill
                            f.write(line + '\n')

