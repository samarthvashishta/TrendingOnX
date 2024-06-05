from flask import Flask, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import datetime
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://sam:sam2002@cluster0.jny4vs4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.trendingtopics
collection = db.trendingonX

# Credentials
username = 'samarthvashishta20@gmail.com'
password = 'password@123'
user = 'sampleuser_name'

# Selenium WebDriver setup
chrome_driver_path = r'C:\Users\Samarth\TrendingOnX\chromedriver.exe'

def scrape_trending_topics():
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    driver.get("https://x.com/i/flow/login")

    wait = WebDriverWait(driver, 10)

    # Enter username
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_field.send_keys(username)
    next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
    next_button.click()
    time.sleep(2)

    # Handle potential username or phone number prompt
    try:
        user_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        user_field.send_keys(user)
        next_button = driver.find_element(By.XPATH, "//span[text()='Next']")
        next_button.click()
    except Exception as e:
        print("User step skipped:", e)
    time.sleep(2)

    # Enter password
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_field.send_keys(password)
    login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")
    login_button.click()
    time.sleep(20)

    # Get page source and parse with BeautifulSoup
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    trending_section = driver.find_element(By.XPATH, '//h1[contains(text(), "Trending now")]/following-sibling::div')
    trending_items = trending_section.find_elements(By.XPATH, './/div[@aria-labelledby]')
    title = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/div/section')
    html_content = title.get_attribute("innerHTML")

    soup = BeautifulSoup(html_content, 'html.parser')
    elements_with_style = soup.find_all(style=lambda value: value and "color: rgb(231, 233, 234);" in value)
    texts_with_style = [element.get_text() for element in elements_with_style]
    points = [text for text in texts_with_style]

    # Store points in MongoDB
    doc = {"points": points[1:], "timestamp": datetime.datetime.utcnow()}
    collection.insert_one(doc)
    driver.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    scrape_trending_topics()
    return redirect(url_for('show_trending'))

@app.route('/trending')
def show_trending():
    trending_topics = collection.find().sort('timestamp', -1).limit(1)
    topics = trending_topics[0]['points'] if trending_topics else []
    timestamp = datetime.datetime.utcnow()
    return render_template('trending.html', topics=topics, timestamp = timestamp)

if __name__ == '__main__':
    app.run(debug=True)
