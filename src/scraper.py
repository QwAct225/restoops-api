import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
class MenuScraper:
    def __init__(self, url, browser='auto'):
        self.url = url
        self.driver = None
        self.menu_data = []
        self.browser = browser.lower()
        
    def detect_browser(self):
        browsers = {
            'brave': [
                '/usr/bin/brave-browser',
                '/usr/bin/brave',
                '/snap/bin/brave',
                os.path.expanduser('~/.local/bin/brave'),
            ],
            'chrome': [
                '/usr/bin/google-chrome',
                '/usr/bin/google-chrome-stable',
                '/usr/bin/chromium-browser',
                '/usr/bin/chromium',
                '/snap/bin/chromium',
            ],
            'firefox': [
                '/usr/bin/firefox',
                '/snap/bin/firefox',
            ]
        }
        
        for browser_name, paths in browsers.items():
            for path in paths:
                if os.path.exists(path):
                    print(f"✓ Ditemukan {browser_name.capitalize()}: {path}")
                    return browser_name, path
        
        return None, None
        
    def setup_driver(self, headless=True):
        try:
            browser_to_use = self.browser
            browser_path = None
            
            if self.browser == 'auto':
                print("Mendeteksi browser yang tersedia...")
                detected_browser, detected_path = self.detect_browser()
                if detected_browser:
                    browser_to_use = detected_browser
                    browser_path = detected_path
                    print(f"Menggunakan {detected_browser.capitalize()}\n")
                else:
                    raise Exception("Tidak ada browser yang terdeteksi (Chrome, Brave, atau Firefox)")
            
            if browser_to_use in ['chrome', 'brave']:
                self._setup_chromium_driver(headless, browser_to_use, browser_path)
            elif browser_to_use == 'firefox':
                self._setup_firefox_driver(headless, browser_path)
            else:
                raise ValueError(f"Browser '{self.browser}' tidak didukung. Pilih: chrome, brave, firefox, atau auto")
                
        except Exception as e:
            print(f"Error saat setup driver: {str(e)}")
            print("\nCoba solusi berikut:")
            print("1. Install salah satu browser: Brave, Chrome, atau Firefox")
            print("2. Pastikan browser terinstall di lokasi standar")
            print("3. Atau spesifikasikan browser: MenuScraper(url, browser='brave')")
            raise
    
    def _setup_chromium_driver(self, headless=True, browser_name='chrome', browser_path=None):
        chrome_options = ChromeOptions()
        
        if browser_name == 'brave' and browser_path:
            chrome_options.binary_location = browser_path
        elif browser_name == 'brave' and not browser_path:
            _, detected_path = self.detect_browser()
            if detected_path:
                chrome_options.binary_location = detected_path
        
        if headless:
            chrome_options.add_argument('--headless=new')
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-popup-blocking')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--metrics-recording-only')
        chrome_options.add_argument('--mute-audio')
        
        chrome_options.page_load_strategy = 'normal'
        
        print(f"Menyiapkan ChromeDriver untuk {browser_name.capitalize()}...")
        self.driver = webdriver.Chrome(options=chrome_options)
        
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        self.driver.set_page_load_timeout(90)
        self.driver.implicitly_wait(15)
        print(f"{browser_name.capitalize()} browser siap digunakan")
    
    def _setup_firefox_driver(self, headless=True, browser_path=None):
        firefox_options = FirefoxOptions()
        
        if browser_path:
            firefox_options.binary_location = browser_path
        
        if headless:
            firefox_options.add_argument('--headless')
        
        firefox_options.add_argument('--width=1920')
        firefox_options.add_argument('--height=1080')
        firefox_options.set_preference('dom.webdriver.enabled', False)
        firefox_options.set_preference('useAutomationExtension', False)
        firefox_options.set_preference('general.useragent.override', 
                                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0')
        
        print("Menyiapkan GeckoDriver untuk Firefox...")
        self.driver = webdriver.Firefox(options=firefox_options)
        
        self.driver.set_page_load_timeout(90)
        self.driver.implicitly_wait(15)
        print("Firefox browser siap digunakan")
        
    def scrape_menu(self, headless=False):
        try:
            print("Menyiapkan browser...")
            if not headless:
                print("⚠️  Browser akan terbuka (non-headless mode)")
            self.setup_driver(headless=headless)
            
            print(f"Mengakses URL: {self.url}")
            self.driver.get(self.url)
            
            print("Menunggu halaman loading...")
            wait = WebDriverWait(self.driver, 30)  
            
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu-grid-item-content")))
            except:
                print("Mencoba menunggu element alternatif...")
                try:
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "menu-name")))
                except:
                    print("Timeout menunggu element menu, melanjutkan parsing...")
            
            print("Menunggu JavaScript loading...")
            time.sleep(4)
            
            print("\nMelakukan scroll untuk load semua menu...")
            
            for scroll_round in range(2):
                print(f"  Round {scroll_round + 1}: Scroll dari atas ke bawah...")
                
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(0.8)
                
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                scroll_position = 0
                scroll_step = 250 
                
                while scroll_position < last_height:
                    scroll_position += scroll_step
                    self.driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                    time.sleep(0.4) 
                
                for _ in range(3):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(0.8)
                
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                print(f"    Height: {new_height}")
            
            print("  Scroll final...")
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            page_source = self.driver.page_source
            print("\nParsing HTML...")
            soup = BeautifulSoup(page_source, 'lxml')
            
            menu_items = soup.find_all('div', class_='menu-grid-item-content')
            print(f"Ditemukan {len(menu_items)} menu items")
            
            print("\nMengambil detail menu dan variants...")
            for idx, item in enumerate(menu_items, start=1):
                try:
                    menu_name_element = item.find('div', class_='menu-name')
                    menu_name = menu_name_element.get_text(strip=True) if menu_name_element else "N/A"
                    menu_data_id = menu_name_element.get('data-id') if menu_name_element else None
                    menu_price_element = item.find('div', class_='menu-price')
                    if menu_price_element:
                        price_span = menu_price_element.find('span')
                        menu_price = price_span.get_text(strip=True) if price_span else "N/A"
                        menu_price_clean = menu_price.replace('Rp', '').replace('.', '').strip()
                    else:
                        menu_price = "N/A"
                        menu_price_clean = "0"
                    
                    sold_out_element = item.find('div', class_='sold-out-badge')
                    is_sold_out = sold_out_element is not None
                    variants, image_url = self._get_menu_variants_by_index(idx - 1, menu_name)
                    variants_str = str(variants) if variants else "[]"
                    
                    menu_dict = {
                        'id': idx,
                        'nama_menu': menu_name,
                        'harga': menu_price_clean,
                        'variants': variants_str,
                        'sold_out': 'Yes' if is_sold_out else 'No',
                        'image_url': image_url if image_url else 'N/A'
                    }
                    
                    self.menu_data.append(menu_dict)
                    
                    status = " (SOLD OUT)" if is_sold_out else ""
                    variants_info = f" | Variants: {variants}" if variants else ""
                    print(f"  {idx}. {menu_name} - Rp{menu_price_clean}{status}{variants_info}")
                    
                except Exception as e:
                    print(f"Error parsing menu item {idx}: {str(e)}")
                    continue
            
            return self.menu_data
            
        except Exception as e:
            print(f"Error saat scraping: {str(e)}")
            raise
            
        finally:
            if self.driver:
                self.driver.quit()
                print("Browser ditutup")
    
    def _get_menu_variants_by_index(self, menu_index, menu_name):
        variants = []
        image_url = None
        
        try:
            menu_elements = self.driver.find_elements(By.CLASS_NAME, "menu-grid-item-content")
            
            if menu_index >= len(menu_elements):
                return variants, image_url
            
            menu_element = menu_elements[menu_index]
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_element)
            time.sleep(0.3)
            
            menu_element.click()
            time.sleep(0.5)
            
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "menu-image-banner"))
                )
            except:
                pass
            
            time.sleep(0.8)
            
            image_url = self._get_image_url_from_modal()
            variants = self._parse_variants_from_modal()
            self._close_modal()
            
        except Exception:
            pass
        
        return variants, image_url
    
    def _get_menu_variants(self, menu_data_id, menu_name):
        variants = []
        
        try:
            menu_element = self.driver.find_element(
                By.XPATH, 
                f"//div[@class='menu-name' and @data-id='{menu_data_id}']"
            )
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", menu_element)
            time.sleep(0.5)
            
            menu_element.click()
            time.sleep(2)  
            
            variants = self._parse_variants_from_modal()
            self._close_modal()
            
        except Exception:
            pass
        
        return variants
    
    def _parse_variants_from_modal(self):
        variants = []
        modal_html = self.driver.page_source
        modal_soup = BeautifulSoup(modal_html, 'lxml')
        
        menu_containers = modal_soup.find_all('div', class_='menu-container')
        
        for container in menu_containers:
            variant_divs = container.find_all('div', class_='word-break')
            for div in variant_divs:
                inner_div = div.find('div')
                if inner_div:
                    text = inner_div.get_text(strip=True)
                    text = text.replace('(+', ' (+')
                    while '  ' in text:
                        text = text.replace('  ', ' ')
                    text = text.strip()
                    
                    skip_words = ['VARIANT', 'MUST', 'SELECTED', 'MAX', 'MIN', 'OPTIONAL', 'REQUIRED']
                    if text and not any(word in text.upper() for word in skip_words):
                        if text.isupper() or '(+' in text or 'LEVEL' in text.upper():
                            if text not in variants:
                                variants.append(text)
        
        if not variants:
            checkboxes = modal_soup.find_all('mat-checkbox')
            for checkbox in checkboxes:
                parent = checkbox.find_parent('div', class_='align-items-center')
                if parent:
                    text_container = parent.find('div', class_='word-break')
                    if text_container:
                        inner_div = text_container.find('div')
                        if inner_div:
                            text = inner_div.get_text(strip=True)
                            if text and text not in variants:
                                variants.append(text)
        
        if not variants:
            radio_buttons = modal_soup.find_all('mat-radio-button')
            for radio in radio_buttons:
                parent = radio.find_parent('div', class_='align-items-center')
                if parent:
                    text_container = parent.find('div', class_='word-break')
                    if text_container:
                        inner_div = text_container.find('div')
                        if inner_div:
                            text = inner_div.get_text(strip=True)
                            if text and text not in variants:
                                variants.append(text)
        
        return variants
    
    def _get_image_url_from_modal(self):
        import re
        
        try:
            banner_elements = self.driver.find_elements(By.CLASS_NAME, "menu-image-banner")
            for element in banner_elements:
                if element.is_displayed():
                    style = element.get_attribute('style')
                    if style and 'background-image' in style:
                        match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', style)
                        if match:
                            url = match.group(1)
                            # Convert to thumbnail version
                            if '_optim.webp' in url:
                                return url.replace('_optim.webp', '_thumb.webp')
                            elif '.webp' in url and '_thumb.webp' not in url:
                                return url.replace('.webp', '_thumb.webp')
                            return url
            
            all_with_bg = self.driver.find_elements(By.XPATH, "//*[contains(@style, 'background-image')]")
            for element in all_with_bg:
                if element.is_displayed():
                    style = element.get_attribute('style')
                    if style and ('menu' in style.lower() or 'mnu' in style.lower()):
                        match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', style)
                        if match:
                            url = match.group(1)
                            if '_optim.webp' in url:
                                return url.replace('_optim.webp', '_thumb.webp')
                            elif '.webp' in url and '_thumb.webp' not in url:
                                return url.replace('.webp', '_thumb.webp')
                            return url
            
            img_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='menu'], img[src*='MNU'], img[src*='aliyuncs']")
            for img in img_elements:
                if img.is_displayed():
                    src = img.get_attribute('src')
                    if src and ('menu' in src.lower() or 'mnu' in src.upper()):
                        if '_optim.webp' in src:
                            return src.replace('_optim.webp', '_thumb.webp')
                        elif '.webp' in src and '_thumb.webp' not in src:
                            return src.replace('.webp', '_thumb.webp')
                        return src
                    
        except Exception:
            pass
        
        return None
    
    def _close_modal(self):
        try:
            close_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'Close') or contains(@aria-label, 'close')]")
            for btn in close_buttons:
                try:
                    if btn.is_displayed() and btn.is_enabled():
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(0.3)
                        return
                except:
                    continue
        except:
            pass
        
        try:
            overlays = self.driver.find_elements(By.CLASS_NAME, "cdk-overlay-backdrop")
            for overlay in overlays:
                try:
                    if overlay.is_displayed():
                        self.driver.execute_script("arguments[0].click();", overlay)
                        time.sleep(0.3)
                        return
                except:
                    continue
        except:
            pass
        
        try:
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.3)
        except:
            pass
    
    def save_to_csv(self, output_path):
        if not self.menu_data:
            print("Tidak ada data untuk disimpan")
            return
        
        df = pd.DataFrame(self.menu_data)
        df.to_csv(output_path, index=False, encoding='utf-8-sig', quoting=1)  
        print(f"\nData berhasil disimpan ke: {output_path}")
        print(f"Total menu: {len(self.menu_data)}")
    
    def save_to_json(self, output_path):
        if not self.menu_data:
            print("Tidak ada data untuk disimpan")
            return
        
        import json
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.menu_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nData berhasil disimpan ke: {output_path}")
        print(f"Total menu: {len(self.menu_data)}")
        
        
    def get_dataframe(self):
        return pd.DataFrame(self.menu_data)
