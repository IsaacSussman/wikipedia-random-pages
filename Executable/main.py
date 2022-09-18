from pydoc import doc
import requests
#import bs4
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
    return page_py
    




def main():
    languageList = "en ceb sv de fr nl ru it es pl war vi ja arz zh ar uk pt fa ca sr id no ko fi hu cs sh zh-min-nan ro tr eu ce ms eo he hy bg da azb tt sk kk min hr et lt be el simple az sl gl ur nn ka hi th uz la ta cy vo mk ast zh-yue lv tg bn af mg oc bs sq nds ky new be-tarask ml te br vec mr pms tl jv su ht sw lb pnb ba ga my szl is fy cv lmo sco wuu diq an pa ku yo ne bar io gu ckb als kn scn bpy ia qu mn bat-smg si nv or cdo ilo gd xmf yi am nap bug wa sd hsb mai fo map-bms mzn li sah os eml frr ps sa avk gor bcl zh-classical ace mrj mhr hif hak roa-tara pam hyw km nso crh rue shn se as bh vls mi nds-nl nah sc ha vep gan sn myv ab glk bo so co tk kab fiu-vro sat zu csb kv ban ie pcd gv udm ay ug zea nrm lij kw frp lez gn lfn stq mwl gom rm mt lo lad olo koi fur bjn ang dty dsb ext ln cbk-zam tyv ary dv ksh gag pfl pi pag av awa haw bxr xal ig krc pap za rw pdc smn kaa szy arc to nov jam wo tpi kbp kbd inh na tet atj tcy ki ak jbo bi roa-rup lbe kg lg ty mdf xh lld fj srn gcr om ltg sm chr got kl pih st mnw ny nqo cu tw tn ts rmy bm chy rn tum ss ch ks iu pnt ady ve ee ik ff sg din dz ti cr mad nia tay trv mni alt skr dag shi guw"

    sg.theme('BrownBlue')


    #This is the ISO language code corresponding to the language you want
    language = "en"

    page=getRandPage(language)

    
    layout=[[sg.Button("Different Article"),sg.Button("Full Page")],[sg.Text("Language:  "),sg.InputText("en",key="-LANGIN-"),sg.Button("Switch Language"),sg.Button("Language List")],[sg.Multiline(page.title+"\n\n\n"+page.summary,size=(300,200),key="-SUMMARY-")]]
    # Create the Window
    window = sg.Window("Wikepia Random Article Selector", layout, size=(1000,400))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        if event == "Switch Language":
            if values["-LANGIN-"] in languageList:
                language = values["-LANGIN-"]
            else:
                sg.popup("That is not a valid language code. See ")
        if event == "Full Page":
            webbrowser.open(page.fullurl)
  
            
        if event == "Different Article":
            page=getRandPage(language)
            window["-SUMMARY-"].update(page.title+"\n\n\n"+page.summary)

        if event == "Language List":
            webbrowser.open_new_tab("https://web.archive.org/web/20220621083116/https://meta.wikimedia.org/wiki/List_of_Wikipedias_by_country")
    window.close()


if __name__=="__main__":
    main()

