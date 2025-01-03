# WooCommerce Product Scraper

## Description

The WooCommerce Product Scraper is a Python application that scrapes product data from a WooCommerce store built with the **Woodmart theme**. The script collects essential information such as product details, prices, images, and more. The data is then saved in a CSV format for easy use.

## Features

- Scrapes product data such as:
  - ID
  - Type
  - SKU
  - Name
  - Price
  - Description
  - Stock information
  - Images
  - And more...
  
- Automatically detects and scrapes products from the given WooCommerce store.
- Saves the data in a CSV file for further processing or analysis.
- Written in Python with Flask to make it easy to integrate with web services.

## Requirements

- Python 3.x
- Flask
- BeautifulSoup4
- Requests
- pandas

## Installation

1. Clone this repository:
    ```bash
    [git clone https://github.com/dhia16/woocommercescraping ]
    ```

2. Navigate to the project directory:
    ```bash
    cd woocommerce-product-scraper
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    ```bash
    # On Windows
    venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

5. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Flask application and trigger the scraping process:

```bash
python app.py
