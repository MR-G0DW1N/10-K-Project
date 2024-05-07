import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from sec_edgar_downloader import Downloader

import os
import tempfile
import textwrap

import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

#from dotenv import load_dotenv, dotenv_values 


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



def download10k (ticker, company, email, download_folder):
    dl = Downloader(company,email,download_folder)
    dl.get("10-K",ticker,after="1995-01-01",download_details=True)

def find_table_recursive(element):

    parent = element.find_next_sibling('div')
    table = parent.find('table')
    if table is not None:
        return table  

    if parent is not None:
        return find_table_recursive(parent)  

    return None      

def findtable(soup1):

    table1 = soup1.find_all('p')
    
    if len(table1)!=0:
        for t in table1:
            for child in t.children:
                str1 = child.get_text()
                #print(str1+'n')
                if r'CONSOLIDATED'and 'BALANCE'and 'SHEETS' in str1:
                    p = t.find_next_sibling('table')
                    if p is None :
                        find_table_recursive(t)

                    rows = p.find_all('td')
                    
                    row_data = []
                    
                    for row in rows:
                        #print(row.get_text())
                        row_data.append(row.get_text(strip=True))

                    s = []

                    for j in row_data:
                        if j == str(''):
                            continue
                        else:
                            s.append(j)

                            
                    prompt_data =''
                    prompt_data = prompt_data.join(s)

                    return prompt_data
                
    else:
        table1 = soup1.find_all('div')
        for t in table1:
            str2 = t.get_text()
            if 'CONSOLIDATED' and 'BALANCE'and 'SHEETS' in str2:
                z = find_table_recursive(t)

                rows = z.find_all('td')
                            
                row_data = []
                
                for row in rows:
                    row_data.append(row.get_text(strip=True))
                
                s = []

                for j in row_data:
                    if j == str(''):
                        continue
                    else:
                        s.append(j)
            
                prompt_data =''
                prompt_data = prompt_data.join(s)

                return prompt_data

#load_dotenv()

st.title("10-K form downloader and Analyser")

option = st.text_input("Do you need to download file: y/n")

if option == 'y':
    company = st.text_input('Company Name:')
    email = st.text_input("Email id:")
    download_folder = st.text_input(r"Download folder location")

    ticker = st.text_input("Please enter the name of Ticker")

    if st.button('Search'):
        download10k(ticker,company,email,download_folder)

    #if st.download_button("Download",form):
    #    st.write("Thank You")


#filepath = st.text_input("Enter file location:")
    
new_file = st.file_uploader("upload file")

#api_key =  os.getenv("api_key")
api_key = st.secrets["api_key"]

if st.button("Analyse"):

    #new_file = open(path,"r")
    htm1 = new_file.read()
    soup1 = BeautifulSoup(htm1,'html.parser')

    p=findtable(soup1)

    init_prompt = 'Analyse this data for me and find insights from it: '
    prompt = init_prompt +p

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt)

    st.write(response.text)


