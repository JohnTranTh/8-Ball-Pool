import sys; # used to get argv
import cgi; # used to parse Mutlipart FormData 
            # this should be replace with multipart in the future

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler;

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qsl

import os
import math
import Physics
import json

# Setup
def setupTable():
    table = Physics.Table()
    # 1 ball
    pos = Physics.Coordinate( 
                    Physics.TABLE_WIDTH / 2.0,
                    (Physics.TABLE_WIDTH / 2.0) + 5.0,
                    );

    sb = Physics.StillBall( 1, pos );
    table += sb;

    # 2 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 +
                    -1.0,
                    Physics.TABLE_WIDTH/2.0 - 
                    math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                    1.0
                    );
    sb = Physics.StillBall( 2, pos );
    table += sb;

    # 3 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 +
                    1.0,
                    Physics.TABLE_WIDTH/2.0 - 
                    math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER+4.0) +
                    2.0
                    );
    sb = Physics.StillBall( 9, pos );
    table += sb;

    # 4 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER*2+4.0)/2.0 + 4.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*2+4.0) - 2.0
                    );
    sb = Physics.StillBall( 10, pos );
    table += sb;

    # 5 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER*2+4.0)/2.0 - 4.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*2+4.0) - 4.0
                    );
    sb = Physics.StillBall( 3, pos );
    table += sb;

    # 6 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - 1.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*2+4.0) - 4.0
                    );
    sb = Physics.StillBall( 8, pos );
    table += sb;

    # 7 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER*3+4.0)/2.0 + 8.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*3+4.0) - 8.0
                    );
    sb = Physics.StillBall( 11, pos );
    table += sb;

    # 8 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER*3+4.0)/2.0 - 9.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*3+4.0) - 10.0
                    );
    sb = Physics.StillBall( 7, pos );
    table += sb;

    # 9 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER+4.0)/2.0 - 3.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*3+4.0) - 11.0
                    );
    sb = Physics.StillBall( 14, pos );
    table += sb;

    # 10 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER+4.0)/2.0 - 1.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*3+4.0) - 11.0
                    );
    sb = Physics.StillBall( 4, pos );
    table += sb;

    # 11 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER*4+4.0)/2.0 + 11.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*4+4.0) - 19.0
                    );
    sb = Physics.StillBall( 5, pos );
    table += sb;

    # 12 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER*4+4.0)/2.0 - 8.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*4+4.0) - 22.0
                    );
    sb = Physics.StillBall( 12, pos );
    table += sb;

    # 13 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 - (Physics.BALL_DIAMETER*2+4.0)/2.0 - 2.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*4+4.0) - 22.0
                    );
    sb = Physics.StillBall( 13, pos );
    table += sb;

    # 14 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + (Physics.BALL_DIAMETER*2+4.0)/2.0 + 4.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*4+4.0) - 22.0
                    );
    sb = Physics.StillBall( 6, pos );
    table += sb;

    # 15 ball
    pos = Physics.Coordinate(
                    Physics.TABLE_WIDTH/2.0 + 2.0,
                    Physics.TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(Physics.BALL_DIAMETER*4+4.0) - 22.0
                    );
    sb = Physics.StillBall( 15, pos );
    table += sb;

    # cue ball also still
    pos = Physics.Coordinate( Physics.TABLE_WIDTH/2.0 + 1.0,
                            Physics.TABLE_LENGTH - Physics.TABLE_WIDTH/2.0 );
    sb  = Physics.StillBall( 0, pos );

    table += sb;

    return table

game = None
startTable = None

class MyHandler( BaseHTTPRequestHandler ):
    def do_GET(self):
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )

        if parsed.path in [ '/startPage.html' ]:

            # retreive the HTML file
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/poolGame.html' ]:

            form_data = dict(parse_qsl(parsed.query))

            gameName = form_data.get("gameName")
            player1 = form_data.get("player1")
            player2 = form_data.get("player2")

            # retreive the HTML file
            fp = open( '.'+parsed.path )
            content = fp.read() % form_data

            global game, startTable

            game = Physics.Game(gameName=gameName, player1Name=player1, player2Name=player2)
            startTable = setupTable()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/style.css' ]:

            # retreive the HTML file
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/css" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()

        elif parsed.path in [ '/script.js' ]:

            # retreive the HTML file
            fp = open( '.'+self.path )
            content = fp.read()

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/javascript" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            # send it to the broswer
            self.wfile.write( bytes( content, "utf-8" ) )
            fp.close()
        
        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
            # this one is different because its an image file

            # retreive the svg file (binary, not text file)
            fp = open( '.'+self.path, 'rb' )
            content = fp.read()

            self.send_response( 200 ); # OK
                # notice the change in Content-type
            self.send_header( "Content-type", "image/svg+xml" )
            self.send_header( "Content-length", len( content ) )
            self.end_headers()

            self.wfile.write( content )    # binary file
            fp.close()

        else:
            # generate 404 for GET requests that aren't the 2 files above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

    def do_POST(self):
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path )
        global game
        global startTable

        # if parsed.path in ['/startGame']:
        #     # form = cgi.FieldStorage( fp=self.rfile,
        #     #                          headers=self.headers,
        #     #                          environ = { 'REQUEST_METHOD': 'POST',
        #     #                                      'CONTENT_TYPE': 
        #     #                                        self.headers['Content-Type'],
        #     #                                    } 
        #     #                        )
        #     form_data = dict(parse_qsl(parsed.query))
        #     poolName = form_data.get("gameName")
        #     player1 = form_data.get("player1")
        #     player2 = form_data.get("player2")
        #     print(form_data)
        #     print(poolName, player1, player2)

        #     #game = Physics.Game(gameName=poolName, player1Name=player1, player2Name=player2)
        #     #startTable = setupTable()

        #     self.send_response(302, "Found")
        #     self.send_header('Location', '/poolGame.html')
        #     self.end_headers()

        if parsed.path in [ '/poolGame.html' ]:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))

            velX = post_data['velX']
            velY = post_data['velY']

            constant_power = 4
            velX = velX * constant_power
            velY = velY * constant_power

            max_speed = 10000
            vector_length = math.sqrt(velX * velX + velY * velY)

            if abs(velX) > max_speed:
                velX = velX * (max_speed / vector_length)
            if abs(velY) > max_speed:
                velY = velY * (max_speed / vector_length)

            table_frames, startTable = game.shoot(game.gameName, game.player1Name, startTable, velX, velY)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(table_frames.encode('utf-8'))

        else:
        # generate 404 for POST requests that aren't the file above
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )


if __name__ == "__main__":
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler )
    httpd.serve_forever()
