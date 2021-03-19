import time, random, csv, sys
import argparse
import winsound
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta

from config import username, password, job_urls, job_title_rejections, job_company_rejections, main_page, questionAndAnswer

class EasyApplyBot:


    def __init__(self, args, url):
    
        
        file = open('infoOutput.txt', 'r')
        temp = file.readlines()
        self.appliedToJobs = int(temp[1])
        self.failedToApplyJobs = int(temp[3])
        self.urls = url
        file.close()
        print('Total Jobs Successfully applied to: %d' % self.appliedToJobs) 
        print('Total Jobs that Failed to Apply: %d' % self.failedToApplyJobs) 
        
        self.sleepMulti = 1.5

        self.args = args
        if self.args.slowInternet:
            self.sleepMulti = 3
        self.options = self.browser_options()
        self.browser = webdriver.Chrome(executable_path = 'C:\\Users\josep\.wdm\drivers\chromedriver\win32\88.0.4324.96\chromedriver.exe', options=self.options, )
        
        self.inForm = False
        self.alreadyApplied = False
        self.typedLetter = False
        self.previousURL = ''
        self.majorErrorCount = 0
        self.majorErrorJustHappened = False
        self.majorErrorCutOff = 10
        self.stopApplication = False
        self.wait = WebDriverWait(self.browser, 30)
        self.browser.maximize_window()
      
      
    def browser_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        options.add_experimental_option('useAutomationExtension',False)
        
        #options.binary_location = "./chromedriver.exe"
        

        #Disable webdriver flags or you will be easily detectable
        options.add_argument("--disable-blink-features=AutomationControlled")
        return options
        
    def start_up(self):
        self.browser.get(main_page)
        
        time.sleep(random.uniform(1,3) * self.sleepMulti)
        
        signInButton = self.browser.find_element_by_xpath('//*[@id="gnav-main-container"]/div/div[1]/div/div[3]/div[3]/a').click()
        
        time.sleep(random.uniform(1,3) * self.sleepMulti)
        
        self.login()
  
        
    def login(self):
        print('Login')
        
        # Select the username element and input the stored username
        select_username = self.browser.find_element_by_xpath('//*[@id="login-email-input"]')
        select_username.send_keys(username)
        
        # Select the password element and input the stored password
        select_password = self.browser.find_element_by_xpath('//*[@id="login-password-input"]')
        select_password.send_keys(password)
        ## press ENTER key 
        select_password.send_keys(Keys.ENTER)
        
        time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))

            
        expectedURL = 'https://www.indeed.com/'
        
        # If we have not reached the expected URL, that means we hit a captcha and the bot needs user input
        if not self.check_target_url(expectedURL):
            print('captcha at login')
            winsound.Beep(2000,2000)
            time.sleep(30 * self.sleepMulti)
            
            select_password = self.browser.find_elements_by_xpath('//*[@id="login-password-input"]')
            if select_password:
                select_password[0].send_keys(password)
                select_password[0].send_keys(Keys.ENTER)
        
        
        print('Finished login')
        
    def find_jobs(self):
        print("Finding Jobs")
        
        startDifferent = True
        
        URL_list = []
        
        
        # Takes the URL function to start the program on a specific spot in the URL list.
        if int(args.url) != 99:
            for i in range(int(args.url), len(job_urls)):
                URL_list.append(self.urls[i])
        else:
            URL_list = self.urls  

        print(URL_list)
                 
        # For each URL in our stored URL,
        for counturl in range(0, len(URL_list)):
            oneMore = False
            done = False
            
            # Set the current URL to be the stored URL
            useThisURL = URL_list[counturl]
            
            # Print out what the URL currently is
            print('New URL : ' + useThisURL)
            
            # Manipulate the URL if the bot was told to start elsewhere
            if startDifferent:
                startDifferent = False
                useThisURL = useThisURL + '&start=' + str(args.start)
                
            
            self.browser.get(useThisURL)
            
            time.sleep(1 * self.sleepMulti + random.uniform(.1,1))
            
            
            
            while done == False:
                # If we cannot find the main element, Then we found an extra captcha. Shouldnt occur anymore but still can happen
                nextPageParent = self.browser.find_elements_by_xpath('//*[@id="resultsCol"]/nav/div/ul')
                if not nextPageParent:
                    print('EXTRA CAPTCHA')
                    winsound.Beep(3000,3000)
                    time.sleep(30 * self.sleepMulti)
                    
                    
                # If we had a captcha and cleared through it, we need to get the main element again
                nextPageParent = self.browser.find_elements_by_xpath('//*[@id="resultsCol"]/nav/div/ul')
                childrenNext = nextPageParent[0].find_elements_by_xpath("./*")
                
                # Function to scroll down the entire page to appear more human
                self.load_page()
                
                nextButton = ''
                
                
                time.sleep(1 + random.uniform(.1,.5))
                
                # Find the next button
                for children in childrenNext:
                    
                    temp = children.find_elements_by_tag_name('a')
                    if temp:
                        if temp[0].get_attribute('aria-label') == 'Next':
                            nextButton = children

                
                # If we cannot find the next page button, finish out this page and quit
                if not nextButton:
                    print('One more Run')
                    oneMore = True
                
                    
                    
                
                self.doTheStuff()
                
                # If we did find the next page button, continue and loop
                if oneMore == False:
                    nextButton.click()
                    time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                # If we did not find the next page button and we have finished with doTheStuff, we are finished
                else:
                    done = True
                
           
    # Major function that determines company information and writes information to output files
    def doTheStuff(self):
        jobElements = self.browser.find_elements_by_class_name('jobsearch-SerpJobCard')
        href = ['0'] * len(jobElements)
        companyName = [''] * len(jobElements)
        salary = [''] * len(jobElements)
        title = [''] * len(jobElements)
        
        sleepInMs = 0
        sleepHowLongMins = 0
        firstCheckTime = 0
        
        
        # Load things from element. This is what the bot prints out when applied/failed jobs occur
        for j in range(0, len(jobElements)):
            hrefTitle = jobElements[j].find_element_by_class_name('title')    
            href[j] = hrefTitle.find_elements_by_tag_name('a')[0].get_attribute('href')
            temp = jobElements[j].find_elements_by_class_name('company')
            if temp:
                companyName[j] = temp[0].text
            temp = jobElements[j].find_elements_by_tag_name('a')
            if temp:
                title[j] = temp[0].get_attribute('title')
            temp = jobElements[j].find_elements_by_class_name('salaryText')
            if temp:
                salary[j] = temp[0].text
        
        # This is to help keep the bot from going to previously applied links
        previouslyAppliedJobs = []
        with open('skipJobs.csv', 'r') as csvfile: 
            for line in csvfile.readlines():
                if line != '\n':
                    previouslyAppliedJobs.append(line[:-1])
        
        # We need to set the values.
        if sleepInMins == 0:
            sleepInMins = random.randint(20,40)
            sleepHowLongMins = random.uniform(3,5)
            firstCheckTime = time.time()
            print('Will sleep in ' + sleepInMins + ' minutes')
        
        # We need to time out for a predetermined amount of time. Looks more bot like. Only occurs at new pages
        if firstCheckTime + (sleepInMins * 60) >= time.time():
            print('Time to sleep. Will be back in ' + sleepHowLongMins + ' minutes')
            time.sleep(sleepHowLongMins * 60)
            sleepInMins = 0
        
        # For each of the links found on the job elements,
        for i in range(0, len(href)):
            previouslyApplied = False
            
            # If the href is in the previously applied list, we need to skip this job
            for link in previouslyAppliedJobs:
                if href[i] == link: 
                    previouslyApplied = True
                    print('Upcoming job application has already been attempted')
                    break
            # If not, continue as normal
            if not previouslyApplied:
            
                self.openTab(href[i])
                
                time.sleep(1 * self.sleepMulti * random.uniform(.1,.5))
                
                # If our click_apply() function has returned false, that means there is either an error, outside link, or a previously applied to job.
                if self.click_apply() == False or self.checkIfReject() == False:
                    # Break from this loop
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    
                # If we clicked on the apply button, continue
                else:
                
                    # Load the page as previously performed. We slowly scroll to the bottom of the page. Act Human.
                    self.load_page()
                
                    self.inForm = False
                    
                    cletter = self.gen_Cover_Letter(companyName[i])
                    # If our question_handler has returned true, we know we successfully applied to this job and we need to increment our output counters.
                    if self.question_handler(cletter) == True:
                        # Write how many jobs we have applied to to the information file
                        # Read in the information
                        self.appliedToJobs += 1
                        file = open('infoOutput.txt', 'r')
                        temp = file.readlines()
                        file.close()
                        # Write modified the information
                        file = open('infoOutput.txt', 'w')
                        temp[1] = str(self.appliedToJobs) + '\n'
                        file.writelines(temp)
                        file.close()
                        # add the job information to the jobApplied csv file
                        with open('jobsApplied.csv', mode='a') as data:
                            dataWriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            dataWriter.writerow([companyName[i],title[i],salary[i],href[i]])
                            

                            
                    # Failed to apply to this job, save the information
                    else:
                        # If we failed to apply to the job AND we havent applied to it before
                        if self.alreadyApplied == False:
                            self.failedToApplyJobs += 1
                            file = open('infoOutput.txt', 'r')
                            temp = file.readlines()
                            file.close()

                            file = open('infoOutput.txt', 'w')
                            temp[3] = str(self.failedToApplyJobs) + '\n'
                            file.writelines(temp)
                            file.close()
                            
                            try:
                                with open('jobsFailed.csv', mode='a') as data:
                                    dataWriter = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                    dataWriter.writerow([companyName[i],title[i],salary[i],href[i]])
                            except:
                                print('Writing Error. Moving On')
                            
                            
                    # Close the current tab and continue
                    self.browser.close()
                    self.browser.switch_to.window(self.browser.window_handles[0])
                    self.typedLetter = False
                    self.alreadyApplied = False
                    # Save every link we visit so we dont visit it again
                    file = open('skipJobs.csv', 'a')
                    file.writelines(href[i]+ '\n') 
                    file.close()
                    time.sleep(1 + random.uniform(.1,.5))
                    
                    #self.browser.find_element_by_tag_name('body').send_keys(Keys.ENTER)
                    temp = self.browser.find_elements_by_xpath('//*[@id="popover-x"]/button')
                    if temp:
                        if temp[0].is_displayed():
                            temp[0].click()
                  
                    

    def checkIfReject(self):
        temp = self.browser.find_elements_by_xpath('//*[@id="viewJobSSRRoot"]/div[1]/div[3]/div[1]/div[1]/h1')
        if temp:
            for i in range(0,len(temp)):
                for j in job_title_rejections:
                    if j.lower() in temp[i].text.lower():
                        print('Found a job title that meets rejection')
                        return False
        temp = self.browser.find_elements_by_xpath('//*[@id="viewJobSSRRoot"]/div[1]/div[3]/div[1]/div[2]/div/div/div[1]/div')
        if temp:
            for i in range(0,len(temp)):
                for j in job_company_rejections:
                    if j.lower() in temp[i].text.lower():
                        print('Found a company that meets rejection')
                        return False
        return True
    
    # Simple return function that takes the company name and inputs it into a return string that gets put into the cover letter section of the application
    def gen_Cover_Letter(self, companyName):
        string = 'Dear Hiring Manager at ' + companyName + ', I am a hiring assistant for Joseph Cantrell. I was coded and made specifically to help him find jobs while he tries to stay afloat during this pandemic. I am made using Python and Selenium. If you would like to know more about him or this bot, please look at the resume attached. I apologize if I missed any optional questions, I am unable to answer every question automatically. Please contact Joseph Cantrell at josephcantrell@josephdcantrell.com for any clarification. Thank you'
        return string
        
    # Compare the current URL with a target URL. If they are the same, return true, else false.
    def check_target_url(self, targetURL):
        if self.browser.current_url == targetURL:
            return True
        return False

    # Function to click on the apply button.
    def click_apply(self):
        # Check for outside links. dont want them
        time.sleep(1 + random.uniform(.1,.5))
        
        # Outside link
        if len(self.browser.find_elements_by_class_name('icl-Button icl-Button--branded icl-Button--lg icl-Button--md')) > 0:
            return False
        # Outside Link
        if len(self.browser.find_elements_by_xpath('//*[@id="applyButtonLinkContainer"]/div/div[2]/a')) > 0:
            return False
        # Already Applied to button
        temp = self.browser.find_elements_by_xpath('//*[@id="saveJobButtonContainer"]/div/div/div/div[2]/button')
        if len(temp) > 0:
            if temp[0].text == 'Applied':
                print('Already Applied in Click Apply')
                return False
    
        temp = self.browser.find_elements_by_xpath('//*[@id="indeedApplyWidget"]/div[2]/button')
        # We found the button and should click on it.
        if temp:
            temp[0].click()
        # This means there is a captcha or a loading error.
        else:
            return False
            
    # This is the scrolling function. Slowly scrolls to the bottom of a page.
    def load_page(self):
        scroll_page = 0
        while scroll_page < 4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
            scroll_page += 200
            time.sleep(random.uniform(.1,.25))

            
    # This function takes and figures out what type of question system we got, and then determines what needs to go where
    def question_handler(self, letter):
        time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
        try:
            self.majorErrorJustHappened = False
            # some new beta version of applying. completly different than the popup window.
            if 'm5' in self.browser.current_url:
                # Find the continue button. Tells us if everything is still okay
                cont_button = self.browser.find_elements_by_xpath('//*[@id="ia-container"]/div/div[1]/main/div/div/div/div[2]/div/button')
                if cont_button:
                    # If we need to select our uploaded resume over the default indeed resume
                    if len(self.browser.find_elements_by_xpath('//*[@id="ia-container"]/div/div[1]/main/div/div/div/div[1]/div[3]/div/div/div[1]/div/div/div[1]/p[2]')) > 0:
                        self.browser.find_element_by_xpath('//*[@id="ia-container"]/div/div[1]/main/div/div/div/div[1]/div[3]/div/div/div[1]/div/div/div[1]/p[2]').click()
                        time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                        
                    # If the cover letter button is present on the current page, click it and write the gen_Cover_Letter return value
                    if len(self.browser.find_elements_by_xpath('//*[@id="write-coverlter-selection-card"]')) > 0:
                        if not self.typedLetter:
                            coverLetter = self.browser.find_element_by_xpath('//*[@id="write-coverlter-selection-card"]').click()
                            time.sleep(1 * self.sleepMulti + random.uniform(.1,1))
                            coverLetter = self.browser.find_element_by_xpath('//*[@id="coverletter-textarea"]')
                            coverLetter.click()
                            coverLetter.send_keys(Keys.CONTROL + "a");
                            coverLetter.send_keys(Keys.DELETE);
                            coverLetter.send_keys(letter)
                            time.sleep(1 * self.sleepMulti + random.uniform(.1,1))
                            self.typedLetter = True
                        
                    # Determine all of the text areas on the page
                    textareas = self.browser.find_elements_by_xpath('//*[starts-with(@id, "q_")]/div')
                    textinputs = []
                    questions = []
                    questions = []
                    # If there are text areas, determine what the text value is and store it. Store the location of the input field as well
                    if textareas:
                        for item in textareas:
                            text_item = item.text
                            if text_item:
                                questions.append(text_item.lower())
                                xpath_textarea = item.find_elements_by_xpath('.//textarea')
                                if xpath_textarea:
                                    textinputs.append(xpath_textarea[0])
                                xpath_inputarea = item.find_elements_by_xpath('.//input')
                                if xpath_inputarea:
                                    textinputs.append(xpath_inputarea[0])
                                    
                    # For each of the questions we just found, we need to determine what to put
                    for i in range(0, len(questions)):
                        foundAnswer = False
                        try:
                            a = questions[i].lower()
                            b = textinputs[i]
                        except:
                            pass
                        # Cycle through all of the questionAndAnswer values in the config file. 
                        for j in range(0, int(len(questionAndAnswer)/2)):
                            # If we found a matching answered question, we need to input it
                            if questionAndAnswer[j*2].lower() in a:
                                # Need a try and except block due to the occasional radio button getting through and breaking
                                try:
                                    # If there is not a value already present on the question
                                    if b.get_attribute('value') == '':
                                        b.click()
                                        b.send_keys(Keys.CONTROL + "a");
                                        b.send_keys(Keys.DELETE);
                                        b.send_keys(questionAndAnswer[(j*2)+1])
                                        foundAnswer = True
                                except:
                                    return False

                        # If we did not have an answer, we need to save the question to a file for later adding
                        if foundAnswer == False:
                            # no answer to the question:
                            file = open('noAnswers.txt','a')
                            file.write('No Answer: %s\n' % a)
                            file.close()
                    # If the continue button is not greyed out, click it.
                    if cont_button[0].is_enabled():
                        cont_button[0].click()
                    else:
                        print('Cont button not enabled. Question not filled out. Quitting')
                        return False
                        
                    
                    self.previousURL == self.browser.current_url
                    # Loop again
                    return self.question_handler(letter)
                # No continue button, we are near the end.
                else:
                    capcha = self.browser.find_elements_by_xpath('//*[@id="rc-anchor-container"]')
                    if capcha:
                        winsound.Beep(2500, 2000)
                        print('capcha present need to handle it')
                    # If no captcha
                    else:
                        apply_button = self.browser.find_elements_by_xpath('//*[@id="form-action-submit"]')
                        if apply_button:
                            apply_button[0].click()
                            time.sleep(1 * self.sleepMulti + random.uniform(.1,1))
                            print('M5 Found apply button')
                            return True
                        review_button = self.browser.find_elements_by_name('ia-pageButtonGroup-exit')
                        if review_button:
                            review_button.find_element_by_xpath('./button')
                            self.alreadyApplied = True
                            print('M5 Review button? We are quitting for some reason?')
                            return False
                        
            
            # Popup window
            else:
                if self.inForm == False:
                    temp = self.browser.find_elements_by_xpath('//*[@title="Job application form container"]')
                    # If we got a website error "We are unable to process the application for this job. Please contact the employer directly to apply." 
                    if temp:
                        self.browser.switch_to.frame(temp[0])
                    
                        self.browser.switch_to.frame(self.browser.find_element_by_xpath('/html/body/iframe'))
                        self.inForm = True
                    else:
                        return False
                    
                    
                if self.browser.find_elements_by_class_name('ia-GlobalErrors'):
                    return False
                
                cont_button = self.browser.find_elements_by_xpath('//*[@id="form-action-continue"]')
                if cont_button:
                
                    questionParent = self.browser.find_element_by_xpath('//*[@id="ia-ApplyFormScreen"]/div[2]/form/div[2]')
                    
                    childElements = questionParent.find_elements_by_xpath("./*")
                    # This for loop could be changed to use the .is_displayed() function, but for now it works.
                    # Determines if the element we are in actually contains what we are looking for. 
                    for i, elements in enumerate(childElements):
                        className = childElements[i].get_attribute('class')
                        # If our class name is not 'ia-Paginator-hiddenPage', that is the element we need
                        if className != 'ia-Paginator-hiddenPage':
                            time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                            childDriver = childElements[i]
                            # We need to change from the default indeed resume and select our own
                            if len(childDriver.find_elements_by_class_name('ia-BoxResumeSelector')) > 0:
                                resumeBox = childDriver.find_elements_by_class_name('ia-BoxResumeSelector-box')
                                if len(resumeBox) == 2:
                                    resumeBox[1].click()
                                    time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                                    break
                            # We need to click on the cover letter button.
                            if len(childDriver.find_elements_by_class_name('ia-AddCoverLetter')) > 0:
                                if not self.typedLetter:
                                    # If we cannot click on the cover letter button, we need to break;
                                    try:
                                        coverLetterClick = childDriver.find_element_by_class_name('icl-Button').click()
                                    except:
                                        break
                                    try:
                                        coverLetter = childDriver.find_element_by_xpath('//*[@id="textarea-applicant.applicationMessage"]')
                                    except:
                                        break
                                    time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                                    coverLetter.send_keys(letter)
                                    time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                                    self.typedLetter = True
                                    break
                            # This one does not currently work. When applying and you dont have the exact skill requirements, 
                            # The bot needs to click on the continue applying button. Not sure why it is not currently working.
                            if len(childDriver.find_elements_by_xpath('//*[@id="ia-ApplyFormScreen"]/div/form/div[2]/div[3]/div/div[2]/button[1]')) > 0:
                                childDriver.find_elements_by_xpath('//*[@id="ia-ApplyFormScreen"]/div/form/div[2]/div[3]/div/div[2]/button[1]')[0].click()
                                print('Clicked on continue applying button')
                                return self.question_handler(letter)
                                
                            # Relevant Job Experience Title
                            # Broke for some odd reason. Will be fixing
                            temp = childDriver.find_elements_by_id('input-applicant.jobTitle')
                            if temp:
                                try:
                                    temp[0].click()
                                    temp[0].send_keys(Keys.CONTROL + "a");
                                    temp[0].send_keys(Keys.DELETE);
                                    temp[0].send_keys('Freelance Software Developer')
                                    time.sleep(1 + random.uniform(.1,.5))
                                except:
                                    print('Tried to click on job title when i wasnt supposed to. im dumb')
                            # Relevant Job Experience Company Name
                            # Broke for some odd reason. Will be fixing
                            temp = childDriver.find_elements_by_id('input-applicant.companyName')
                            if temp:
                                try:
                                    temp[0].click()
                                    temp[0].send_keys(Keys.CONTROL + "a");
                                    temp[0].send_keys(Keys.DELETE);
                                    temp[0].send_keys('Personal')
                                    time.sleep(1 + random.uniform(.1,.5))
                                except:
                                    print('Tried to click on relevant company name when i wasnt supposed to. im dumb')
                          
                    # Same as before
                    textareas = self.browser.find_elements_by_xpath('//*[starts-with(@id, "q_")]/div')
                    textinputs = []
                    questions = []
                    if textareas:
                        for item in textareas:
                            text_item = item.text
                            if text_item:
                                questions.append(text_item.lower())
                                xpath_textarea = item.find_elements_by_xpath('.//textarea')
                                if xpath_textarea:
                                    textinputs.append(xpath_textarea[0])
                                xpath_inputarea = item.find_elements_by_xpath('.//input')
                                if xpath_inputarea:
                                    textinputs.append(xpath_inputarea[0])
                    
                    
                    


                    for i in range(0, len(questions)):
                        foundAnswer = False
                        try:
                            a = questions[i].lower()
                            b = textinputs[i]
                        except:
                            pass
                        for j in range(0, int(len(questionAndAnswer)/2)):
                            if questionAndAnswer[j*2].lower() in a:
                                try:
                                    if b.get_attribute('value') == '':
                                        b.click()
                                        b.send_keys(Keys.CONTROL + "a");
                                        b.send_keys(Keys.DELETE);
                                        b.send_keys(questionAndAnswer[(j*2)+1])
                                        foundAnswer = True
                                except:
                                    return False
                        
                        if 'country' in a:
                            dropdown = self.browser.find_elements_by_xpath('//*[@id="select-0"]')
                            if dropdown:
                                dropdown[0].click()
                                dropdown[0].send_keys('u')
                                dropdown[0].send_keys(Keys.ENTER)
                        
                        # no answer to the question:
                        if foundAnswer == False:
                            
                            file = open('noAnswers.txt','a')
                            file.write('No Answer: %s\n' % a)
                            file.close()
                        
                        time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
                    if cont_button[0].is_enabled():
                        try:
                            cont_button[0].click()
                        except:
                            print('Error when clicking continue button. probably slow loading speed')
                    else:
                        return False
                    return self.question_handler(letter)
                else:
                    capcha = self.browser.find_elements_by_xpath('//*[@id="rc-anchor-container"]')
                    if capcha:
                        winsound.Beep(2500, 2000)
                        print('capcha present need to handle it')
                    else:
                        
                        apply_button = self.browser.find_elements_by_xpath('//*[@id="form-action-submit"]')
                        # We have the submit button
                        if apply_button:
                            apply_button[0].click()  
                            time.sleep(3 * self.sleepMulti + random.uniform(.1,.5))
                            
                            return True
                        # We have the "You already applied to this job"
                        else:
                            self.alreadyApplied = True
                            return False
        except:            
            print('Exception occured while applying to this job. Trying again')
            self.question_handler(letter)
            if self.majorErrorJustHappened:
                self.majorErrorCount += 1
                if self.majorErrorCount >= self.majorErrorCutOff:
                    self.quitApplication()
            self.majorErrorJustHappened = True

    # Function to open tabs. Cleans the code up a bit.
    def openTab(self, url):
        self.browser.execute_script("window.open('');")
        # Switch to the new window
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.get(url)
        time.sleep(1 * self.sleepMulti + random.uniform(.1,.5))
        
    
    # Main running code.
    def startApp(self):
        self.start_up()
        self.find_jobs()
        
    def quitApplication(self):
        sys.exit('Encountered more than ' + str(self.majorErrorCutOff) + ' times. Stopping the program. Most likely got hit by Indeed bot detection')
        
        
