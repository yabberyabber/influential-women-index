import re
import operator
import string
import os
from bs4 import BeautifulSoup

def wikiToHtml( wikitext=None ):
   bashCommand = "pandoc -f mediawiki -t html5 -s temp.txt -o wiki.html"
   
   try:
      tempFile = open( 'temp.txt', 'w' )
   except IOError:
      print "File already exists"

   if not wikitext:
      raise TypeError( "Missing wikitext" )   

   tempFile.write( wikitext )
   tempFile.close()

   os.system( bashCommand )
   os.system( 'rm temp.txt' )

   try:
      htmlFile = open( 'wiki.html', 'r' )
   except IOError:
      print "Something went horribly wrong"

   rawHtml = htmlFile.read()
   return rawHtml

def htmlToPlain( htmlText=None ):
   if not htmlText:
      raise TypeError( "Missing htmlText" )
      
   soup = BeautifulSoup( htmlText, "html.parser" )
   data = soup.findAll( text=True )
   
   def visible( element ):
      if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
         return False;
      elif re.match('<!--.*-->', str(element.encode('utf-8'))):
         return False
      return True

   result = filter( visible, data )
   return reduce( lambda x, y: x + y, result )

      
            

