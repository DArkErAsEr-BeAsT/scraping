#!/usr/bin/python
import PyPDF2
from selenium import webdriver
import urllib.request
import time
import os.path
from PyPDF2 import PdfFileWriter, PdfFileReader
from argparse import ArgumentParser
from glob import glob

from selenium.common.exceptions import NoSuchElementException
import io
ti_folder = "/Users/darkeraser/Documents/projects/scraping/course_pdfs/exams_TI"
import os

def pdf_merge(path, output_filename):
    output = PdfFileWriter()

    for pdffile in glob(path + os.sep + '*.pdf'):
        if pdffile == output_filename:
            continue
        print("Parse '%s'" % pdffile)
        document = PdfFileReader(open(pdffile, 'rb'))
        for i in range(document.getNumPages()):
            output.addPage(document.getPage(i))

    print("Start writing '%s'" % output_filename)
    with open(output_filename, "wb") as f:
        output.write(f)

if __name__ == "__main__":
    parser = ArgumentParser()

    # Add more options if you like
    parser.add_argument("-o", "--output",
                        dest="output_filename",
                        default="merged.pdf",
                        help="write merged PDF to FILE",
                        metavar="FILE")
    parser.add_argument("-p", "--path",
                        dest="path",
                        default=".",
                        help="path of source PDF files")

    args = parser.parse_args()
    pdf_merge(args.path, args.output_filename)



def main():
    pdf_merge(ti_folder, ti_folder+"/exam.pdf")




main()