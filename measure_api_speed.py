import requests
import time
import numpy as np

# Define the API endpoints
GET_ALL_BOOKS_API_URL = 'http://127.0.0.1:8000/getbooks'
GET_BOOK_BY_NAME_API_URL = 'http://127.0.0.1:8000/getbook/{book_name}'

try:
    # Get all book names
    response = requests.get(GET_ALL_BOOKS_API_URL, verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error fetching book names: {e}")
    exit()

all_books = response.json()
book_names = [book['name'] for book in all_books]

# Initialize a list to store response times
response_times = []

# Loop through the book names and measure the response time
for book_name in book_names:
    try:
        url = GET_BOOK_BY_NAME_API_URL.format(book_name=book_name)
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        
        time_taken = end_time - start_time
        response_times.append(time_taken)
        
        print(f"Book name: {book_name}")
        print(f"Response time: {time_taken:.4f} seconds")
        print('-' * 50)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching book '{book_name}': {e}")

# Calculate and print the average response time
if response_times:
    average_response_time = sum(response_times) / len(response_times)
    print(f"Average response time for {len(book_names)} books: {average_response_time:.4f} seconds")
    
    # Calculate percentiles
    p50 = np.percentile(response_times, 50)
    p90 = np.percentile(response_times, 90)
    p95 = np.percentile(response_times, 95)
    p99 = np.percentile(response_times, 99)
    
    # Print percentiles
    print(f"P50 (Median) response time: {p50:.4f} seconds")
    print(f"P90 response time: {p90:.4f} seconds")
    print(f"P95 response time: {p95:.4f} seconds")
    print(f"P99 response time: {p99:.4f} seconds")
else:
    print("No response times recorded.")
