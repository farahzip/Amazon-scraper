import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from dotenv import load_dotenv
import numpy as np
import time
import random

'''Amazon changes page layouts frequently, so any class and id names inside the functions 
might need to be checked for validity before running'''

# Function to extract product title
def get_title(soup):
    try:
        title = soup.find('span', attrs={'id': 'productTitle'}).text.strip()
    except AttributeError:
        title = "Not Available"
    return title

# Function to extract product price
def get_price(soup):
    try:
        price = soup.find('span', {'class': 'a-offscreen'}).text.strip()
    except AttributeError:
            price = "Not Available"
    return price

# Function to extract product rating
def get_rating(soup):
    try:
        rating = soup.find('span', attrs={'class': 'a-icon-alt'}).text.strip()
    except AttributeError:
        rating = "No Rating"
    return rating

# Function to extract number of user ratings
def get_rating_count(soup):
    try:
        rating_count = soup.find('span', {'id': 'acrCustomerReviewText'}).text.strip()
    except AttributeError:
        rating_count = "0"
    return rating_count

# Function to extract availability
def get_availability(soup):
    try:
        available = soup.find('div', attrs={'id': 'availability'}).find('span').text.strip()
    except AttributeError:
        available = "Not Available"
    return available


if __name__ == '__main__':
    print("Loading environment variables...")
    load_dotenv()

    URL = os.getenv('url')
    USER_AGENT = os.getenv('user_agent')

    if not URL or not USER_AGENT:
        print("Error: Missing URL or USER_AGENT in .env file")
        exit()

    print(f"Using URL: {URL}")
    print(f"Using User-Agent: {USER_AGENT}")

    HEADERS = {'User-Agent': USER_AGENT, 'Accept-Language': 'en-US, en;q=0.5'}

    try:
        print("Fetching Amazon page...")
        webpage = requests.get(URL, headers=HEADERS)
        webpage.raise_for_status()
        print("Page fetched successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Amazon page: {e}")
        exit()

    soup = BeautifulSoup(webpage.content, "html.parser")
    print("Parsing page content...")

    links = soup.find_all('a', attrs={'class': 'a-link-normal s-line-clamp-2 s-link-style a-text-normal'})

    if not links:
        print("Error: No product links found. Amazon might have changed the page structure.")
        exit()

    print(f"Found {len(links)} product links.")

    link_list = [link.get('href') for link in links]
    product_data = {'title': [], 'price': [], 'rating': [], 'rating_count': [], 'availability': []}

    for index, link in enumerate(link_list):
        try:
            print(f"Fetching product {index + 1}...")
            new_webpage = requests.get('https://amazon.com' + link, headers=HEADERS)
            new_webpage.raise_for_status()
            new_soup = BeautifulSoup(new_webpage.content, 'html.parser')

            title = get_title(new_soup)
            price = get_price(new_soup)
            rating = get_rating(new_soup)
            rating_count = get_rating_count(new_soup)
            availability = get_availability(new_soup)

            print(f"Title: {title}\n, Price: {price}\n, Rating: {rating}\n, Rating Count: {rating_count}\n, Availability: {availability}\n")

            product_data['title'].append(title)
            product_data['price'].append(price)
            product_data['rating'].append(rating)
            product_data['rating_count'].append(rating_count)
            product_data['availability'].append(availability)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching product page: {e}")

    # Convert to DataFrame
    amazon_df = pd.DataFrame.from_dict(product_data)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df.dropna(subset=['title'], inplace=True)

    # Save to CSV
    amazon_df.to_csv('amazon_data.csv', header=True, index=False)
    print("Scraping complete! Data saved to amazon_data.csv")
