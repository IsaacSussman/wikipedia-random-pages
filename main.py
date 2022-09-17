from pydoc import doc
import requests
import bs4
import numpy as np
import wikipediaapi as wa
import PySimpleGUI as sg
import webbrowser


"""
def getHeaderImage(text:str):
    soup = bs4.BeautifulSoup(text,"html.parser")
    print("Title of the website is : ")
    iImage = soup.find("td",{"class":"infobox-image"})
    if iImage != None:
        iImage=iImage
    print(iImage)
"""



def getRandPage(wikiLang:str) -> wa.WikipediaPage:
    """Takes in a language, returns a random article in that language as text in a string and a WikipediaPage

    Args:
        wikiLang (str): The language the article should be in, as a ISO language code 
        (https://www.iso.org/iso-639-language-codes.html)

    Returns:
        page_py (wikipediaapi.WikipediaPage): The wikipedia page, to be used by the wikipediaapi
    """

    wiki=wa.Wikipedia(wikiLang)  
    r = requests.get('https://%s.wikipedia.org/wiki/Special:Random' %wikiLang)
    text = r.text
    title = text[int(text.find("<title>"))+7:int(text.find("</title>"))]
    title = title[:title.find(" -")]
    page_py = wiki.page(title)
    print(page_py)
    
    return page_py
    




def main():
    reader=open("langlist")
    languageList = reader.read().split()
    reader.close()

    sg.theme('BrownBlue')


    #This is the ISO language code corresponding to the language you want
    language = "en"

    page=getRandPage(language)

    
    layout=[[sg.Button("Different Article"),sg.Button("Full Page")],[sg.Text("Language:  "),sg.InputText("en",key="-LANGIN-"),sg.Button("Switch Language"),sg.Button("Language List")],[sg.Multiline(page.title+"\n\n\n"+page.summary,size=(300,200),key="-SUMMARY-")]]
    # Create the Window
    window = sg.Window(page.title, layout, size=(1000,400))
    #    Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == "Switch Language":
            if values["-LANGIN-"] in languageList:
                language = values["-LANGIN-"]
            else:
                sg.popup("That is not a valid language code. See ")
        if event == "Full Article":
            webbrowser.open_new_tab(page.fullurl)
            
        if event == "Different Article":
            page=getRandPage(language)
            window["-SUMMARY-"].update(page.title+"\n\n\n"+page.summary)

        if event == "Language List":
            webbrowser.open_new_tab("https://web.archive.org/web/20220621083116/https://meta.wikimedia.org/wiki/List_of_Wikipedias_by_country")
    window.close()


if __name__=="__main__":
    main()

