This scraper uses the scrapy pipeline to scrap data from Medium Archives. For each post that is scraped from Medium Archive, the content of the post is also scraped. 

To run this scraper, the following command is to be run:

scrapy crawl -a start_date=20170901 -a end_date=20180930 -a tagSlug='data-science' -o "data_science//medium_scrapper_%(item_name)s.csv" -t csv  medium_scrapper 

start_date is the date from which you want the archive to be scrapped
end_date is the last data for which you want the data to be scrapped.
Tag_Slug is the Tag

