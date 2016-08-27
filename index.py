from flask import *
from matching import Matcher
import json
app = Flask( __name__ )

@app.route( '/' )
@app.route( '/search' )
def handle_non_api_request():
    query = request.args.get( 'query', None )
    print query
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
    matches = Matcher().find_matches_for( query )
    return json.dumps( matches )
