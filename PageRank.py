import collections

class PageRank( object ):
  def __init__( self, weight_function ):
    self.word_lookup_table = collections.defaultdict( lambda: collections.defaultdict( lambda: 0 ) )
    self.word_frequency = collections.defaultdict( lambda: 0 )
    self.weight_function = weight_function

  def extract_topics( self, page_content ):
    newdict = collections.defaultdict( lambda: 0 )
    for word in page_content.split():
      newdict[ word ] += 1
    return newdict 

  def populate( self, page_content, page_category, page_id ):
    word_frequency_histogram = self.extract_topics( page_content )
    num_words = reduce( lambda x, y: x + y, word_frequency_histogram.values() )

    for word in word_frequency_histogram:
      self.word_lookup_table[ word ][ page_id ] = \
          float( word_frequency_histogram[ word ] ) / float( num_words )
      self.word_frequency[ word ] += word_frequency_histogram[ word ]

  def dump_lookup_table( self ):
    for word in self.word_lookup_table:
      print "PAGES CONTAINING %s:" % word
      for page in self.word_lookup_table[ word ]:
        print '\tPAGE ID: %s    FREQUENCY: %s' % ( page, self.word_lookup_table[ word ][ page ] )

  def word_weight( self, word ):
    return weight_function( self.word_frequency[ word ] )

  def query( self, search_terms ):
    pass
