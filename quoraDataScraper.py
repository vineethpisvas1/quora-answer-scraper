from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import  ActionChains
import time
timestr = time.strftime("%Y%m%d-%H%M%S")



profile_url = 'https://www.quora.com/bookmarked_answers'



driver = webdriver.Chrome(executable_path=r'path/to/web/driver/has/to/be/given/here')
driver.get(profile_url)

# Login Part for using it on Bookmarked answers page

loginInputFields = driver.find_elements_by_class_name('header_login_text_box')
for inputField in loginInputFields:
    if(inputField.get_attribute('name')=='email'):
        inputField.send_keys('Your email here!')
    elif(inputField.get_attribute('name')=='password'):
        inputField.send_keys('Your password here!')

submitFields = driver.find_elements_by_class_name('submit_button')

for submitField in submitFields:
    if(submitField.get_attribute('value')=='Login'):
        submitField.click()

bottom_of_the_page_xpath = '//div[@class="spinner_display_area hidden"]'   #determing the end part of the profile webpage

f = open('quora_answers_'+timestr+'.html','a')
questionHTML="""<p><b>Question:</b></p>"""
answerHTML="""<p><b>Answer:</b></p>"""
breakLineHTML = """<br>"""
endQuestionHTML = """<br>=========================================*#*#*#*===========================================<br>"""

# To reach the end of the page in order to load all the answers
while True:
    ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()   #triggering the arrow down key to move down in the page
    try:
        bottom_of_the_page = driver.find_element_by_xpath(bottom_of_the_page_xpath)
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        break
    except:
        continue


# Return to top of the page to avoid clicking on the Quora search bar
element = driver.find_element_by_xpath('//div[@class="header"]')
driver.execute_script("return arguments[0].scrollIntoView(true);", element)


more_links = driver.find_elements_by_xpath('//a[@class="ui_qtext_more_link"]')
for more_link in more_links:
    more_link.click()
    time.sleep(1)


# To reach the end of the page in order to load all the answers
driver.execute_script("return arguments[0].scrollIntoView(true);", bottom_of_the_page)
ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
time.sleep(1)
driver.execute_script("return arguments[0].scrollIntoView(true);", element)

more_links = driver.find_elements_by_xpath('//a[@class="ui_qtext_more_link"]')
for more_link in more_links:
    try:
        more_link.click()
        time.sleep(1)
    except:
        continue


driver.execute_script("return arguments[0].scrollIntoView(true);", bottom_of_the_page)
ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
time.sleep(1)
driver.execute_script("return arguments[0].scrollIntoView(true);", element)

answer_xpath = '//div[@class="inline_expand_item feed_item"]//div[@class="answer_body_preview"]//div[@class="ui_qtext_expanded"]/span[1]'
answers = driver.find_elements_by_xpath(answer_xpath)

question_xpath = '//span[@class="ui_content_title ui_content_title--default ui_content_title--medium"]/span[@class="ui_qtext_rendered_qtext"]'
questions = driver.find_elements_by_xpath(question_xpath)

for i in range(0, len(answers)):
    questionInnerHTML = questions[i].get_attribute('innerHTML')
    answerInnerHTML = answers[i].get_attribute('innerHTML')
    f.write(questionHTML)
    f.write(questionInnerHTML)
    f.write(breakLineHTML)
    f.write(answerHTML)
    f.write(answerInnerHTML)
    f.write(endQuestionHTML)