from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

def extract_amazon_data_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # Let JS content load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    title = soup.find("span", id="productTitle")
    price = soup.find("span", class_="a-offscreen")
    rating = soup.find("span", class_="a-icon-alt")

    return {
        "title": title.get_text(strip=True) if title else "Not found",
        "price": price.get_text(strip=True) if price else "Not found",
        "rating": rating.get_text(strip=True) if rating else "Not found"
    }

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            result = extract_amazon_data_selenium(url)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5032)
