import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_product_details(page, product_url):
    """
    Scrapes product details from a given product URL.

    Args:
        page: The Playwright page instance.
        product_url: The URL of the product to scrape.

    Returns:
        A dictionary containing product details: Title, Price, Description, Image URL, Dimensions, and Source URL.
    """
    page.goto(product_url)
    page.set_default_timeout(60000)

    # Scraping product details
    product_name = page.locator("//div[@class='product__title']//h1").text_content().strip()
    price = page.locator("//span[@class='price-item price-item--regular'").text_content().strip()

    # Handle multiple paragraphs for description
    description_elements = page.locator("//div[@class='product__description rte quick-add-hidden']//p")
    descriptions = [desc.text_content().strip() for desc in description_elements.all() if desc.text_content().strip()]
    description = " ".join(descriptions) if descriptions else "No description available"

    # Scraping image URL
    img_tag = page.locator("//div[@class='product__media media media--transparent']//img").first
    img_url = img_tag.get_attribute("src") if img_tag else "No image available"

    # Scraping dimensions if available
    try:
        if page.locator('//div[@class="accordion__content rte"]//p/span'):
            dimension_element = page.locator('//div[@class="accordion__content rte"]//p/span').text_content()
        else:
            dimension_element = "No dimensions available"
    except Exception as e:
        print(f"Error scraping dimensions for {product_url}: {e}")
        dimension_element = "No dimensions available"

    return {
        "Title": product_name,
        "Price": price,
        "Description": description,
        "Image URL": img_url,
        "Dimensions": dimension_element,
        "Source URL": product_url
    }

def scrape_category(page, category_url):
    """
    Scrapes all product details from a given category URL.

    Args:
        page: The Playwright page instance.
        category_url: The URL of the category to scrape.

    Returns:
        A list of dictionaries, each containing details of a product.
    """
    # Open the category page
    page.goto(category_url)

    # Get the base URL
    base_url = category_url.split("/collections")[0]  # Extract base URL from the category URL

    # Find all product URLs in the category
    product_links = page.locator("//h3[@class='card__heading h5']//a")
    product_urls = [link.get_attribute('href') for link in product_links.all()]

    # Ensure product URLs are absolute
    product_urls = [url if url.startswith("http") else base_url + url for url in product_urls]

    # Scrape details for each product
    products = []
    for product_url in product_urls:
        product_details = scrape_product_details(page, product_url)
        products.append(product_details)

    return products

def scrape_all_categories():
    """
    Scrapes products from all predefined categories and saves them to a CSV file.

    The scraper uses Playwright to navigate through category pages and product pages.
    """
    categories = [
        "https://timbermanor.in/collections/armchairs",
        "https://timbermanor.in/collections/bar-cabinets",
        "https://timbermanor.in/collections/beds",
        "https://timbermanor.in/collections/bedside-tables",
        "https://timbermanor.in/collections/frontpage",
        "https://timbermanor.in/collections/book-shelves",
        "https://timbermanor.in/collections/cabinets-1",
        "https://timbermanor.in/collections/cane-rattan-beds",
        "https://timbermanor.in/collections/seater",
        "https://timbermanor.in/collections/chest-of-drawers",
        "https://timbermanor.in/collections/tables",
        "https://timbermanor.in/collections/console-tables",
        "https://timbermanor.in/collections/cupboards-wardrobes",
        "https://timbermanor.in/collections/day-beds",
        "https://timbermanor.in/collections/dining-tables",
        "https://timbermanor.in/collections/dressers",
        "https://timbermanor.in/collections/end-tables",
        "https://timbermanor.in/collections/kitchen-items",
        "https://timbermanor.in/collections/nightstands",
        "https://timbermanor.in/collections/ottomans-benches",
        "https://timbermanor.in/collections/premium-beds",
        "https://timbermanor.in/collections/sideboards",
        "https://timbermanor.in/collections/loungers",
        "https://timbermanor.in/collections/solidwood-beds",
        "https://timbermanor.in/collections/study-desk-writing-tables",
        "https://timbermanor.in/collections/cabinets",
        "https://timbermanor.in/collections/whitman-collection",
        "https://timbermanor.in/collections/whitman-collection-1"
    ]

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        all_products = []
        for category_url in categories:
            products = scrape_category(page, category_url)
            all_products.extend(products)

        browser.close()

    # Create DataFrame and save to CSV
    df = pd.DataFrame(all_products)
    df.to_csv('timbermanor_products.csv', index=False)
    print(df)

# Run the scraper
scrape_all_categories()
