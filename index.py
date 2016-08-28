import DbInit
import PageRank
from flask import *
from matching import Matcher
import json
import urllib2
import get_freq_dict as get_freqy
import MarkupConverter as michaels_text_api
from OpenSSL import SSL
import os

context = SSL.Context(SSL.SSLv23_METHOD)
cer = os.path.join( os.getcwd(), 'DESKTOP-SMQH0LD.crt' )
key = os.path.join( os.getcwd(), 'DESKTOP-SMQH0LD.key' )

print cer
print key
print __file__

app = Flask( __name__ )

@app.route( '/' )
@app.route( '/search' )
def handle_non_api_request():
    query = request.args.get( 'query', None )
    template_args = {}

    if query:
        template_args[ 'longintro' ] = False
        template_args[ 'showresults' ] = True
        matches = Matcher().find_matches_for( query )
        print matches
        template_args[ 'results' ] = matches
    else:
        template_args[ 'longintro' ] = True
        template_args[ 'showresults' ] = False

    return render_template( 'front_page.html', **template_args )

@app.route( '/api' )
def handle_api_request():
    query = request.args.get( 'query', None )
    print query
    if not query or 'wikipedia' not in query:
      return {}
    print 'you know what dat query is'
    print query
    webpage = urllib2.urlopen( query ).read() 
    print 'calling michaels api'
    text = michaels_text_api.htmlToPlain( webpage )
    print 'called michaels api'
    bag_of_words = get_freqy.get_freq_dict( text )
    
    results = DbInit.lookup_table.query( bag_of_words )
    print results
    ret_list = []
    for article_id, score in sorted(results.items(), key=lambda x: x[1], reverse=True):
      article_title = DbInit.article_db.get_article_title_by_id( article_id )
      article_url = DbInit.article_db.get_article_url_by_id( article_id )
      article_summary = DbInit.article_db.get_article_summary_by_id( article_id )
      ret_list.append( { 'title': article_title, 'url': article_url, 'summary': article_summary } )
    response = jsonify( json.dumps( ret_list ) )
    response.status_code = 200
    return response

if __name__ == '__main__':
  context = (cer, key)
  app.run( host='0.0.0.0', port=5123, debug=True, ssl_context=context )
