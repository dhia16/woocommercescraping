import os
import tempfile
import csv
import requests
from flask import Flask, render_template, request, send_file
from io import StringIO
from bs4 import BeautifulSoup

app = Flask(__name__)

# Function to fetch and parse the HTML content of a product page
def get_product_details(url):
    product_details = {}

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', class_='product_title')
    product_details['title'] = title.get_text(strip=True) if title else 'Unknown Product'

    description = soup.find('div', class_='woocommerce-product-details__short-description')
    product_details['description'] = description.get_text(strip=True) if description else ''

    price = soup.find('span', class_='price')
    product_details['price'] = price.get_text(strip=True) if price else '0'

    categories = soup.find('span', class_='posted_in')
    product_details['categories'] = categories.get_text(strip=True) if categories else ''

    feature_image = soup.find('img', class_='wp-post-image')
    product_details['feature_image'] = feature_image['src'] if feature_image else ''

    gallery_images = []
    gallery = soup.find('div', class_='woocommerce-product-gallery')
    if gallery:
        gallery_images = [img['src'] for img in gallery.find_all('img') if img.get('src')]
    product_details['gallery_images'] = ', '.join(gallery_images)

    return product_details

# Function to generate WooCommerce CSV
def generate_csv(product_urls):
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', newline='', encoding='utf-8')
    csv_writer = csv.writer(temp_file)

    # WooCommerce CSV Header
    csv_writer.writerow([
        'ID', 'Type', 'SKU', 'Name', 'Published', 'Is Featured?', 'Visibility in catalog',
        'Short description', 'Description', 'Date on sale from', 'Date on sale to', 
        'Tax status', 'Tax class', 'In stock?', 'Stock quantity', 'Backorders allowed?', 
        'Sold individually?', 'Weight (kg)', 'Length (cm)', 'Width (cm)', 'Height (cm)', 
        'Allow customer reviews?', 'Purchase note', 'Sale price', 'Regular price', 'Categories',
        'Tags', 'Shipping class', 'Images', 'Download limit', 'Download expiry days'
    ])

    # Writing product data to CSV
    for url in product_urls:
        product = get_product_details(url)
        if product:
            csv_writer.writerow([
                '', 'simple', '', product['title'], '1', '0', 'visible', '', 
                product['description'], '', '', 'taxable', '', '1', '100', 'no', '0', 
                '', '', '', '', '1', '', product['price'], product['price'], 
                product['categories'], '', '', product['feature_image'] + ',' + product['gallery_images'], '', ''
            ])
    
    # Close the temp file
    temp_file.close()
    return temp_file.name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_csv', methods=['POST'])
def generate_csv_route():
    urls = request.form.get('urls').splitlines()  # Get URLs from the textarea
    file_path = generate_csv(urls)

    # Send the CSV file
    return send_file(
        file_path,
        as_attachment=True,
        download_name='woocommerce_products.csv',
        mimetype='text/csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
