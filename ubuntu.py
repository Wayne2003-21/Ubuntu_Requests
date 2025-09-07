import os
import requests
from urllib.parse import urlparse
import uuid
import hashlib

def fetch_images():
    urls = input("Enter image URLs (separated by spaces): ").strip().split()
    
    save_dir = "Fetched_Images"
    os.makedirs(save_dir, exist_ok=True)  
    downloaded_hashes = set()
    
    for url in urls:
        print(f"\n🔗 Processing: {url}")
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status() 
            
            content_type = response.headers.get("Content-Type", "")
            content_length = response.headers.get("Content-Length", "Unknown")
            
            if "image" not in content_type:
                print("❌ Skipped: URL is not an image.")
                continue
            
            print(f"   Content-Type: {content_type}")
            print(f"   Content-Length: {content_length} bytes")
            
            file_bytes = response.content
            file_hash = hashlib.md5(file_bytes).hexdigest()
            if file_hash in downloaded_hashes:
                print(" Duplicate detected. Skipping download.")
                continue
            downloaded_hashes.add(file_hash)
        
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or "." not in filename:  # If no filename in URL, generate one
                extension = content_type.split("/")[-1] if "/" in content_type else "jpg"
                filename = f"image_{uuid.uuid4().hex}.{extension}"
            
            filepath = os.path.join(save_dir, filename)
            
           
            with open(filepath, "wb") as file:
                file.write(file_bytes)
            
            print(f"Image saved as {filepath}")
        
        except requests.exceptions.MissingSchema:
            print("Invalid URL. Please include http:// or https://")
        except requests.exceptions.HTTPError as http_err:
            print(f" HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Connection error. Check your internet connection.")
        except requests.exceptions.Timeout:
            print("Request timed out. Try again later.")
        except Exception as err:
            print(f" An unexpected error occurred: {err}")

if __name__ == "__main__":
    print(" Ubuntu Image Fetcher")
    print('"A person is a person through other persons." - Ubuntu Philosophy\n')
    fetch_images()
