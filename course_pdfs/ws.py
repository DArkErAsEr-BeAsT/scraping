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
ws_folder = "/home/david/Documents/projects/scraping/course_pdfs/wahrstat"
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
    user_agent = 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    chrome_options = webdriver.ChromeOptions(); 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    #chrome_options.debugger_address="127.0.0.1:9222"
    chrome_options.add_argument("--headless")
    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": "/home/david/Documents/projects/scraping/course_pdfs/", "download.extensions_to_open": "applications/pdf"}
    chrome_options.add_experimental_option("prefs", profile)
    #chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option ( 'excludeSwitches', [ 'enable-automation']) # parameters added in the form of key-value pairs
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome( executable_path="/usr/local/bin/chromedriver",options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    scrape_ex_pdfs(driver)
    scrape_sol_pdfs(driver)
    #scrape_slides(driver)
    #time.sleep(20)
    #print("b")   
    driver.close()
    driver.quit()



def download_file(download_url, filename, folder):
    response = urllib.request.urlopen(download_url) 
    print(folder+"/"+filename+ ".pdf")   
    if not os.path.isfile(folder+"/"+filename+ ".pdf" ):
        file = open(folder+"/"+filename + ".pdf", 'wb')
        file.write(response.read())
        file.close()
        try:
            return file.read()
        except io.UnsupportedOperation:
            print("wtf")
    else:
        return 

def scrape_ex_pdfs(driver):
    driver.get("https://metaphor.ethz.ch/x/2021/fs/401-0614-00L/")
    time.sleep(1)
  
    for i in range (1,14):  
        try:
            pdf = driver.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr["+str(i)+"]/td[1]/a")
            
            file = download_file(pdf.get_attribute('href'), "ex"+str(i), ws_folder+"/ex")
           
            

        except NoSuchElementException:
            print("no serie")
    pdf_merge(ws_folder+"/ex", ws_folder+"/ex_result.pdf")

def scrape_sol_pdfs(driver):
    driver.get("https://metaphor.ethz.ch/x/2021/fs/401-0614-00L/")
    time.sleep(1)
  
    for i in range (1,14):
        try:
            pdf = driver.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr["+str(i)+"]/td[3]/a")
            #pdfs.(pdf)
            download_file(pdf.get_attribute('href'), "sol"+str(i), ws_folder+"/sol")
     
        except NoSuchElementException:
            print("no serie")
    pdf_merge(ws_folder+"/sol", ws_folder+"/sol_result.pdf")

def scrape_slides(driver):
    driver.get("https://metaphor.ethz.ch/x/2021/fs/401-0614-00L/")
    time.sleep(1)
  
    for i in range (1,14):
        try:
            pdf = driver.find_element_by_xpath("/html/body/main/article/div/div/div/table[1]/tbody/tr["+str(i)+"]/td[3]/a")
            #pdfs.(pdf)
            download_file(pdf.get_attribute('href'), "slide"+str(i), "slides")
        
        except NoSuchElementException:
            print("no slide")
    pdf_merge("slides", "slides_result.pdf")
main()