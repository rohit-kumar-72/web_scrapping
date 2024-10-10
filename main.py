from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from selenium.webdriver.common.proxy import Proxy, ProxyType
 
# Dictionary to hold the data
d = {
    'Date&Time': [],
    'Name': [],
    'Brand': [],
    'Avg. Rating': [],
    'Rating Count': [],
    'Sponsered': [],
    'Price': [],
    'Sale Price': [],
    'Express': [],
    'Links': [],
}


try:
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = '187.94.100.254:8080'  
    proxy.ssl_proxy = '187.94.100.254:8080'  
except Exception as e:
    print("error with the proxy!!!\n\n")

print("\n\n\n++++++++++++++++++++++  PLEASE WAIT WE ARE FETCHING DATA  ++++++++++++++++++++++++\n\n\n")



driver = webdriver.Firefox()
driver.minimize_window()



def fetch_data(driver):
    for page in range(1, 5):

        url = f"https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?limit=50&page={page}&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc"
        
        # getting each page data 
        driver.get(url)

        try:
            cards = driver.find_elements(By.CLASS_NAME, "productContainer")
        
            # processing on each card 
            for card in cards:
                try:
                    # Get product ID and link
                    a_element = card.find_element(By.CSS_SELECTOR, "div a")
                    id = a_element.get_attribute("id")
                    link =a_element.get_attribute("href")
                    
                    # Get date & time (if available)
                    try:
                        date_time = card.find_element(By.CSS_SELECTOR, f"#{id} b").text
                    except:
                        pass
                    
                    # Get product name and brand
                    name = card.find_element(By.CSS_SELECTOR, f"#{id} .fPskJH").get_attribute("title")
                    brand_name = name.split(' ')[0]
                    
                    # Get rating and rating count (if available)
                    try:
                        rating = card.find_element(By.CSS_SELECTOR, f"#{id} .hUinXQ").text
                        rating_count = card.find_element(By.CSS_SELECTOR, f"#{id} .kwLXrK").text
                    except Exception:
                        rating = '-'
                        rating_count = '-'
                    
                    # Check if the product is sponsored
                    try:
                        sponsered_div = card.find_element(By.CSS_SELECTOR, f"#{id} .AkmCS").text
                        is_sponsered = 'Y' if len(sponsered_div) > 0 else 'N'
                    except Exception:
                        is_sponsered = 'N'
                    
                    # Get prices
                    amount = card.find_element(By.CSS_SELECTOR, ".amount").text
                    try:
                        old_price = card.find_element(By.CSS_SELECTOR, ".oldPrice").text
                    except Exception as e:
                        old_price=amount
                    
                    # Check if express shipping is available
                    try:
                        card.find_element(By.CSS_SELECTOR, ".eVCkvW")  # Checking if this class exists
                        express = 'Y'
                    except Exception:
                        express = 'N'
                        
                    
                    # Append data to the dictionary
                    d['Date&Time'].append(date_time)
                    d['Name'].append(name)
                    d['Brand'].append(brand_name)
                    d['Avg. Rating'].append(rating)
                    d['Rating Count'].append(rating_count)
                    d['Sponsered'].append(is_sponsered)
                    d['Price'].append(old_price)
                    d['Sale Price'].append(amount)
                    d['Express'].append(express)
                    d['Links'].append(link)

                except Exception as e:
                    print(f"Error processing card: {e}")
                    continue  # Skip this card and move to the next one
        
        except Exception as e:
            print(f"Error occurred while scraping: {e}")
            break    

    driver.close()
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(data=d)
    df.to_csv("data.csv", index=False)
    return df

def clean_data(data):
    # Remove commas and convert to float
    data['Price'] = data['Price'].astype(str).str.replace(',', '').astype(float)
    data['Sale Price'] = data['Sale Price'].astype(str).str.replace(',', '').astype(float)

data=fetch_data(driver)
# data=pd.read_csv("data.csv")
clean_data(data)
    
def group_using_brand(data):
    print()
    print("\n\n\n++++++++++++++++++++++  Number of Products from Each brand  ++++++++++++++++++++++++\n\n\n")

    # Number of Products from Each brand
    brand_product_details = data['Brand'].value_counts()
    pd.set_option('display.max_rows', None)
    print("Number of Products from Each Brand:\n")
    print(brand_product_details)
    print("----------------------------------------------------------------")
    print()
    
    # Generate a list of colors from a colormap
    plt.figure(figsize=(12, 6))
    cmap = plt.colormaps['Paired']  # You can choose any colormap name you prefer
    colors = cmap(np.linspace(0, 1, len(brand_product_details)))

    # Create the bar plot with different colors
    bars = plt.bar(brand_product_details.index, brand_product_details.values, color=colors, width=0.5)

    plt.title('Number of Products from Each Brand')
    plt.xlabel('Brand')
    plt.ylabel('Number of Products')
    plt.xticks(rotation=90, ha='center',fontsize=8)
    plt.tight_layout()

    # Show the plot
    plt.show()

def expensive_product(data):
    price_sorted_data=data.sort_values("Price",ascending=False)
    
    # Most expensive products
    print("\n\n\n++++++++++++++++++++++ Most expensive products  ++++++++++++++++++++++++\n\n\n")
    expensive_price=price_sorted_data.iloc[0]['Price']
    for index, row in price_sorted_data.iterrows():
        
        if row['Price'] != expensive_price:
            break
        
        print(row[['Brand', 'Price', 'Avg. Rating', 'Sale Price']])
        print()
        
    print()
    print("----------------------------------------------------------------")

def cheapest_product(data):
    price_sorted_data=data.sort_values("Price",ascending=False)
    
    # Most cheapest Product
    print("\n\n\n++++++++++++++++++++++  Most cheapest Product  ++++++++++++++++++++++++\n\n\n")
    cheapest_price = price_sorted_data.iloc[-1]['Price']
    for index, row in price_sorted_data[::-1].iterrows():
        
        if row['Price'] != cheapest_price:
            break
        
        print("cheapest Products:\n\n",row[['Brand', 'Price', 'Avg. Rating', 'Sale Price']],sep='')
        print("----------------------------------------------------------------")
        print()


print("1. GET MOST EXPENSIVE PRODUCT.","2. GET CHEAPEST PRODUCT.","3. NUMBER OF PRODUCT FROM EACH BRAND.","4. EXIT.",sep='\n')

key=int(input('\n Enter key 1 | 2 | 3 | 4 : '))

while(key==1 or key==2 or key==3):
    if key==1:
        expensive_product(data)
    elif key==2:
        cheapest_product(data)
    elif key==3:
        group_using_brand(data)
        
    print("\n\n\n")
        
    print("1. GET MOST EXPENSIVE PRODUCT.","2. GET CHEAPEST PRODUCT.","3. NUMBER OF PRODUCT FROM EACH BRAND.","4. EXIT.",sep='\n')
    key=int(input('\n Enter key 1 | 2 | 3 | 4 : '))