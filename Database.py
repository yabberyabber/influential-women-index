# Copyright 2016 SKWAAD Inc.
# @author asethi77
# Fast in-memory database for rapidly analyzing Wikipedia documents

import json
import collections

class WikiDb:
  def __init__( self, json_data ):
    self.article_id_to_metadata = collections.defaultdict( lambda: collections.defaultdict( lambda: '' ) )
    for wiki_json, category in json_data:
      parsed_json = json.loads( open( wiki_json ).read() )
      self.load_json_to_db( parsed_json, category )

  def db_entries( self ):
      return [ entry for entry in self.article_id_to_metadata ]

  def load_json_to_db( self, wiki_json, category ):
    # NOTE: This doesn't *technically* match the page_id wikimedia assigns,
    # but for our purposes this is actually much more convenient to use.
    for page_id in wiki_json[ 'query' ][ 'pages' ]:
      page_details = wiki_json[ 'query' ][ 'pages' ][ page_id ]
      if not 'revisions' in page_details:
        continue
      self.article_id_to_metadata[ page_id ][ 'title' ] = page_details[ 'title' ]
      self.article_id_to_metadata[ page_id ][ 'wikitext' ] = page_details[ 'revisions' ][ 0 ][ '*' ]
      self.article_id_to_metadata[ page_id ][ 'category' ] = category
      self.article_id_to_metadata[ page_id ][ 'url' ] = \
          'https://en.wikipedia.org/wiki/%s' % page_details[ 'title' ].replace( ' ', '_' ) 

  def get_article_title_by_id( self, art_id ):
    if not art_id in self.article_id_to_metadata:
      raise KeyError( 'Unable to find %s in database' % art_id )

    return self.article_id_to_metadata[ art_id ][ 'title' ]

  def get_article_category_by_id( self, art_id ):
    if not art_id in self.article_id_to_metadata:
      raise KeyError( 'Unable to find %s in database' % art_id )

    return self.article_id_to_metadata[ art_id ][ 'category' ]

  def get_article_url_by_id( self, art_id ):
    if not art_id in self.article_id_to_metadata:
      raise KeyError( 'Unable to find %s in database' % art_id )

    return self.article_id_to_metadata[ art_id ][ 'url' ]

  def get_article_content_by_id( self, art_id ):
    if not art_id in self.article_id_to_metadata:
      raise KeyError( 'Unable to find %s in database' % art_id )

    return self.article_id_to_metadata[ art_id ][ 'wikitext' ]
