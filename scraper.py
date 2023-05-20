######
#
#Doesnt do APUs
#(CPUs with integrated graphics.)
#
#
######


import yaml
import datetime
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

def mapCPUData(cpuInfo):
  # Map the output to the expected format
  # WARNING : 
  # TODO : 
  ####### WIKICHIP CAN SOMETIMES USE DIFFERENT NAMES FOR THESE THINGS SO THIS HAS TO BE CONSIDERED.
  data = {}
  try:
    data['name'] = cpuInfo['name'].replace(" ","-")
    data['humanName'] = cpuInfo['name'] 
  except:
    print('name is not present. THIS NEEDS TO BE FOUND BEFORE PR. Perhaps the scraper failed as wikichip changed?')
  data['isPart'] = True
  data['type'] = 'CPU'
  try:
    data['inherits'] = [cpuInfo['core name'].replace(" ","-")]
  except:
    print('core name(inherits) is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  data['data'] = {}
  try:
    data['data']['Release Date'] = datetime.datetime.strptime(cpuInfo['first launched'], "%B %d, %Y").strftime("%Y-%m-%d")
  except:
    print('Release date is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L1 Cache (Data)'] = cpuInfo['l1d$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L1 Cache (Instruction)'] = cpuInfo['l1i$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L2 Cache (Total)'] = cpuInfo['l2$ size'].split(" (")[0]
  except:
    print('L2 Cache is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L3 Cache (Total)'] = cpuInfo['l3$ size'].split(" (")[0]
  except:
    print('L3 cache is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['TDP'] = cpuInfo['tdp'].split(" (")[0]
  except:
    print('TDP is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Core Count'] = int(cpuInfo['core count'].split(" (")[0])
  except:
    print('Core count is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Thread Count'] = int(cpuInfo['thread count'].split(" (")[0])
  except:
    print('Thread count is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Base Frequency'] = cpuInfo['base frequency'].split(" (")[0]
  except:
    print('Base frequency is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Boost Frequency'] = cpuInfo['turbo frequency'].split(" (")[0]
  except:
    print('Boost frequency is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Lithography'] = cpuInfo['process'].split(" (")[0]
  except:
    print('Lithography not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Sockets'] = [cpuInfo['socket']]#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
    data['data']['Socket'] = [cpuInfo['socket']]#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
  except:
    print('Socket is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Unlocked'] = not cpuInfo['has locked clock multiplier']
  except:
    print('overclockable(unlocked) is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Architecture'] = cpuInfo['microarchitecture']
  except:
    print('Architecture is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Memory Type'] = cpuInfo['supported memory type'].split('-')[0]
  except:
    print('Memory type is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Max Memory Frequency'] = cpuInfo['supported memory type'].split('-')[1] + " MHz" #This may not be consistent.
  except:
    print('Max memory frequency is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Max Memory Channels'] = int(cpuInfo['max memory channels'])
  except:
    print('Max memory channels not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Stepping'] = cpuInfo['core stepping']
  except:
    print('Core stepping is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  #XFR Support
  #All extensions: FMA4 FMA3 AVX AMD-V .etc

  
  #print(data)
  #with open('TEST.yaml', 'w') as outfile:
  #  yaml.dump(data, outfile, default_flow_style=False)
  return data

def mapInheritData(cpuInfo):
  # Map the output to the expected format
  data = {}
  data['name'] = cpuInfo['core name'].replace(" ","-")
  data['hidden'] = True
  data['data'] = {}
  try:
    data['data']['Release Date'] = datetime.datetime.strptime(cpuInfo['first launched'], "%B %d, %Y").strftime("%Y-%m-%d")
  except:
    print('Release date is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L1 Cache (Data)'] = cpuInfo['l1d$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L1 Cache (Instruction)'] = cpuInfo['l1i$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L2 Cache (Total)'] = cpuInfo['l2$ size'].split(" (")[0]
  except:
    print('L2 Cache is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['L3 Cache (Total)'] = cpuInfo['l3$ size'].split(" (")[0]
  except:
    print('L3 cache is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['TDP'] = cpuInfo['tdp'].split(" (")[0]
  except:
    print('TDP is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Core Count'] = int(cpuInfo['core count'].split(" (")[0])
  except:
    print('Core count is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Thread Count'] = int(cpuInfo['thread count'].split(" (")[0])
  except:
    print('Thread count is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Base Frequency'] = cpuInfo['base frequency'].split(" (")[0]
  except:
    print('Base frequency is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Boost Frequency'] = cpuInfo['turbo frequency'].split(" (")[0]
  except:
    print('Boost frequency is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Lithography'] = cpuInfo['process'].split(" (")[0]
  except:
    print('Lithography not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Sockets'] = [cpuInfo['socket']]#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
    data['data']['Socket'] = [cpuInfo['socket']]#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
  except:
    print('Socket is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Unlocked'] = not cpuInfo['has locked clock multiplier']
  except:
    print('overclockable(unlocked) is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Architecture'] = cpuInfo['microarchitecture']
  except:
    print('Architecture is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Memory Type'] = cpuInfo['supported memory type'].split('-')[0]
  except:
    print('Memory type is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Max Memory Frequency'] = cpuInfo['supported memory type'].split('-')[1] + " MHz" #This may not be consistent.
  except:
    print('Max memory frequency is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Max Memory Channels'] = int(cpuInfo['max memory channels'])
  except:
    print('Max memory channels not present. THIS NEEDS TO BE FOUND BEFORE PR')
  try:
    data['data']['Stepping'] = cpuInfo['core stepping']
  except:
    print('Core stepping is not present. THIS NEEDS TO BE FOUND BEFORE PR')
  #XFR Support
  #All extensions: FMA4 FMA3 AVX AMD-V .etc
  return data

def outputData(inherit,specs):
  title = inherit["core name"].replace(" ","-")
  inherit1 = mapInheritData(inherit)
  with open((title)+'-inherit.yaml', 'w') as outfile:
    yaml.dump(inherit1, outfile, default_flow_style=False)
  for each in specs:
    each1 = mapCPUData(each)
    with open((title)+'/'+ each['model number']+'.yaml', 'w') as outfile:
      yaml.dump(each1, outfile, default_flow_style=False)


def organiseData(specs):
  """
  This functions finds what data is to be added to the inherit file, and what attributes are unique to a CPU
  TODO : 
  1. change data to fit SpecDB (i.e.  first launched: January 12, 2021 -> Release Date: '2021-01-12')
  2. Might be best to put smth in inherit if its the same for 70%+ of the CPUs. just make sure the 30% dont remove the attribute
    (for example, most Vermeer CPUs came out much earlier than the 5800x3d.)

  Parameters
  ----------
  specs : list
    list dictionaries of specs
  
  Returns
  ----------
  dictionary
    dfjhgdlsjkfh
  """
  bigDictionary = {}
  #print(specs['name'])
  for each in specs:
    #below tests if it is a gpu or cpu
    if('integrated gpu' in each):
      preData = {'name':(each['name']).replace(" ","-"),'humanName':each['name'],'isPart':'true','type':'APU'}
    else:
      preData = {'name':(each['name']).replace(" ","-"),'humanName':each['name'],'isPart':'true','type':'CPU'}

    for dictionaryTitle in each:
      if dictionaryTitle in bigDictionary:
        bigDictionary[dictionaryTitle].append(each[dictionaryTitle])
      else:
        bigDictionary[dictionaryTitle] = [each[dictionaryTitle]]
  inherit = {}
  for dictionaryTitle in bigDictionary:
    if len(bigDictionary[dictionaryTitle]) == len(specs):
      #check if all the elements in the list are the same.
      if bigDictionary[dictionaryTitle].count(bigDictionary[dictionaryTitle][0]) == len(bigDictionary[dictionaryTitle]):
        #they are! put this in the inherit dictionary.
        inherit[dictionaryTitle] = bigDictionary[dictionaryTitle][0]
  #next is to remove the items that made it to the inherit dictionary from the induvidual cpu specs
  for dictionaryTitle in inherit:
    for each in specs:
      each.pop(dictionaryTitle)
  #print(inherit)
  #print(specs)
  return inherit,specs

#  with open((title.replace(" ","-"))+'/'+ each['model number']+'.yaml', 'w') as outfile:
#    yaml.dump(each, outfile, default_flow_style=False)

def statsPage(url, title):
  """
  Once the codename page has been scraped and induvidual CPUs are found,
  the stats for these CPUs get scraped here.

  Parameters
  ----------
  title : str
    The cpu name of the page we are scraping.
  url : str
    The CPU URL we are scraping.
  
  Returns
  ----------
  dictionary
    A dictionary of stats scraped from the webpage.
  """
  print("scraping "+ url+"...")
  sleep(1)
  try:
    webpage = urlopen(Request(url, headers={'User-Agent':'Mozilla/6.0'}))
  except HTTPError as e:#If there is a server error
    print(e)#show the error
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
  """
  Once the microarchitecture page has been scraped, the codename page gets scraped here.
  This method finds induvidual CPU pages to send to method statsPage()

  Parameters
  ----------
  title : str
    The Codename of the page we are scraping.
  url : str, optional
    The codename URL we are scraping.
  
  Returns
  ----------
  list
    A list of dictionaries of the cpu specs from that codename.
  """
  print("scraping "+ url+"...")
  #TODO : Test if this page is actually a codename page, if not, return an error.
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
    print(e)#show the error
  except URLError as e:#If URL does not exist
    print("Server could not be found")
  else:#If there are no errors
    html = BS(webpage.read(), "html.parser")
    #find list of cpus table
    #latestResult = html.find('div',{'class':'mw-data-after-content'}).find('table',{'class':'smwfacttable'})
    #WORKING HERE !!!!!

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
    return specsList
        
      


while True:
  try:
    webpage = urlopen(req)#Open microarchitecture page
  except HTTPError as e:#If there is a server error
    print(e)#show the error
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
        specsList = codenamePage(each.getText(),BASE_URL+each["href"])
        inherit, specs = organiseData(specsList)
        outputData(inherit,specs)

    
    sleep(10)
