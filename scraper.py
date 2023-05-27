######
#
#Doesnt do APUs
#(CPUs with integrated graphics.)
#
#
#
#######------TODO--------#######
#gpu base frequency
#gpu boost frequency
#fp32 compute
#render output unit count
#vram capacity
#GPU
#GPU Model
#Die size
#Module Count
#FP64 Compute
#XFR Frequency
#Shader Processing Count
#Texture mapping unit count
#VRAM Type
#VRAM frequency
#VRAM bandwidth
#VRAM bus width
#maximum VRAM capacity
#compatible chipsets
#XFR Support
#DirectX Support
#HLSL Shader model
#OpenGL support
#Vulkan support
#OpenCL Support
#Freesync support
#crossfire support
#max displays

#######------DONE--------#######
#Base frequency -
#boost frequency -
#core count -
#thread count -
#release date -
#TDP -
#Architecture -
#Codename
#Socket -
#Lithography -
#Stepping -
#L1 cache i -
#l1 cache d -
#l2 cache -
#l3 cache -
#max memory channels -
#memory type -
#max memory frequency -
#Unlocked -
#FMA4 bool
#FMA3 bool
#AES bool
#sha bool
#BMI {BMI2 BMI No}
#AVX/SSE/MMX (['AVX-512', 'AVX2', 'AVX',
#					'SSE 4.2', 'SSE 4.1', 'SSE4a', 'SSSE3', 'SSE3', 'SSE2', 'SSE', 
#					'EMMX', 'MMX',
#					'No'])
#other extensions
#
#
#
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
SLEEP_DURATION = 1.5


def mapCPUData(cpuInfo, title):
  """
  # Map the output to the expected format
  """
  # WARNING : 
  # TODO : 
  ####### WIKICHIP CAN SOMETIMES USE DIFFERENT NAMES FOR THESE THINGS SO THIS HAS TO BE CONSIDERED.
  if('integrated gpu' in each):
    apu = True
  else:
    apu = False
  data = {}
  try:
    data['name'] = cpuInfo['name'].replace(" ","-")
    data['humanName'] = cpuInfo['name'] 
  except:
    print('name is not present. Ignored. Perhaps the scraper failed as wikichip changed?')
  data['isPart'] = True
  data['type'] = 'CPU'
  try:
    data['inherits'] = [title]
  except:
    print('core name(inherits) is not present. Ignored')
  data['data'] = {}
  try:
    data['data']['Release Date'] = datetime.datetime.strptime(cpuInfo['first launched'], "%B %d, %Y").strftime("%Y-%m-%d")
  except:
    print('Release date is not present. Ignored')
  try:
    data['data']['L1 Cache (Data)'] = cpuInfo['l1d$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) is not present. Ignored')
  try:
    data['data']['L1 Cache (Instruction)'] = cpuInfo['l1i$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) not present. Ignored')
  try:
    data['data']['L2 Cache (Total)'] = cpuInfo['l2$ size'].split(" (")[0]
  except:
    print('L2 Cache is not present. Ignored')
  try:
    data['data']['L3 Cache (Total)'] = cpuInfo['l3$ size'].split(" (")[0]
  except:
    print('L3 cache is not present. Ignored')
  try:
    data['data']['TDP'] = cpuInfo['tdp'].split(" (")[0]
  except:
    print('TDP is not present. Ignored')
  try:
    data['data']['Core Count'] = int(cpuInfo['core count'].split(" (")[0])
  except:
    print('Core count is not present. Ignored')
  try:
    data['data']['Thread Count'] = int(cpuInfo['thread count'].split(" (")[0])
  except:
    print('Thread count is not present. Ignored')
  try:
    data['data']['Base Frequency'] = cpuInfo['base frequency'].split(" (")[0]
  except:
    print('Base frequency is not present. Ignored')
  try:
    data['data']['Boost Frequency'] = cpuInfo['turbo frequency'].split(" (")[0]
  except:
    print('Boost frequency is not present. Ignored')
  try:
    data['data']['Lithography'] = cpuInfo['process'].split(" (")[0]
  except:
    print('Lithography not present. Ignored')
  try:
    #data['data']['Sockets'] = cpuInfo['socket'].split(" and ")#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
    data['data']['Socket'] = cpuInfo['socket']#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
  except:
    print('Socket is not present. Ignored')
  try:
    data['data']['Unlocked'] = not cpuInfo['has locked clock multiplier']
  except:
    print('overclockable(unlocked) is not present. Ignored')
  try:
    data['data']['Architecture'] = cpuInfo['microarchitecture']
  except:
    print('Architecture is not present. Ignored')
  try:
    data['data']['Memory Type'] = cpuInfo['supported memory type'].split('-')[0]
  except:
    print('Memory type is not present. Ignored')
  try:
    data['data']['Max Memory Frequency'] = cpuInfo['supported memory type'].split('-')[1] + " MHz" #This may not be consistent.
  except:
    print('Max memory frequency is not present. Ignored')
  try:
    data['data']['Max Memory Channels'] = int(cpuInfo['max memory channels'])
  except:
    print('Max memory channels not present. Ignored')
  try:
    data['data']['Stepping'] = cpuInfo['core stepping']
  except:
    print('Core stepping is not present. Ignored')
  #XFR Support
  return data

