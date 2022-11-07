import yaml
from os import mkdir
from time import sleep as sleep
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup as BS

BASE_URL = "https://en.wikichip.org"
URL = "https://en.wikichip.org/wiki/amd/microarchitectures/zen_3"#Would be the user input
req = Request(URL, headers={'User-Agent':'Mozilla/6.0'})


class Architerture():
  name = ""
  humanName = ""
  type = ""
  lithography = ""
  releaseDay = ""
  socket = ""
  parts = []


class PcPart():
  header = ""
  name = ""
  humanName=""
  type = ""
  releaseDate = ""
  coreCount = ""
  threadCount = ""
  l2Cache = ""
  l3Cache = ""
  baseFrequency = ""
  boostFrequency = ""
  tdp = ""
  l1DataCache = ""
  l1InstructionCache = ""
  unlocked = ""
  memoryType = ""
  maxMemoryFrequency = ""
  xfr = ""
  avxSseMmx = ""
  fma4 = ""
  fma3 = ""
  bmi = ""
  aes = ""
  sha = ""
  otherExtensions = []
  compatibleChipsets = []
  steppings = []

  #def __innit__(self, ):
  #

class Apu(PcPart):
  gpuModel = ""
  maxDisplays = ""
  shaderProcessorCount = ""
  textureMappingUnitCount = ""
  renderOutputUnitCount = ""
  gpuBaseFrequency = ""

def organiseData(specs,title):

  with open((title.replace(" ","-"))+'/'+ specs['model number']+'.yaml', 'w') as outfile:
    yaml.dump(specs, outfile, default_flow_style=False)

def statsPage(url, title):
  print("scraping "+ url+"...")
  sleep(1)
  try:
    webpage = urlopen(Request(url, headers={'User-Agent':'Mozilla/6.0'}))
  except HTTPError as e:#If there is a server error
    print("e")#show the error
  except URLError as e:#If URL does not exist
    print("Server could not be found")
  else:#If there are no errors
    html = BS(webpage.read(), "html.parser")
    

    latestResult1 = html.find('div',{'class':'smwfact'}).find('table',{'class':'smwfacttable'})
    stats2 = {}
    statsHtml = latestResult1.findAll('tr')
    for each in statsHtml:
      if(each.find('td',{'class':'smwpropname'})):
        stats2[each.find('td',{'class':'smwpropname'}).getText().replace(u'\xa0', ' ')] = each.find('td',{'class':'smwprops'}).getText().replace(u'\xa0', ' ')[:-3]
    
    return(stats2)
    


def codenamePage(title, url):
  print("scraping "+ url+"...")
  try:
    # Create target Directory
    mkdir(title.replace(" ","-"))
    print("Directory Created ") 
  except FileExistsError:
    print("Directory already exists")
  specsList = []
  sleep(1)
  try:
    webpage = urlopen(Request(url, headers={'User-Agent':'Mozilla/6.0'}))
  except HTTPError as e:#If there is a server error
    print("e")#show the error
  except URLError as e:#If URL does not exist
    print("Server could not be found")
  else:#If there are no errors
    html = BS(webpage.read(), "html.parser")
    #find list of cpus table
    latestResult = html.find('table',{'class':'infobox'})
    #WORKING HERE !!!!!
    # i can get some info from here but i need some from arch page

    #need to replace spaces with '_' 
    titleNew = title.replace(' ','_')
    latestResult = html.find('span',{'id':titleNew+'_Processors'}).parent
    latestResult = (latestResult.find_next_sibling('div').find('table'))
    #latestResult = html.findAll('table')[1]
    #print(latestResult)
    #below doesnt work because wikichip tables are inconsistant af
    #if("List of "+title+" Processors") in latestResult.getText():
    #  print("correct table found!!")
    tableRows = (latestResult.findAll('tr'))
    titles = []
    values = []
    for i in tableRows:
      th = i.findAll('th')
      if len(th) >4:
        for j in th:
          titles.append(j.getText())
        break
    print(titles)
    if titles != []:
      for i in tableRows:
        td = i.findAll('td')
        count = 0
        for j in td:
          temp = j.getText().replace(u'\xa0', ' ')

          nextUrl = j.find('a', href=True)
          if nextUrl:
            specsList.append(statsPage(BASE_URL + nextUrl['href'],title))

          count = count +1
      #doing smth here with specsList
        
      


while True:
  try:
    webpage = urlopen(req)#Open microarchitecture page
  except HTTPError as e:#If there is a server error
    print("e")#show the error
  except URLError as e:#If URL does not exist
    print("Server could not be found")
  else:#If there are no errors
    #Scrapes
    html = BS(webpage.read(), "html.parser")#the html is stored
    #find extensions
    #you can only find extensions on this page
    latestResult = html.find('table',{'class':'infobox'})
    labels = latestResult.findAll('td',{'class':'label'})
    values = latestResult.findAll('td',{'class':'value'})
    extensions = ''
    for i in range(len(labels)):
      if labels[i].getText() == "Extensions":
        extensions = values[i].getText()
        break
    #find list of codenames
    latestResult = html.find('div', {'id':'mw-content-text'}).find('table', {'class':'wikitable'})
    #find the href link
    latestResult = latestResult.findAll('a', href=True)
    for each in latestResult:
      if "/wiki/" in each["href"] and '/cores/' in each["href"]:
        print(each.getText())
        codenamePage(each.getText(),BASE_URL+each["href"])

    
    sleep(10)
