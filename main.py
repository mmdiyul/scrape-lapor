from selenium import webdriver
import mysql.connector as mc
import time
import re


class Lapor:
    def __init__(self):
        self.email = 'YOUR_EMAIL'
        self.password = 'YOUR_PASSWORD'
        self.jumlah_data = 600000
        self.db = self.connect_database()
        self.cursor = self.db.cursor()
        self.driver = webdriver.Chrome('./chromedriver')
        self.driver.get('https://www.lapor.go.id')
        self.login()
        self.open_laporan_page()
        self.get_laporan_and_store()

    @staticmethod
    def connect_database():
        return mc.connect(
            host='localhost',
            user='root',
            password='asd',
            db='lapor'
        )

    def login(self):
        self.driver.find_element_by_css_selector('li.nav-login').click()
        # set email
        email = self.driver.find_element_by_css_selector("input[class*='form-control'][name='login']")
        time.sleep(0.1)
        email.send_keys(self.email)
        # set password
        password = self.driver.find_element_by_css_selector("input[class*='form-control'][name='password']")
        password.send_keys(self.password)
        password.submit()
        # sleep
        time.sleep(5)

    def open_laporan_page(self):
        self.driver.get('https://www.lapor.go.id/laporan')

    def get_laporan_and_store(self):
        for i in range(self.jumlah_data):
            count_infinite_item = len(self.driver.find_elements_by_css_selector('div.infinite-item'))
            judul = self.driver.find_elements_by_css_selector('div.complaint-title a')[i]
            link = judul.get_attribute('href')
            pelapor = self.driver.find_elements_by_css_selector('span.text-user')[i]
            platform = self.driver.find_elements_by_css_selector('span.text-channel')[i]
            tanggal = self.driver.find_elements_by_css_selector('div.user-information div')[i]
            laporan = self.driver.find_elements_by_css_selector('div.complaint-excerpt p.readmore')[i]
            instansi = self.driver.find_elements_by_css_selector('div.complaint-track-body p a')[i]
            print(i + 1, str(judul.text))
            print(str(link))
            print(str(pelapor.text))
            print(str(platform.text))
            print(str(instansi.text))
            print(self.cleanhtml(str(laporan.text)))
            print(str(tanggal.text))
            print('------------------------------------')
            self.cursor.execute("""INSERT INTO laporan(title, description, platform, waktu, username, link,
            institution) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')""" %
                                (self.cleanhtml(str(judul.text)),
                                 self.cleanhtml(str(laporan.text)),
                                 self.cleanhtml(str(platform.text)),
                                 self.cleanhtml(str(tanggal.text)),
                                 self.cleanhtml(str(pelapor.text)),
                                 self.cleanhtml(str(link)),
                                 self.cleanhtml(str(instansi.text))))
            self.db.commit()
            if i == count_infinite_item - 1 and i == self.jumlah_data - 1:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                return
            if i == count_infinite_item - 1:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                lanjut = self.driver.find_element_by_css_selector('div.ias-trigger')
                lanjut.click()
                time.sleep(30)

    @staticmethod
    def cleanhtml(text):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', text)
        cleanr = re.compile('\n')
        cleantext = re.sub(cleanr, ' ', cleantext)
        cleanr = re.compile('\r')
        cleantext = re.sub(cleanr, ' ', cleantext)
        cleanr = re.compile("'")
        cleantext = re.sub(cleanr, '', cleantext)
        cleanr = re.compile('&para;')
        cleantext = re.sub(cleanr, ' ', cleantext)
        return cleantext


if __name__ == '__main__':
    lapor = Lapor()
