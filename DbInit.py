from Database import WikiDb
from PageRank import PageRank

print "Added db init"

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

print "populating database"
for entry in article_db.db_entries():
  lookup_table.populate( article_db.get_article_content_by_id( entry ), entry )
print "populated database"

# Now you can query article_db and lookup_table using the standard APIs.
