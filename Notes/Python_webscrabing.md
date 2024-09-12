# Webscraping in Python
## Website which requires access
So, as  it seems right now I have to access OUH's ugeplan through the web-based version of HosInfo called (Altiplan).
To do this I needed a login.

### Scrape page which requires login/ secure access
How did I go about logging in and scraping the correct page? I tried some different approaches, but ultimately it prooved succesful to save the *cookies* and *headers* for the site, then I could use **Python's** `requests` library to inject these when getting the site.

#### Cookies and Headers to cURL
This [StackOverflow tip](https://stackoverflow.com/questions/23102833/how-to-scrape-a-website-which-requires-login-using-python-and-beautifulsoup#:~:text=64-,There,-is%20a%20simpler) said to login and then use some information contained in the *developer information* of *html* page, which could be copied to a *cURL*, which by using this [converter](https://curlconverter.com/) could convert the *cURL* to **Python** code. This Python code I then inject into my `requests.get( )` method (and it just works!)

