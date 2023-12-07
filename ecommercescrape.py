import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Function to scrape product information
def scrape_product_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    product_info = []

    # Assuming product name, price, and link have specific CSS classes
    products = soup.find_all(class_='product')
    for product in products:
        name = product.find(class_='product-name').text
        price = product.find(class_='product-price').text
        link = product.find('a')['href']

        product_info.append({
            'name': name,
            'price': price,
            'link': link
        })

    return product_info

# Local API URL for products
url = 'http://localhost:5000/api/products'

# Scrape product information from the local API
product_info = scrape_product_info(url)

# Store scraped data in a DataFrame
if product_info:
    df = pd.DataFrame(product_info)  # Create a DataFrame from the product_info list

    # Data cleaning: Remove non-numeric characters from the price and convert to float
    df['price'] = df['price'].str.replace('₹', '').astype(float)

    # Visualization: Plotting product prices
    plt.bar(df['name'], df['price'])
    plt.xlabel('Product Name')
    plt.ylabel('Price (in ₹)')
    plt.title('Product Prices')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Display the plot
    plt.show()

    # Display the cleaned data
    print("Cleaned Data in DataFrame:\n", df)
