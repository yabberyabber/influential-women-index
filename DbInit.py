from Database import WikiDb
from PageRank import PageRank

def weight_function( frequency ):
  return 1 / frequency

article_json = [ ('wiki_json/female_explorers.json', 'Female Explorers'),
          ('wiki_json/women_nobel_laureates.json', 'Women Nobel Laureates'),
          ('wiki_json/women_computer_scientists.json', 'Women Computer Scientists'),
          ('wiki_json/women_company_founders.json', 'Women Company Founders'),
          ('wiki_json/women_prime_ministers.json', 'Women Prime Ministers'),
        ]

article_db = WikiDb( article_json )
lookup_table = PageRank( weight_function )

# Now you can query article_db and lookup_table using the standard APIs.
