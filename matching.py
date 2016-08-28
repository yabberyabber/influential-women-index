from collections import namedtuple
def Match( title, url, summary ):
	return { 'title': title,
			 'url': url,
			 'summary': summary }

DUMMY_MATCHES = [
		Match( 'Google is a website', 'http://google.com', 'Google lets you searc for stuff' ),
		Match( 'Amazon is also a website', 'http://amazon.com', 'Amazon lets u buy stuff' ),
		]

class Matcher( object ):
	def __init__( self ):
		pass

	def _fetch_page( self ):
		pass

	def _vectorize_page( self ):
		DUMMY_BAG_OF_WORDS = {
				'apple': 2,
				'cat': 7,
				'poop': 17 }
		return { 'tf': DUMMY_BAG_OF_WORDS,
				 'doc_len': 26 }

	def _find_tf_idf_matches( self, tf, doc_len ):
		pass

	def find_matches_for( self, url ):
		return DUMMY_MATCHES
