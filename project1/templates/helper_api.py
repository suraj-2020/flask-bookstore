import requests
import urllib.parse

def ratings(isbn):
	url="https://www.goodreads.com/book/review_counts.json?"
	key="Oqhs7hRXH5nTCEmltXjXg"
	params={"isbn":isbn,"key":key}
	full_url=url+ urllib.parse(params)

	data=requests.get(full_url).json()

	avg_rating=data['books'][0]['average_rating']
	no_rating=data['books'][0]['work_ratings_count']

	if not average_rating:
        average_rating = "Not found"
    if not number_ratings:
        number_ratings = "Not found"

    review_counts_result = {'average_rating': average_rating, 'number_ratings': number_ratings}

    return review_counts_result


