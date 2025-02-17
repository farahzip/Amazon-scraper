# Amazon-scraper
A Python scraper that extracts product details from each listing on an Amazon product page.  

## Features  
- Scrapes the following product details:  
  - Title  
  - Price  
  - Rating  
  - Review count  
  - Availability status  
- Saves extracted data into a CSV file  
- Handles errors  
- Uses environment variables for configuration  

## Installation  

1. Clone this repository
   
   ```sh
   git clone https://github.com/yourusername/amazon-scraper.git

3. Navigate to the project directory

   ```sh
   cd amazon-scraper

4. Install required packages
   
   ```sh
   pip install -r requirements.txt

5. Set up environment variables

   - Create a .env file in the project root
   - Add the following details:
     
   ```env
   URL="https://www.amazon.com/dp/example-product-id"
   USER_AGENT="your-browser-user-agent"
   
## Usage

1. Run the script:
   
   ```sh
   python app.py

2. Example output:
   
   ```makefile
   Fetching product details...
   Title: Sample Product
   Price: $19.99
   Rating: 4.5/5
   Reviews: 1,234
   Availability: In Stock

4. Data is saved in CSV format

   - Default filename: amazon_data.csv
   - Stored in the current directory


## Notes

    ⚠ Amazon frequently updates its page structure, which may break the scraper.
    If the script stops working, inspect the product page and update the class or ID selectors in the code.

