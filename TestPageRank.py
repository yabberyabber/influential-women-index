from PageRank import PageRank
import math

def weight_function( frequency, tf, N ):
  #return 1.0 / frequency
  return math.log(N/frequency + 1 ) * tf

pr = PageRank( weight_function )
page_content = 'the quick brown fox jumped over the lazy dog'
page_category = 'Whatevs'
page_id = '0'

pr.populate( page_content, page_category, page_id )
pr.populate( 'the other dog jumped over the even lazier dog but it was dumb', 'Whatevs', '1' )
pr.dump_lookup_table()

print pr.query( { 'dog': 0.4, 'lazier': 0.2 } )

print pr.query( { 'cat': 0.3, 'lazy': 0.6 } )
