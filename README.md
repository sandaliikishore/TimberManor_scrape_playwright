
# TimberManor Product Scraper

## Overview
This project is a web scraper built with Python and Playwright to extract product details from the TimberManor website. It navigates through predefined category pages, scrapes product details, and saves the data to a CSV file.

## Features
- Scrapes product details including title, price, description, image URL, dimensions, and source URL.
- Supports multiple categories, automatically navigating through them.
- Saves the collected data into a structured CSV file for further use.

## Setup Instructions

### Prerequisites
Ensure you have the following installed on your system:
1. Python (>=3.7)
2. Playwright library
3. Pandas library

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/timbermanor-scraper.git
   cd timbermanor-scraper
   ```
2. Install the required Python libraries:
   ```bash
   pip install playwright pandas
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Usage

### Running the Scraper
1. Open the terminal and navigate to the project directory.
2. Run the scraper using the following command:
   ```bash
   python scraper.py
   ```
3. The script will scrape products from predefined categories and save the data to a CSV file named `timbermanor_products.csv` in the project directory.

### Output
The output CSV file contains the following columns:
- **Title**: Name of the product
- **Price**: Price of the product
- **Description**: Detailed description of the product
- **Image URL**: URL of the product image
- **Dimensions**: Dimensions of the product (if available)
- **Source URL**: URL of the product page

## Code Structure

### `scrape_product_details`
Scrapes details of a single product from its URL.
- **Inputs**: 
  - `page` (Playwright page instance) 
  - `product_url` (URL of the product)
- **Outputs**: A dictionary containing the product details.

### `scrape_category`
Scrapes all products in a given category.
- **Inputs**: 
  - `page` (Playwright page instance)
  - `category_url` (URL of the category page)
- **Outputs**: A list of dictionaries with product details.

### `scrape_all_categories`
The main function to scrape all predefined categories and save the results to a CSV file.
- **Outputs**: A CSV file containing all scraped product details.

## Configuration
The list of categories to scrape is predefined in the `scrape_all_categories` function. You can modify the `categories` list to add or remove category URLs as needed.

## Error Handling
- If dimensions or other product details are missing, the scraper assigns default values such as "No dimensions available".
- Logs errors encountered during scraping specific product details.

## Limitations
- The scraper assumes a specific HTML structure for the TimberManor website. Changes to the website layout may require updates to the XPath locators in the code.

## Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.
