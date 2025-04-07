"""
AlaskaTextCleaner.py
This program takes txt files obtained from alaska and rewrites it as a .txt file
It also removes some stuff like whitespace and line numbers
"""
import os
from string import digits
format_to_clean = ".txt"

if format_to_clean == ".txt":
    for in_file in os.listdir("bills/alaska"):
        if in_file.endswith(".txt"):

                try:
                    with open(os.path.join("bills/alaska", in_file), "r", encoding="utf-8") as f:
                        with open("bills-plaintext/alaska/" + in_file, "w", encoding="utf-8") as out_file:
                            for line in f:
                                line = line.lstrip(digits)
                                line = line[1:]
                                out_file.write(line)
                except UnicodeDecodeError:
                    try:
                        with open(os.path.join("bills/alaska", in_file), "r", encoding="cp1252") as f:
                            with open("bills-plaintext/alaska/" + in_file, "w", encoding="cp1252") as out_file:
                                for line in f:
                                    line = line.lstrip(digits)
                                    line = line[1:]
                                    out_file.write(line)
                    except Exception as e:
                        print(e)

