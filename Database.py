# Copyright 2016 SKWAAD Inc.
# @author asethi77
# Fast in-memory database for rapidly analyzing Wikipedia documents

import json
import urllib2
import collections
import requests
import os

class WikiDb:
  def __init__( self, json_data ):
    self.article_id_to_metadata = collections.defaultdict( lambda: collections.defaultdict( lambda: '' ) )
    self.queued_summaries = []
    if not os.path.exists( 'db_json.dat' ):
      for wiki_json, category in json_data:
        parsed_json = json.loads( open( wiki_json ).read() )
        self.load_json_to_db( parsed_json, category )

      db_file = open( 'db_json.dat', 'w' )
      db_file.write( json.dumps( self.article_id_to_metadata ) )
      db_file.close()
    else:
      self.article_id_to_metadata = json.loads( open( 'db_json.dat', 'r' ).read() )

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
      self.queued_summaries.append( ( page_id, page_details[ 'title' ] ) )

      if len( self.queued_summaries ) >= 20:
        self.get_summaries()
    self.get_summaries()

  def get_summaries( self ):
    print "fetching summary batch"
    title_string = ""
    while len( self.queued_summaries ) > 0:
      page_id, page_title = self.queued_summaries.pop()
      page_title = page_title.replace( ' ', '_' )
      title_string += "%s|" % page_title
    
    #query_str = "http://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=True&titles=%s&exlimit=20&explaintext=True&exsentences=2&format=json" % title_string
    api_endpoint = "http://en.wikipedia.org/w/api.php"
    params = {}
    params.update({
      'exlimit': '20',
      'titles': title_string,
      'action': 'query',
      'exintro': 'True',
      'explaintext': 'True',
      'prop': 'extracts',
      'exsentences': '2',
      'format': 'json',
    }) 
    response = requests.get( api_endpoint, params=params )
    json_str = json.loads( response.text )
    json_str = json_str["query"]["pages"]
    for page_id in json_str:
      if page_id != "-1":
        self.article_id_to_metadata[ page_id ][ 'summary' ] = json_str[ page_id ][ "extract" ]

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

  def get_article_summary_by_id( self, art_id ):
    if not art_id in self.article_id_to_metadata:
      raise KeyError( 'Unable to find %s in database' % art_id )

    return self.article_id_to_metadata[ art_id ][ 'summary' ]