def mapInheritData(cpuInfo, extensions):
  """
    Map the output to the expected format
  """
  data = {}
  data['hidden'] = True
  data['name'] = cpuInfo['core name'].replace(" ","-")
  data['data'] = {}
  try:
    data['data']['Release Date'] = datetime.datetime.strptime(cpuInfo['first launched'], "%B %d, %Y").strftime("%Y-%m-%d")
  except:
    print('Release date is not present. Ignored')
  try:
    data['data']['L1 Cache (Data)'] = cpuInfo['l1d$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) is not present. Ignored')
  try:
    data['data']['L1 Cache (Instruction)'] = cpuInfo['l1i$ size'].split(" (")[0]
  except:
    print('L1 Cache (Data) not present. Ignored')
  try:
    data['data']['L2 Cache (Total)'] = cpuInfo['l2$ size'].split(" (")[0]
  except:
    print('L2 Cache is not present. Ignored')
  try:
    data['data']['L3 Cache (Total)'] = cpuInfo['l3$ size'].split(" (")[0]
  except:
    print('L3 cache is not present. Ignored')
  try:
    data['data']['TDP'] = cpuInfo['tdp'].split(" (")[0]
  except:
    print('TDP is not present. Ignored')
  try:
    data['data']['Core Count'] = int(cpuInfo['core count'].split(" (")[0])
  except:
    print('Core count is not present. Ignored')
  try:
    data['data']['Thread Count'] = int(cpuInfo['thread count'].split(" (")[0])
  except:
    print('Thread count is not present. Ignored')
  try:
    data['data']['Base Frequency'] = cpuInfo['base frequency'].split(" (")[0]
  except:
    print('Base frequency is not present. Ignored')
  try:
    data['data']['Boost Frequency'] = cpuInfo['turbo frequency'].split(" (")[0]
  except:
    print('Boost frequency is not present. Ignored')
  try:
    data['data']['Lithography'] = cpuInfo['process'].split(" (")[0]
  except:
    print('Lithography not present. Ignored')
  try:
    #data['data']['Sockets'] = cpuInfo['socket'].split(" and ")#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
    data['data']['Socket'] = cpuInfo['socket']#TODO:EPYC-7443P sockets:SP3  + and LGA-4094
  except:
    print('Socket is not present. Ignored')
  try:
    data['data']['Unlocked'] = not cpuInfo['has locked clock multiplier']
  except:
    print('overclockable(unlocked) is not present. Ignored')
  try:
    data['data']['Architecture'] = cpuInfo['microarchitecture']
  except:
    print('Architecture is not present. Ignored')
  try:
    data['data']['Memory Type'] = cpuInfo['supported memory type'].split('-')[0]
  except:
    print('Memory type is not present. Ignored')
  try:
    data['data']['Max Memory Frequency'] = cpuInfo['supported memory type'].split('-')[1] + " MHz" #This may not be consistent.
  except:
    print('Max memory frequency is not present. Ignored')
  try:
    data['data']['Max Memory Channels'] = int(cpuInfo['max memory channels'])
  except:
    print('Max memory channels not present. Ignored')
  try:
    data['data']['Stepping'] = cpuInfo['core stepping']
  except:
    print('Core stepping is not present. Ignored')
  #XFR Support
  #All extensions: FMA4 FMA3 AVX AMD-V .etc
  #Gotta make extensions from string to list.
  extensionsL = extensions.split(", ")
  if 'FMA4' in extensionsL:
    data['data']['FMA4'] = True
    extensionsL.remove('FMA4')
  else:
    data['data']['FMA4'] = False
  if 'FMA3' in extensionsL:
    data['data']['FMA3'] = True
    extensionsL.remove('FMA3')
  else:
    data['data']['FMA3'] = False
  if 'AES' in extensionsL:
    data['data']['AES'] = True
    extensionsL.remove('AES')
  else:
    data['data']['AES'] = False
  #SHA
  if 'SHA' in extensionsL:
    data['data']['SHA'] = True
    extensionsL.remove('SHA')
  else:
    data['data']['SHA'] = False
  #BMI
  if 'BMI2' in extensionsL:
    data['data']['BMI'] = 'BMI2'
    extensionsL.remove('BMI2')
    extensionsL.remove('BMI')
  elif 'BMI' in extensionsL:
    data['data']['BMI'] = 'BMI'
    extensionsL.remove('BMI')
  else:
    data['data']['BMI'] = 'No'
  #AVX/SSE/MMX
  if 'AVX-512' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'AVX-512'
    if 'AVX-512' in extensionsL: extensionsL.remove('AVX-512')
    if 'AVX2' in extensionsL: extensionsL.remove('AVX2')
    if 'AVX' in extensionsL: extensionsL.remove('AVX')
    if 'SSE4.2' in extensionsL: extensionsL.remove('SSE4.2')
    if 'SSE4.1' in extensionsL: extensionsL.remove('SSE4.1')
    if 'SSE4a' in extensionsL: extensionsL.remove('SSE4a')
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'AVX2' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'AVX2'
    if 'AVX2' in extensionsL: extensionsL.remove('AVX2')
    if 'AVX' in extensionsL: extensionsL.remove('AVX')
    if 'SSE4.2' in extensionsL: extensionsL.remove('SSE4.2')
    if 'SSE4.1' in extensionsL: extensionsL.remove('SSE4.1')
    if 'SSE4a' in extensionsL: extensionsL.remove('SSE4a')
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'AVX' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'AVX'
    if 'AVX' in extensionsL: extensionsL.remove('AVX')
    if 'SSE4.2' in extensionsL: extensionsL.remove('SSE4.2')
    if 'SSE4.1' in extensionsL: extensionsL.remove('SSE4.1')
    if 'SSE4a' in extensionsL: extensionsL.remove('SSE4a')
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSE4.2' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSE 4.2'
    if 'SSE4.2' in extensionsL: extensionsL.remove('SSE4.2')
    if 'SSE4.1' in extensionsL: extensionsL.remove('SSE4.1')
    if 'SSE4a' in extensionsL: extensionsL.remove('SSE4a')
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSE4.1' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSE 4.1'
    if 'SSE4.1' in extensionsL: extensionsL.remove('SSE4.1')
    if 'SSE4a' in extensionsL: extensionsL.remove('SSE4a')
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSE4a' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSE4a'
    if 'SSE4a' in extensionsL: extensionsL.remove('SSE4a')
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSSE3' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSSE3'
    if 'SSSE3' in extensionsL: extensionsL.remove('SSSE3')
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSE3' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSE3'
    if 'SSE3' in extensionsL: extensionsL.remove('SSE3')
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSE2' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSE2'
    if 'SSE2' in extensionsL: extensionsL.remove('SSE2')
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'SSE' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'SSE'
    if 'SSE' in extensionsL: extensionsL.remove('SSE')
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'EMMX' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'EMMX'
    if 'EMMX' in extensionsL: extensionsL.remove('EMMX')
    if 'MMX' in extensionsL: extensionsL.remove('MMX')
  elif 'MMX' in extensionsL:
    data['data']['AVX/SSE/MMX'] = 'MMX'
    extensionsL.remove('MMX')
  else:
    data['data']['AVX/SSE/MMX'] = 'No'
  data['data']['Other Extensions'] = extensionsL
  return data

