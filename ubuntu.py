import os
import requests
from urllib.parse import urlparse
import uuid

def fetch_image():
    url = input("Enter the URL of the image: ").strip()
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  
        
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename:  
            filename = f"image_{uuid.uuid4().hex}.jpg"
        
        save_dir = "Fetched_Images"
        os.makedirs(save_dir, exist_ok=True)  
        
        filepath = os.path.join(save_dir, filename)
        
        with open(filepath, "wb") as file:
            file.write(response.content)
        
        print(f"Image successfully saved to {filepath}")  
    
    except requests.exceptions.MissingSchema:
        print("❌ Invalid URL. Please include http:// or https://")
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Please check your internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Try again later.")
    except Exception as err:
        print(f"❌ An unexpected error occurred: {err}")

if __name__ == "__main__":
    fetch_image()
