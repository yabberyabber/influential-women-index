from PageRank import PageRank

def weight_function( frequency ):
  return 1 / frequency

pr = PageRank( weight_function )
page_content = 'The quick brown fox jumped over the lazy dog.'
page_category = 'Whatevs'
page_id = '0'

pr.populate( page_content, page_category, page_id )
pr.dump_lookup_table()
