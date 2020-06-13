import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Oqhs7hRXH5nTCEmltXjXg","isbns":"9781632168146"})
print(res.json())