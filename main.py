from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import csv
import time

# Enter your chrome driver path here. Here is mine:
chrome_driver_path = "C:\Development\chromedriver.exe"


def write_data_to_csv(prices, prices_per, areas, links):
    with open("data.csv", mode="a", newline='') as file:
        writer = csv.writer(file)
        for row in zip(prices, prices_per, areas, links):
            writer.writerow(row)


class WebScraping(Service):

    def __init__(self, driver_path):
        super().__init__()
        self.service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=self.service)
        self.clear_prices = []
        self.clear_prices_per = []
        self.clear_descriptions = []
        self.clear_areas = []
        self.clear_links = []

        # Takes data from the website
    def get_housing_data(self):
        self.driver.get("https://m.xxxxxxx.lt/butai/vilniuje/")
        prices = self.driver.find_elements(by="class name", value="price-main")
        self.clear_prices = [int(price.text.replace("€", "").replace(" ", "")) for price in prices]
        prices_per = self.driver.find_elements(by="class name", value="price-per")
        self.clear_prices_per = [int(price_per.text.replace("€/m²", "").replace(" ", "")) for price_per in prices_per]
        descriptions = self.driver.find_elements(by="class name", value="item-description-v4")
        self.clear_descriptions = [description.text for description in descriptions]
        for description in self.clear_descriptions:
            try:
                self.clear_areas.append(float(description[9:15].replace(",", ".")))
            except ValueError:
                self.clear_areas.append(float(description[9:12].replace(",", ".")))
        links = self.driver.find_elements(by="class name", value="result-item-info-container-big_thumbs")
        self.clear_links = [link.get_attribute('href') for link in links]

        # Auto scrolls through pages to collect all the data
    def next_page(self):
        forward_button = self.driver.find_element(by="class name", value="icon-arrow-next-page")
        forward_button.click()
        time.sleep(3)

        # Does not close the browser after taking the data (optional)
    def dont_close_window(self):
        # Add the following line to wait for user input before closing the window
        input("Press any key to close the window...")

        # Close the window after user input
        self.driver.quit()

        # Auto clicks "accept cookies" button to be able to get to next page of the website
    def agree(self):
        try:
            agree_button = self.driver.find_element(by="id", value="onetrust-accept-btn-handler")
            agree_button.click()
            time.sleep(2)
        except:
            pass


bot = WebScraping(chrome_driver_path)

for _ in range(3):
    """Range takes an input of total number of pages to be scrolled through. 3 is just an example."""
    bot.get_housing_data()
    write_data_to_csv(
        prices=bot.clear_prices,
        prices_per=bot.clear_prices_per,
        areas=bot.clear_areas,
        links=bot.clear_links,
    )
    """prices = Real estate price in euros: integer
       pricer_per = Real estate price in euros per square meter: integer
       areas = area of the Real estate in square meters: integer
       links = website link of the of the Real estate"""
    bot.agree()
    # need to wait until an add closes
    time.sleep(8)
    bot.next_page()


bot.dont_close_window()
