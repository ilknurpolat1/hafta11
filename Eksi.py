from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import os
import re

class EksiSozluk:
    def __init__(self, url_listesi):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.url_listesi = url_listesi
        self.link_listesi = []
        self.baslik_isimleri = []


    def baslik_linklerini_topla(self, url):
        self.driver.get(url)
        self.driver.maximize_window()

        wait = WebDriverWait(self.driver, 60)
        container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".topic-list.partial")))

        time.sleep(5)
        li = container.find_elements(By.TAG_NAME, "li")
        for i in li:
            try:
                a = i.find_element(By.TAG_NAME, 'a')
                link = a.get_attribute('href')
                baslik = a.text.strip()
                self.link_listesi.append(link)
                self.baslik_isimleri.append(self.temizle(baslik))
            except:
                continue

        try:
            daha_fazla = self.driver.find_element(By.ID, "quick-index-continue-link")
            self.driver.execute_script("arguments[0].click();", daha_fazla)
            time.sleep(5)
            container1 = self.driver.find_element(By.CSS_SELECTOR, ".topic-list.partial")
            li1 = container1.find_elements(By.TAG_NAME, "li")
            for j in li1:
                try:
                    a1 = j.find_element(By.TAG_NAME, 'a')
                    link1 = a1.get_attribute('href')
                    baslik1 = a1.text.strip()
                    self.link_listesi.append(link1)
                    self.baslik_isimleri.append(self.temizle(baslik1))
                except:
                    continue
        except:
            pass

        try:
            son = self.driver.find_element(By.CLASS_NAME, "last")
            self.driver.execute_script("arguments[0].click();", son)
            time.sleep(5)
            container2 = self.driver.find_element(By.CSS_SELECTOR, ".topic-list.partial")
            li2 = container2.find_elements(By.TAG_NAME, "li")
            for k in li2:
                try:
                    a2 = k.find_element(By.TAG_NAME, 'a')
                    link2 = a2.get_attribute('href')
                    baslik2 = a2.text.strip()
                    self.link_listesi.append(link2)
                    self.baslik_isimleri.append(self.temizle(baslik2))
                except:
                    continue
        except:
            pass

    def sh_dosyalarini_olustur(self):
        if not os.path.exists("sh_dosyalar"):
            os.makedirs("sh_dosyalar")

        for baslik in self.baslik_isimleri:
            dosya_yolu = os.path.join("sh_dosyalar", f"{baslik}.sh")
            with open(dosya_yolu, "a", encoding="utf-8") as f:
               # f.write("#!/bin/bash\n")
                f.write(f"# Başlık: {baslik}\n")

    def yorumlari_cek_ve_yaz(self):
        for i in range(len(self.link_listesi)):
            self.driver.get(self.link_listesi[i])
            self.driver.maximize_window()

            wait = WebDriverWait(self.driver, 60)

            try:
                sayfa_sayisi = self.driver.find_element(By.CLASS_NAME, "pager")
                sayilar = sayfa_sayisi.find_elements(By.TAG_NAME, "a")

                for a in sayilar:
                    text = a.text.strip()
                    if text.isdigit():
                        sayi_int = int(text)
            except:
                sayi_int = 1

            for j in range(1, sayi_int + 1):
                if j != 1:
                    self.driver.get(self.link_listesi[i] + f"&p={j}")

                wait.until(EC.presence_of_element_located((By.ID, "entry-item-list")))
                container = self.driver.find_element(By.ID, "entry-item-list")
                li_elements = container.find_elements(By.TAG_NAME, "li")

                for li in li_elements:
                    try:
                        content = li.find_element(By.CLASS_NAME, "content")
                        with open(self.kayit_dosyasi, "a", encoding="utf-8") as f:
                            f.write(content.text + "\n" + "é")
                    except:
                        continue

    def kapat(self):
        self.driver.quit()

    def calistir(self):
        for url in self.url_listesi:
            self.baslik_linklerini_topla(url)
        self.sh_dosyalarini_olustur()
        self.yorumlari_cek_ve_yaz()
        self.kapat()

if __name__ == "__main__":
    url_listesi = [
        "https://eksisozluk.com/basliklar/gundem",
        "https://eksisozluk.com/basliklar/debe"
    ]
    ali = EksiSozluk(url_listesi)
    ali.calistir()