def mapMainData(title,cpuNameData):
  data = {}
  data['name'] = title
  data['humanName'] = title.replace("-"," ")
  data['type'] = 'CPU Architecture'
  data['data'] = {}
  data['sections'] = {}
  data['sections']['Data to be changed'] = cpuNameData

  return data

def outputData(inherit,specs, extensions, cpuNameData):
  """
  This functions outputs the data into YAML files. It calls mapCPUData and mapInheritData to map the wikichip data to SpecDB data.
  """
  title = inherit["core name"].replace(" ","-")
  with open((title)+'.yaml', 'w') as outfile:
    yaml.dump(mapMainData(title,cpuNameData), outfile, default_flow_style=False, sort_keys=False)
  inherit1 = mapInheritData(inherit, extensions)
  with open((title)+'-inherit.yaml', 'w') as outfile:
    yaml.dump(inherit1, outfile, default_flow_style=False, sort_keys=False)
  for each in specs:
    each1 = mapCPUData(each, title)
    with open((title)+'/'+ each['name']+'.yaml', 'w') as outfile:
      yaml.dump(each1, outfile, default_flow_style=False, sort_keys=False)


def organiseData(specs):
  """
  This functions finds what data is to be added to the inherit file, and what attributes are unique to a CPU
  TODO : 
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
  cpuNameDictionary = {}
  #print(specs['name'])
  for each in specs:
    cpuNameDictionary[each['name']] = [each['model number']]
    
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
  return inherit,specs,cpuNameDictionary

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
  print("scraping stats page "+ url+"...")
  sleep(SLEEP_DURATION)
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
  print("scraping codename page "+ url+"...")
  #TODO : Test if this page is actually a codename page, if not, return an error.
  try:
    # Create target Directory
    mkdir(title.replace(" ","-"))
    print("Directory Created ") 
  except FileExistsError:
    print("Directory already exists")
  specsList = []
  sleep(SLEEP_DURATION)
  try:
    webpage = urlopen(Request(url, headers={'User-Agent':'Mozilla/6.0'}))
  except HTTPError as e:#If there is a server error
    print(e)#show the error
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
    #print(titles)
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
  print("Make sure to delete the APU data it gives you. This wont be correct.")
  url = input("Enter a wikichip microarchitecture page like:https://en.wikichip.org/wiki/amd/microarchitectures/zen_3\n")
  if "wikichip.org/wiki" in url:
    req = Request(url, headers={'User-Agent':'Mozilla/6.0'})
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
          #print(each.getText())
          specsList = codenamePage(each.getText(),BASE_URL+each["href"])
          inherit, specs, cpuNameData = organiseData(specsList)
          outputData(inherit,specs, extensions, cpuNameData)

      
  url=""
