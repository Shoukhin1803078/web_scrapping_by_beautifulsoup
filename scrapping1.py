from bs4 import BeautifulSoup

html_doc = """
<html>
  <head><title>My First Page</title></head>
  <body>
    <h1>Welcome Bro 😎</h1>
    <p class="info">This is a paragraph</p>
    <a href="https://example.com">Click here</a>
  </body>
</html>
"""

soup = BeautifulSoup(html_doc, 'html.parser')

# title বের করা
print(soup.title.text)

# h1 বের করা
print(soup.h1.text)

# class দিয়ে find
print(soup.find('p', class_='info').text)

# link বের করা
print(soup.a['href'])

# পুরো HTML দেখার জন্য
print(soup.prettify())