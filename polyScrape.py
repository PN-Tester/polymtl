#scraper for polymtl classes
#written by : Pierre-Nicolas Allard-Coutu
import requests
from bs4 import BeautifulSoup

#--------------------------------------------------------------------------------CONSTANTS-----------------------------------------------------------------------------------------
#headers required to avoid 403 response
HEADERS = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','Accept-Encoding':'gzip, deflate, br','Accept-Language':'en-CA,en;q=0.9,fr-CA;q=0.8,fr;q=0.7,en-GB;q=0.6,en-US;q=0.5','Cache-Control':'max-age=0','Connection':'keep-alive','Cookie':'has_js=1; _ga=GA1.2.965074011.1578942585; _gid=GA1.2.1386198001.1578942585','Host':'www.polymtl.ca','If-Modified-Since':'Tue, 14 Jan 2020 00:50:50 GMT','If-None-Match':'1578963050-1','Sec-Fetch-Mode':'navigate','Sec-Fetch-Site':'none','Sec-Fetch-User':'?1','Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
	
#URL = "https://www.polymtl.ca/etudes/programmes/certificat-en-cyberenquete" #Preset URL for testing

#base URL for additional relative links
BASEURL = "https://www.polymtl.ca"


#--------------------------------------------------------------------------------CLASSES-------------------------------------------------------------------------------------------
class Course:
	def __init__(self, name, sigle, group, date, time, teacher):
		self.name = name
		self.sigle = sigle
		self.group = group
		self.date = date
		self.time = time
		self.teacher = teacher
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#we will store course objects in this array
course_array = []

#--------------------------------------------------------------------------------PRINT FOR DEBUGGIN--------------------------------------------------------------------------------
def printDebug(string):
	print("\n==========================================\n")
	print(string)
	print("\n==========================================\n")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------PRINT COURSE--------------------------------------------------------------------------------------
def printCourse(course):
	print("\n")
	print("SIGLE : "+course.sigle)
	print("COURSE : "+course.name)
	print("DATE : "+course.date)
	print("TIME : "+course.time)
	print("TEACHER : "+course.teacher)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getProgram():
	print("\nWelcome to polymtl schedule assistance tool")
	selection = 0
	while selection not in ['1','2','3','4','5']:
		selection = input("\n\tSelect a program\n\t[1] Cyberfraud\n\t[2] Cyberenquête\n\t[3] Cybersecurité\n\t[4] Réseautique et sécurité\n\t[5] Other\n\n>>")
	if selection == "1":
		URL = "https://www.polymtl.ca/programmes/programmes/certificat-en-cyberfraude"
	if selection == "2":
		URL = "https://www.polymtl.ca/programmes/programmes/certificat-en-cyberenquete"
	if selection == "3":
		URL = "https://www.polymtl.ca/programmes/programmes/certificat-en-cybersecurite-des-reseaux-informatiques"
	if selection == "4":
		URL = "https://www.polymtl.ca/programmes/programmes/microprogramme-de-1er-cycle-en-reseautique-et-securite"
	if selection == "5":
		URL = input("[?] Enter program URL\n>>")
	return URL


def initialize(URL):
	r = requests.get(URL,headers=HEADERS)
	soup = BeautifulSoup(r.content,'html.parser')
	content = soup.find_all(class_="contenu")
	
	print("[!] Acquired page source...\n")
	
	links = []
	
	for item in content:
		for elem in item.find_all('a',href=True):
			links.append(elem['href'])

			
	print("[!] Extracted links...\n")
	
	goodLinks = []
	
	for link in links:
		if link[0:11] == "/programmes":
			goodLinks.append(link)
			
	print("[!] Isolated targets...\n")
	
	goodLinks = list(dict.fromkeys(goodLinks))
	
	print("[!] Removed duplicate entries...\n")
	
	return goodLinks

def getData(goodLinks):
	print("[!] Extracting data...\n")
	
	for link in goodLinks:
		parse(link)


