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
    latestResult = html.find('table',{'class':'infobox'})
    latestResult1 = html.find('div',{'class':'smwfact'}).find('table',{'class':'smwfacttable'})
    stats2 = {}
    statsHtml = latestResult1.findAll('tr')
    for each in statsHtml:
      if(each.find('td',{'class':'smwpropname'})):
        stats2[each.find('td',{'class':'smwpropname'}).getText().replace(u'\xa0', ' ')] = each.find('td',{'class':'smwprops'}).getText().replace(u'\xa0', ' ')[:-3]
    
    with open((title.replace(" ","-"))+'/'+ stats2['model number']+'.yaml', 'w') as outfile:
      yaml.dump(stats2, outfile, default_flow_style=False)


def codenamePage(title, url):
  print("scraping "+ url+"...")
  try:
    # Create target Directory
    mkdir(title.replace(" ","-"))
    print("Directory Created ") 
  except FileExistsError:
    print("Directory already exists")
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
            statsPage(BASE_URL + nextUrl['href'],title)

          count = count +1
        
      


while True:
  try:
    webpage = urlopen(req)#Open hltv results page
  except HTTPError as e:#If there is a server error
    print("e")#show the error
  except URLError as e:#If URL does not exist
    print("Server could not be found")
  else:#If there are no errors
    #Scrapes
    html = BS(webpage.read(), "html.parser")#the html is stored
    #print(html)
    latestResult = html.find('div', {'id':'mw-content-text'}).find('table', {'class':'wikitable'})
    #print(latestResult)
    latestResult = latestResult.findAll('a', href=True)
    for each in latestResult:
      if "/wiki/" in each["href"] and '/cores/' in each["href"]:
        print(each.getText())
        codenamePage(each.getText(),BASE_URL+each["href"])

    
    sleep(10)
