import collections
import math
import operator 
import get_freq_dict

class PageRank( object ):
  def __init__( self, weight_function, total_num_of_articles_in_data_base_ ):
    self.word_lookup_table = collections.defaultdict( lambda: collections.defaultdict( lambda: 0 ) )
    self.word_frequency = collections.defaultdict( lambda: 0 )
    self.weight_function = weight_function
    self.total_num_of_articles_in_data_base_ = total_num_of_articles_in_data_base_

  def extract_topics( self, page_content ):
    freq_dict = get_freq_dict.get_freq_dict( page_content )    
    return freq_dict

  def populate( self, page_content, page_id ):
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
    print "querying!!!!"
    # search_terms bag of doc A (dict)
    score_dict = collections.defaultdict( lambda:0 )
    for word, freq_query in search_terms.iteritems():
      for doc, freq_doc in self.word_lookup_table[word].iteritems():
        score_dict[doc] += math.log((freq_query * freq_doc * self.weight_function(self.word_frequency[word], freq_query, self.total_num_of_articles_in_data_base_)) + 1)
    sorted_x = sorted(score_dict.items(), key=operator.itemgetter(0))
    return dict(sorted(sorted_x, key=operator.itemgetter(1), reverse=True)[0:3])
 