def parse(relative_link):
	global course_array
	try:
		r = requests.get(BASEURL+relative_link,headers=HEADERS)
		courseSoup = BeautifulSoup(r.content, 'html.parser')	
		
		#extract sigle
		raw_sigle = courseSoup.find_all(class_="sigle")
		raw_sigle = str(raw_sigle)			
		raw_sigle = raw_sigle.split('</i>')[1] #this now look like : CR300</h2>]
		raw_sigle = raw_sigle.split('<')[0] # now raw_sigle is isolated, there is a space in front, but i will not remove it for now...
		sigle = raw_sigle.strip() #raw_sigle[1:len(raw_sigle)] # now its perfect, just the sigle
		
		#extract name/title
		raw_name = courseSoup.find_all(class_ = "titre")
		raw_name = str(raw_name)
		raw_name = raw_name.split('</h3>')[0]
		name = raw_name.split('>')[1]
	
		#group is [5]
		#date is [6]
		#time is [7]
		#teacher is [9]
		
		raw_data = courseSoup.find('tbody') #get the table
		data = raw_data.find_all('td')
		
		#Extract Group
		raw_group = str(data[5])
		raw_group = raw_group.split('<td>')[1]
		group = raw_group.split('</td>')[0]
		
		#Extract Date
		raw_date = str(data[6])
		raw_date = raw_date.split('<td>')[1]
		date = raw_date.split('</td>')[0]
		
		#Extract Time
		raw_time = str(data[7])
		raw_time = raw_time.split('<td>')[1]
		time = raw_time.split('</td>')[0]
		
		#Extract Teacher
		raw_teacher = str(data[9])
		raw_teacher = raw_teacher.split('<td>')[1]
		teacher = raw_teacher.split('</td>')[0]
		
		course_array.append(Course(name,sigle,group,date,time,teacher))
		
		print('[+] Added Course : '+sigle+"\n")
	except:
		print('[-] Error getting course data, skipping...\n')
		pass

#now goodLinks contains only the links we want to follow for course details, we can follow them all and then parse the source for the info we want
#to do, implement multi threading without getting banned from Poly website.. xD


#===================================================================================================================================MAIN===============================================================================================================================
if __name__=='__main__':
	try:
		getData(initialize(getProgram()))
		
		for course in course_array:
			if course.group == 'Été':
				course_array.remove(course)
				
		for course in course_array:
			if course.time[0] not in ['0','1']:
				course_array.remove(course)
				
		print('[+] Removed invalid courses...\n')
		
		print("[+] Completed Successfully!\n")
		
		while(True):
			choice = input("\n[?] Select an action\n\t[1] Show Monday\n\t[2] Show Tuesday\n\t[3] Show Wednesday\n\t[4] Show Thursday\n\t[5] Show Friday\n\t[6] Show All\n\t[7] Exit\n>>")
			
			if choice == '1':
				for course in course_array:
					if course.date == "Lundi":
						printCourse(course)
			if choice == '2':
				for course in course_array:
					if course.date == "Mardi":
						printCourse(course)
			if choice == '3':
				for course in course_array:
					if course.date == "Mercredi":
						printCourse(course)
			if choice == '4':
				for course in course_array:
					if course.date == "Jeudi":
						printCourse(course)
			if choice == '5':
				for course in course_array:
					if course.date == "Vendredi":
						printCourse(course)
			if choice == '6':
				for course in course_array:
					if course.date == "Lundi":
						printCourse(course)
					if course.date == "Mardi":
						printCourse(course)
					if course.date == "Mercredi":
						printCourse(course)
					if course.date == "Jeudi":
						printCourse(course)
					if course.date == "Vendredi":
						printCourse(course)
			if choice == '7':
				exit(0)

	except KeyboardInterrupt:
	
		print('\n[!] EXITING PROGRAM\n')
		
		exit(0)

