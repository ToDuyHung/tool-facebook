from facebook_scraper import get_posts

count = 0
for post in get_posts('mogivietnam'):
	if count == 8:break
	print(post)
	count += 1