# Arg parse stuff
parser = argparse.ArgumentParser(description='Indeed Automatic Job Applications')
parser.add_argument('-s','--start', help='Start the program with a specific starting location on the first URL', required=False,default='0')
parser.add_argument('-u','--url', help='Start the program with a specific URL', required=False,default='99')
parser.add_argument('-slow','--slowInternet', help='Enable this if you need more time for each page to load', required=False ,action='store_true' ,default=False)
args = parser.parse_args()

# Print statement to choose the time frame to search between
print('Choose the time frame to search from')
print('0: Over 14 days')
print('1: 14 days and below')
print('2: 7 days and below')
print('3: 3 days and below')
print('4: Less than 24 hours')

selection = 99
selection = input("Enter numeric value above: ")
selection = int(selection)

if selection > 4:
    while selection > 4:
        print('Wrong input')
        selection = input("Enter numeric value above: ")
        selection = int(selection)
    


urlWeUse = [''] * len(job_urls)
# Modify the URL to add the search time.    
if selection != 0:
    for i, link in enumerate(job_urls):
        temp = link.split('&remote')
        if selection == 1:
            temp = temp[0] + '&fromage=14&remote' + temp[1]
            urlWeUse[i] = temp
        if selection == 2:
            temp = temp[0] + '&fromage=7&remote' + temp[1]
            urlWeUse[i] = temp
        if selection == 3:
            temp = temp[0] + '&fromage=3&remote' + temp[1]
            urlWeUse[i] = temp
        if selection == 4:
            temp = temp[0] + '&fromage=1&remote' + temp[1]  
            urlWeUse[i] = temp
                
        


# Init and start the bot
bot = EasyApplyBot(args,  urlWeUse)
bot.startApp()


        
        
