import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import pywhatkit as kit

# Initialize Edge WebDriver
driver = webdriver.Edge()

driver.maximize_window()

try:
    # Internshala automation
    website = 'https://internshala.com/'
    driver.get(website)

    # Logging into the website
    driver.find_element(By.XPATH, '/html/body/div[1]/div[19]/div/nav/div[3]/button[2]').click()
    username = ""#add username
    user = driver.find_element(By.XPATH, '/html/body/div[1]/div[17]/div/div/div[2]/form/div[1]/input')
    user.send_keys(username)
    password = ''#add password
    pas_path = driver.find_element(By.XPATH, '/html/body/div[1]/div[17]/div/div/div[2]/form/div[2]/input')
    pas_path.send_keys(password)
    time.sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[17]/div/div/div[2]/form/div[4]/button').click()
    time.sleep(5)

    # Hover over internships
    actChain = ActionChains(driver)
    intern = driver.find_element(By.XPATH, "//a[@id='internships_new_superscript']")
    actChain.move_to_element(intern).perform()
    time.sleep(2)

    # Selecting location 
    driver.find_element(By.XPATH, "(//span[contains(text(),'Location')])[1]").click()
    driver.find_element(By.XPATH, "//a[normalize-space()='Work from Home']").click()
    time.sleep(2)

    # Selecting preferences
    category = driver.find_element(By.XPATH, "/html/body/div[1]/div[20]/div[3]/div/div[4]/div[1]/div/div/div[1]/form/div[2]/label")
    category.click()
    time.sleep(2)
    profile = driver.find_element(By.XPATH, '/html/body/div[1]/div[20]/div[3]/div/div[4]/div[1]/div/div/div[1]/form/div[2]/div/div[1]/ul/li/input')
    profile.click()
    profile.send_keys("Computer Science")
    time.sleep(2)
    profile.send_keys(Keys.ENTER)
    time.sleep(3)

    # Selecting the stipend range as per choice
    try:
        slider = driver.find_element(By.ID, "stipend_filter")
        actChain.click_and_hold(slider).move_by_offset(60, 0).release().perform()
        time.sleep(3)
    except Exception as e:
        print('Not able to find element', e)
    time.sleep(10)

    # Extracting data (internship) based upon keywords
    internshiplist = []
    keywords = ['AI Developer', 'Python Web Scraping', 'Backend Development', 'Full Stack Development', 'Android App Development', 'Web Development', 'Mobile App Development', 'Machine Learning', 'Blockchain Development', 'Node.js Development', 'Software Development', 'iOS App Development', 'WordPress Development', 'Front End Development', 'Python Full Stack Development', 'AWS DevOps Engineer', 'Product Management']

    while True:
        data = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'container-fluid individual_internship')]")))

        for item in data:
            try:
                jobRole = item.find_element(By.XPATH, ".//div[1]/div[1]/h3").text
                joblink = item.get_attribute('data-href')
                url= 'https://internshala.com'+joblink
                companyName = item.find_element(By.XPATH, ".//div[1]/div[1]/div/div/p").text
                stipend = item.find_element(By.XPATH, ".//div[2]/div[1]/div[3]/span").text
                duration = item.find_element(By.XPATH, ".//div[2]/div[1]/div[2]/span").text

                if any(keyword in jobRole for keyword in keywords):
                    internship = {
                        "role": jobRole,
                        "link": url,
                        "company": companyName,
                        "stipend": stipend,
                        "duration": duration
                    }
                    internshiplist.append(internship)

            except Exception as e:
                print("Exception occurred", e)
            time.sleep(1)  # Reduce sleep time to avoid long waits
        
        break

    # Save to CSV
    df = pd.DataFrame(internshiplist)
    df.to_csv('internship.csv', index=False)
    print("Internship data saved to internship.csv")

    # WhatsApp Web automation
    whatsapp_web_url = 'https://web.whatsapp.com/'
    driver.get(whatsapp_web_url)
    print("Please scan the QR code to log in to WhatsApp Web.")
    time.sleep(20)  # Wait for manual login

    myPhoneNumber = '+918826336052'
    for index, internshipRow in df.head(5).iterrows():  # Only process the first five rows
        try:
            # Print the URL before navigating to it
            print(f"Navigating to URL: {internshipRow['link']}")

            # Validate and clean the URL
            url = internshipRow['link']
            if not url.startswith('http'):
                url = 'https://internshala.com' + url

            driver.get(url)
            time.sleep(5)  # Wait for the page to load

            # Take a screenshot
            screenshotFilepath = "C:\\Users\\Dell\\Internshala Automation\\screenshot"+ str(index) + ".png"
            driver.save_screenshot(screenshotFilepath)
            print(f"Screenshot saved: {screenshotFilepath}")

            # Send the screenshot via WhatsApp
            kit.sendwhats_image(myPhoneNumber, screenshotFilepath, url)
            print(f"Sent {screenshotFilepath} and link to {myPhoneNumber}")
            time.sleep(10)
            
        except Exception as e:
            print(f"An error occurred while sending message for internship {index}: {e}")

finally:
    driver.quit()
