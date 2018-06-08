import os  
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
import time
import random
import datetime
import pytz
from dateutil.parser import parse

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=me")  
chromedriver = os.path.join(os.getcwd(), 'chromedriver.exe')
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)
driver.implicitly_wait(10)

driver.get('https://old.reddit.com/login')

username_field = input('enter your username: ')
password_field = input('enter your password: ')
try:
	driver.find_element_by_id('user_login').send_keys(username_field)
	driver.find_element_by_id('passwd_login').send_keys(password_field)
	driver.find_element_by_xpath("//button[text()='log in']").click()
except NoSuchElementException:
	driver.quit()
else:
	time.sleep(5)

file_name = input('type the name of the file where usernames are stored: ')
try:
	with open('downvote_targets.txt') as file:
		names = [line.rstrip('\n') for line in file]
except FileNotFoundError:
	print('there was a problem locating the file')
	driver.quit()

aware_time_now = pytz.utc.localize(datetime.datetime.now())

for name in names:
	driver.get('https://old.reddit.com/user/{}'.format(name))
	while True:
		print('downvoting {}...'.format(name))
		print('starting karma: {}'.format(driver.find_element_by_class_name('comment-karma').text))

		try:
			comments = driver.find_elements_by_class_name('thing')
			downvote_arrows = [comment.find_elements_by_class_name('arrow')[1] for comment in comments]
			timestamps = [comment.find_element_by_tag_name('time') for comment in comments]
		except NoSuchElementException:
			driver.quit()

		if not len(timestamps):
			break
		if (aware_time_now - parse(timestamps[0].get_attribute('datetime'))).days > 2:
			break
		for downvote_button, timestamp in zip(downvote_arrows, timestamps):
			if (aware_time_now - parse(timestamp.get_attribute('datetime'))).days < 2:
				if 'downmod' not in downvote_button.get_attribute('class'):
					downvote_button.click()
					pause_time = random.randint(90,120)
					print('downvoted at {}. pausing for {} seconds...'.format(datetime.datetime.now(), pause_time))
					time.sleep(pause_time)
				else:
					pass
			else:
				break

		if (aware_time_now - parse(timestamps[-1].get_attribute('datetime'))).days < 2:
			try:
				next_button = driver.find_element_by_partial_link_text('next')
			except:
				break
				driver.quit()
			else:
				driver.refresh()
				print('ending karma after series: {}'.format(driver.find_element_by_class_name('comment-karma')))
				next_button.click()
		else:
			break
			driver.quit()

driver.quit()