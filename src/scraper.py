import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
class MenuScraper:
    def __init__(self, url):
        self.url = url
        self.driver = None
        self.menu_data = []
        
    def setup_driver(self, headless=True):
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless=new') 
            
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-setuid-sandbox')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chrome_options.page_load_strategy = 'normal'  
        
        try:
            print("Menginstall/mengupdate Chrome driver...")
            service = Service(ChromeDriverManager().install())
            service.start_error_message = "Chrome driver gagal dijalankan"
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            self.driver.set_page_load_timeout(90)  
            self.driver.implicitly_wait(15)  
            
            print("Browser siap digunakan")
            
        except Exception as e:
            print(f"Error saat setup driver: {str(e)}")
            print("\nCoba solusi berikut:")
            print("1. Update Chrome browser ke versi terbaru")
            print("2. Restart terminal/command prompt")
            print("3. Hapus cache webdriver: %USERPROFILE%\\.wdm")
            raise
        
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
            time.sleep(5)
            
            print("Mencari dan mengklik semua tab kategori...")
            all_menu_data = []
            
            try:
                tabs = self.driver.find_elements(By.CSS_SELECTOR, "button[role='tab'], .mat-mdc-tab")
                print(f"Ditemukan {len(tabs)} tab kategori")
                
                for i, tab in enumerate(tabs):
                    try:
                        self.driver.execute_script("arguments[0].click();", tab)
                        tab_text = tab.text.strip()
                        print(f"\n  Tab {i+1}: {tab_text}")
                        time.sleep(3)  
                        
                        print(f"  Melakukan scroll di tab '{tab_text}'...")
                        last_height = self.driver.execute_script("return document.body.scrollHeight")
                        scroll_attempts = 0
                        
                        while scroll_attempts < 5:
                            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2)
                            new_height = self.driver.execute_script("return document.body.scrollHeight")
                            
                            if new_height == last_height:
                                break
                            last_height = new_height
                            scroll_attempts += 1
                        
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        time.sleep(1)
                        
                    except Exception as e:
                        print(f"  Error mengklik tab {i+1}: {str(e)}")
                        continue
                        
            except Exception as e:
                print(f"Tidak dapat menemukan tab, melanjutkan dengan single page: {str(e)}")
            
            print("\nMelakukan scroll final untuk load semua menu...")
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            
            for i in range(10):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                print(f"  Scroll #{i+1}, height: {new_height}")
                
                if new_height == last_height:
                    scroll_attempts += 1
                    if scroll_attempts >= 3:
                        break
                else:
                    scroll_attempts = 0
                last_height = new_height
            
            print("Selesai scroll, tunggu loading final...")
            time.sleep(3)
            
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
            time.sleep(1.5)  
            
            variants = self._parse_variants_from_modal()
            image_url = self._get_image_url_from_modal()
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
        """Extract image URL from modal and convert to thumbnail version"""
        try:
            modal_html = self.driver.page_source
            modal_soup = BeautifulSoup(modal_html, 'lxml')
            
            # Find the div with class 'menu-image-banner' that has style with background-image
            image_banner = modal_soup.find('div', class_='menu-image-banner')
            
            if image_banner and image_banner.get('style'):
                style = image_banner.get('style')
                # Extract URL from background-image: url("...")
                import re
                match = re.search(r'url\(["\']?([^"\')]+)["\']?\)', style)
                if match:
                    url = match.group(1)
                    # Convert _optim.webp to _thumb.webp
                    if '_optim.webp' in url:
                        url = url.replace('_optim.webp', '_thumb.webp')
                    elif '.webp' in url and '_thumb.webp' not in url:
                        # If it's a webp but not already optimized, try to add _thumb before .webp
                        url = url.replace('.webp', '_thumb.webp')
                    return url
        except Exception as e:
            print(f"  Error extracting image URL: {str(e)}")
        
        return None
    
    def _close_modal(self):
        try:
            close_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'close') or contains(@aria-label, 'close')]")
            close_button.click()
            time.sleep(0.5)
        except Exception:
            try:
                overlay = self.driver.find_element(By.CLASS_NAME, "cdk-overlay-backdrop")
                overlay.click()
                time.sleep(0.5)
            except Exception:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                time.sleep(0.5)
    
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
