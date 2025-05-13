import os
import time
import random
import urllib.parse
import requests
import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

# ---------- setting ----------

# keyword per field (field name: [keyword list])
fields_keywords = {
    "FOLDER TITLE 1": [
        "Marine ecosystem assessment",
        "Ocean biodiversity survey",
        "Coral reef monitoring",
        "Marine habitat mapping",
        "Coastal environmental impact assessment",
        "Fisheries resource assessment",
        "Marine biomass estimation",
        "Oceanographic data analysis",
        "Sustainable fisheries management",
        "Marine spatial planning",
        "Mariculture seed production",
        "Shellfish hatchery techniques",
        "Finfish breeding and larviculture",
        "Seaweed cultivation methods",
        "Offshore aquaculture systems",
        "Aquaculture broodstock management",
        "Marine fish larvae rearing",
        "Algal seed culture",
        "Bivalve spat collection",
        "Genetic improvement in aquaculture",
        "Recirculating aquaculture systems (RAS)",
        "Floating cage aquaculture",
        "Automated feeding systems",
        "Aquaculture water quality monitoring",
        "Sea cage design and engineering",
        "Restorative aquaculture practices",
        "Integrated multi-trophic aquaculture (IMTA)",
        "Eco-friendly mariculture",
        "Marine protected areas (MPAs)",
        "Blue carbon ecosystems",
    ],
    "FOLDER TITLE 2": [
        "Digital shoe prototyping",
        "Lean footwear manufacturing",
        "Injection-molded footwear",
        "3D knitting shoe technology",
        "Robotic shoe assembly",
        "Biofabricated leather alternatives",
        "Recycled PET shoe materials",
        "Self-healing shoe polymers",
        "Plant-based sneaker materials",
        "Aerogel cushioning for footwear",
        "Carbon-neutral shoe production",
        "Waterless dyeing processes",
        "Zero-waste footwear patterns",
        "Compostable shoe components",
        "Circular economy in shoemaking",
        "Italian luxury shoe craftsmanship",
        "Vietnamese athletic shoe exports",
        "German orthopedic footwear tech",
        "Brazilian sustainable sandals",
        "Indian hand-stitched footwear",
        "On-demand shoe manufacturing",
        "Blockchain in footwear supply chain",
        "Direct-to-consumer shoe brands",
        "Microfactory shoe production",
        "AI-driven inventory for footwear",
        "Volcanic ash-infused soles",
        "Space-grade footwear materials",
        "Antimicrobial hospital shoes",
        "Electric-heated winter boots",
        "Haptic feedback smart shoes",
    ],
}

# Max downloadable PDF count per keyword
MAX_PDF = 200

# main folder to save
SAVE_DIR = os.path.join(os.getcwd(), 'downloaded_pdfs')
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------

# User-Agent random generate
ua = UserAgent()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={ua.random}")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
# chrome_options.add_argument("--headless"

# execute browser
svc = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=svc, options=chrome_options)


# random waiting
def random_sleep(a=2, b=5):
    time.sleep(random.uniform(a, b))

# function to check if there is a robot detection
def is_robot_detected(driver):
    page_text = driver.page_source.lower()
    return ("unusual traffic" in page_text or
            "i'm not a robot" in page_text or
            "automated queries" in page_text)

# PDF save function
def save_pdf(url, save_path):
    try:
        response = requests.get(url, timeout=15, stream=True)
        if response.status_code == 200:
            # extract the original file name
            original_filename = url.split('/')[-1]
            original_filename = urllib.parse.unquote(original_filename)  # decoding
            final_path = os.path.join(save_path, original_filename)

            if not os.path.exists(final_path):  # prevent duplicate
                with open(final_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                print(f"✅ Save: {final_path}")
            else:
                print(f"⚠️ Already exist: {final_path}")
        else:
            print(f"⚠️ Download failed: {url}")
    except Exception as e:
        print(f"❗ Request failed: {url} - {e}")

# ▶ Work per keyword
for field, keywords in fields_keywords.items():
    print(f"\n📂 Start field work: {field}")

    # generate field directory
    field_folder = os.path.join(SAVE_DIR, field.replace(' ', '_'))
    os.makedirs(field_folder, exist_ok=True)

    for keyword in keywords:
        print(f"\n🔍 Start search: {keyword}")

        search_query = f"{keyword} filetype:pdf"
        base_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"

        pdf_urls = set()
        page_num = 0

        while len(pdf_urls) < MAX_PDF:
            target_url = base_url + f"&start={page_num * 10}"
            driver.get(target_url)

            # check if there is a robot detection
            if is_robot_detected(driver):
                print("🚨 Robot detected! please solve the problem manually.")
                
                # perform automatically after solving the problem manually
                input("continue performation automatically after solving the problem manually...")

                print("✅ restart after solving the problem manually!")

                # Setting to perform just after manual solution
                continue  # Restart (processing robot-detected page)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a")))

            except:
                print("❗ failed to load page")
                break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            random_sleep(2, 4)

            links = driver.find_elements(By.CSS_SELECTOR, "a")
            for link in links:
                href = link.get_attribute('href')
                if href and href.endswith('.pdf'):
                    pdf_urls.add(href)

            print(f"all found PDF link count: {len(pdf_urls)}")

            page_num += 1
            random_sleep(3, 6)

            if page_num > 2:
                print("❗ too many page search, stopped.")
                break

        print(f"totally {len(pdf_urls)} PDF links found. start download!")

        # generate folder per keyword
        keyword_folder = os.path.join(field_folder, keyword.replace(' ', '_'))
        os.makedirs(keyword_folder, exist_ok=True)

        for pdf_url in pdf_urls:
            save_pdf(pdf_url, keyword_folder)

        random_sleep(5, 10)

driver.quit()
print("\n🎉 all work finished!")
