from flask import Flask, render_template, request, session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

def run_selenium(province, city, budget, budget2):
    driver = webdriver.Chrome()
    driver1 = webdriver.Chrome()
    
    try:
        wait = WebDriverWait(driver, 10)
        driver.get('https://chat18.aichatos.xyz/#/chat/1711713604024')
        driver1.get("https://file.digitaling.com/eImg/uimages/20150907/1441607668416465.gif")
        input_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'n-input__textarea-el')))
        input_box.send_keys(f"我想去{province}{city}旅游, 经费是{budget}元, 历时{budget2}天, 请为我每天建议旅游路线，著名景点和当地特色")
        input_box.send_keys(Keys.RETURN)
        time.sleep(30)
        html = driver.page_source
        return parse_html(html)
    finally:
        driver.quit()
        driver1.quit()

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text_contents = [element.get_text() for element in soup.find_all(['p', 'li'])]
    return text_contents

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/results", methods=['GET'])
def get_results():
    global province, city, budget, budget2
    province = request.args.get('province')
    city = request.args.get('city')
    budget = request.args.get('budget')
    budget2 = request.args.get('budget2') 
    
    text_contents = session.get('text_contents')
    if text_contents is None:
        text_contents = run_selenium(province, city, budget, budget2)
        session['text_contents'] = text_contents
        
    # Remove first three items    
    text_contents = text_contents[3:] if text_contents else []
    del text_contents[-1]
    return render_template("results.html", text_contents=text_contents)


if __name__ == '__main__':
    app.run(debug=True)