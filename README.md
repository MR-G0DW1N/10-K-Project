# 10-K-Project

This web application allows you to download and analyze 10-K forms for various ticker symbols. The financial data analysis is powered by Google's Gemini API.

Link - https://10-k-project-devansh-kashyap.streamlit.app/

#Usage

Web Interface

    Download 10-K Forms
        Enter a ticker symbol in the input field and click "Search".
        The 10-K forms will be fetched and stored locally using the gatech_task1.1 script.

    Upload and Analyze
        Click on "Upload" to analyze a downloaded 10-K form.
        Select a file and click "Analyze" to process the form using the gatech_task1.2 script and Google's Gemini API.
        View the financial analysis results on the web interface.

#Files and Functions

gatech_task1.1

    Function: download10k(ticker, company, email, download_folder)
        Uses the sec_edgar_downloader library to download the 10-K form for a given ticker symbol from the SEC database.
        Saves the downloaded form locally.

gatech_task1.2

    Functions:
        findtable(soup)
            Find the desired table to extract its data from the 10K forms which arein the form of .html files. Uses BeautifulSoup4 to parse the html files.

#Deployment

This project is deployed as a web application using Streamlit. 

            
