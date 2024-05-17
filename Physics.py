import phylib;
import os
import sqlite3
import math

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER

HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH

SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON

DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME

MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
                      "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="pool-table" width="700" height="1375" viewBox="-25 -25 1400 2750"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

FRAME_INTERVAL = 0.01

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    # game logic
    def svg(self):
        if self.obj.still_ball.number == 0:
            result = (
                """ <circle id="cue-ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" 
                % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]))
        elif self.obj.still_ball.number >= 1 and self.obj.still_ball.number <= 7:
            result = (
                """ <circle id="low-ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" 
                % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]))
        elif self.obj.still_ball.number == 8:
            result = (
                """ <circle id="black-ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" 
                % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]))
        else:
            result = (
                """ <circle id="high-ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" 
                % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]))
        return result

################################################################################

class RollingBall( phylib.phylib_object ):
    
    def __init__ ( self, number, pos, vel, acc ):
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0 )
        
        self.__class__ = RollingBall

    def svg(self):
        result = (
            """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" 
            % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]))
        return result


class Hole( phylib.phylib_object ):
    
    def __init__ ( self, pos ):
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HOLE, 
                                       0, 
                                       pos, None, None, 
                                       0.0, 0.0 )
        
        self.__class__ = Hole

    def svg(self):
        result = """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS)
        return result

class HCushion( phylib.phylib_object ):
    
    def __init__ ( self, y ):
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_HCUSHION, 
                                       0, 
                                       None, None, None, 
                                       0.0, y )
        
        self.__class__ = HCushion

    def svg(self):
        if self.obj.hcushion.y == TABLE_LENGTH: #Bottom cushion
            result = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % 2700
        else:
            result = """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % -25

        return result


class VCushion( phylib.phylib_object ):
    
    def __init__ ( self, x ):
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_VCUSHION, 
                                       0, 
                                       None, None, None, 
                                       x, 0.0 )
        
        self.__class__ = VCushion

    def svg(self):
        if self.obj.vcushion.x == TABLE_WIDTH: #Right cushion
            result = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % 1350
        else:
            result = """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % -25

        return result


class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        result = ""
        result += HEADER
        for object in self:
            if object is not None:
                result += object.svg()
        result += FOOTER

        return result
    
    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );

                # add ball to table
                new += new_ball;
        
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                    Coordinate( ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;

        # return table
        return new;

    def cueBall( self, xvel, yvel ):

        for cue_ball in self:
            if isinstance(cue_ball, StillBall):
                if cue_ball.obj.still_ball.number == 0:
                    xpos = cue_ball.obj.still_ball.pos.x
                    ypos = cue_ball.obj.still_ball.pos.y

                    cue_ball.type = phylib.PHYLIB_ROLLING_BALL
                    cue_ball.obj.rolling_ball.pos.x = xpos
                    cue_ball.obj.rolling_ball.pos.y = ypos
                    cue_ball.obj.rolling_ball.vel.x = xvel
                    cue_ball.obj.rolling_ball.vel.y = yvel

                    speed = math.sqrt((xvel * xvel) + (yvel * yvel))

                    xacc = (xvel * -1.0 / speed) * DRAG
                    yacc = (yvel * -1.0 / speed) * DRAG
                    
                    cue_ball.obj.rolling_ball.acc.x = xacc
                    cue_ball.obj.rolling_ball.acc.y = yacc
                    cue_ball.obj.rolling_ball.number = 0

    def isCueBallGone(self):

        cue_ball_status = 0

        for cue_ball in self:
            if isinstance(cue_ball, StillBall):
                if cue_ball.obj.still_ball.number == 0:
                    cue_ball_status = 1
        
        return cue_ball_status


class Database:

    def __init__( self, reset=False ):

        if reset:
            if os.path.exists( 'phylib.db' ):
                os.remove( 'phylib.db' )

        # create database file if it doesn't exist and connect to it
        self.conn = sqlite3.connect( 'phylib.db' )

    def createDB( self ):

        cur = self.conn.cursor()

        cur.execute( """ CREATE TABLE IF NOT EXISTS Ball (
                                BALLID      INTEGER NOT NULL,
                                BALLNO      INTEGER NOT NULL,
                                XPOS        FLOAT NOT NULL,
                                YPOS        FLOAT NOT NULL,
                                XVEL        FLOAT,
                                YVEL        FLOAT,
                                PRIMARY KEY (BALLID AUTOINCREMENT) ) """ )
            
        cur.execute( """ CREATE TABLE IF NOT EXISTS TTable (
                                TABLEID     INTEGER NOT NULL,
                                TIME        FLOAT NOT NULL,
                                PRIMARY KEY (TABLEID AUTOINCREMENT) ) """ )
            
        cur.execute( """ CREATE TABLE IF NOT EXISTS BallTable (
                                BALLID      INTEGER NOT NULL,
                                TABLEID     INTEGER NOT NULL,
                                FOREIGN KEY (BALLID) REFERENCES Ball,
                                FOREIGN KEY (TABLEID) REFERENCES TTable ) """ )

        cur.execute( """ CREATE TABLE IF NOT EXISTS Game (
                                GAMEID      INTEGER NOT NULL,
                                GAMENAME    VARCHAR(64) NOT NULL,
                                PRIMARY KEY (GAMEID AUTOINCREMENT) ) """ )

        cur.execute( """ CREATE TABLE IF NOT EXISTS Player (
                                PLAYERID    INTEGER NOT NULL,
                                GAMEID      INTEGER NOT NULL,
                                PLAYERNAME  VARCHAR(64) NOT NULL,
                                PRIMARY KEY (PLAYERID AUTOINCREMENT),
                                FOREIGN KEY (GAMEID) REFERENCES Game ) """ )   

        cur.execute( """ CREATE TABLE IF NOT EXISTS Shot (
                                SHOTID      INTEGER NOT NULL,
                                PLAYERID    INTEGER NOT NULL,
                                GAMEID      INTEGER NOT NULL,
                                PRIMARY KEY (SHOTID AUTOINCREMENT)
                                FOREIGN KEY (PLAYERID) REFERENCES Player,
                                FOREIGN KEY (GAMEID) REFERENCES Game ) """ )

        cur.execute( """ CREATE TABLE IF NOT EXISTS TableShot (
                                TABLEID     INTEGER NOT NULL,
                                SHOTID      INTEGER NOT NULL,
                                FOREIGN KEY (TABLEID) REFERENCES TTable,
                                FOREIGN KEY (SHOTID) REFERENCES Shot ) """ )         
    
        cur.close()
        self.conn.commit()

    def readTable( self, tableID ):

        cur = self.conn.cursor()

        table = Table()

        ballList = cur.execute(""" SELECT * FROM (BallTable INNER JOIN Ball
                                ON BallTable.BALLID = Ball.BALLID
                                INNER JOIN TTable
                                ON BallTable.TABLEID = TTable.TABLEID)
                                WHERE BallTable.TABLEID = '%d' """ % (tableID + 1)).fetchall()
        
        if len(ballList) == 0:
            return None

        for ball in ballList:
            ballNo = ball[3]
            xpos = ball[4]
            ypos = ball[5]
            xvel = ball[6]
            yvel = ball[7]
            
            if xvel == None and yvel == None:
                pos = Coordinate(xpos, ypos)
                sb = StillBall(ballNo, pos)
                table += sb

            else:
                pos = Coordinate(xpos, ypos)
                vel = Coordinate(xvel, yvel)

                speed = math.sqrt((xvel * xvel) + (yvel * yvel))

                xacc = (xvel * -1.0 / speed) * DRAG
                yacc = (yvel * -1.0 / speed) * DRAG
                acc = Coordinate(xacc, yacc)

                rb = RollingBall(ballNo, pos, vel, acc)
                table += rb

        
        time = cur.execute(""" SELECT TIME FROM (TTable)
                                    WHERE TTable.TABLEID = '%d' """ % (tableID + 1)).fetchone()[0]
        
        table.time = time

        cur.close()
        self.conn.commit()

        return table


    def writeTable( self, table ):

        cur = self.conn.cursor()

        cur.execute(""" INSERT
                                INTO TTable (TIME)
                                VALUES      ('%f') """ % (table.time))
        
        tableID = cur.lastrowid
        
        for ball in table:
            if isinstance(ball, StillBall):

                cur.execute(""" INSERT
                                        INTO Ball (BALLNO, XPOS, YPOS)
                                        VALUES    ('%d',  '%f', '%f') """ 
                                        % (ball.obj.still_ball.number,
                                           ball.obj.still_ball.pos.x,
                                           ball.obj.still_ball.pos.y))
                
                ballID = cur.lastrowid

                cur.execute(""" INSERT
                                        INTO BallTable (BALLID, TABLEID)
                                        VALUES         ('%d', '%d') """ % (ballID, tableID))
                
            if isinstance(ball, RollingBall):

                cur.execute(""" INSERT
                                        INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                        VALUES    ('%d',  '%f', '%f', '%f', '%f') """ 
                                        % (ball.obj.rolling_ball.number,
                                           ball.obj.rolling_ball.pos.x,
                                           ball.obj.rolling_ball.pos.y,
                                           ball.obj.rolling_ball.vel.x,
                                           ball.obj.rolling_ball.vel.y))
                
                ballID = cur.lastrowid

                cur.execute(""" INSERT
                                        INTO BallTable (BALLID, TABLEID)
                                        VALUES         ('%d', '%d') """ % (ballID, tableID))
                
        cur.close()
        self.conn.commit()

        return tableID - 1
            
    def close( self ):

        self.conn.commit()
        self.conn.close()

    def getGame( self, gameID ):

        cur = self.conn.cursor()

        game = cur.execute(""" SELECT * FROM (Game INNER JOIN Player
                                ON Game.GAMEID = Player.GAMEID)
                                WHERE Game.GAMEID = '%d' 
                                ORDER BY Player.PLAYERID """ % (gameID)).fetchall()

        player1 = game[0]
        gameName = player1[1]
        player1Name = player1[4]

        player2 = game[1]
        player2Name = player2[4] 

        cur.close()
        self.conn.commit()

        return gameName, player1Name, player2Name
    
    def setGame( self, gameName, player1Name, player2Name ):
        
        cur = self.conn.cursor()

        cur.execute(""" INSERT
                            INTO Game (GAMENAME)
                            VALUES    ('%s') """ % (gameName))
        
        gameID = cur.lastrowid
        
        cur.execute(""" INSERT
                            INTO Player (GAMEID, PLAYERNAME)
                            VALUES    ('%d', '%s') """ % (gameID, player1Name))
        
        cur.execute(""" INSERT
                            INTO Player (GAMEID, PLAYERNAME)
                            VALUES    ('%d', '%s') """ % (gameID, player2Name))

        cur.close()
        self.conn.commit()

        return gameID

    def newShot( self, gameID, playerName ):

        cur = self.conn.cursor()

        playerID = cur.execute(""" SELECT PLAYERID FROM Player
                                        WHERE (Player.GAMEID = '%d') AND (PLAYERNAME = '%s') """ % (gameID, playerName)).fetchone()[0]
 
        cur.execute(""" INSERT
                            INTO Shot (PLAYERID, GAMEID)
                            VALUES    ('%d', '%d') """ % (playerID, gameID))

        shotID = cur.lastrowid

        cur.close()
        self.conn.commit()

        return shotID
        
    def setTableShot( self, tableID, shotID ):

        cur = self.conn.cursor()
        tableID += 1

        cur.execute(""" INSERT
                            INTO TableShot (TABLEID, SHOTID)
                            VALUES         ('%d', '%d') """ % (tableID, shotID))

        cur.close()
        self.conn.commit()


class Game:

    def __init__( self, gameID = None, gameName = None, player1Name = None, player2Name = None ):

        self.gameID = gameID
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name

        if gameID != None and gameName == None and player1Name == None and player2Name == None:
            database = Database()
            database.createDB()
            self.gameID += 1
            self.gameName, self.player1Name, self.player2Name = database.getGame(self.gameID)
            database.close()

        elif gameID == None and gameName != None and player1Name != None and player2Name != None:
            database = Database()
            database.createDB()
            self.gameID = database.setGame(gameName, player1Name, player2Name)
            database.close()

        else:
            raise TypeError
        
    def shoot( self, gameName, playerName, table, xvel, yvel ):

        tableFrames = ""
        delimiter = "*"

        database = Database()

        endTable = table

        shotID = database.newShot(self.gameID, playerName)

        table.cueBall(xvel, yvel)

        while endTable:
            initialTime = table.time
            endTable = table.segment()
            if endTable != None:
                endTime = endTable.time
                elapsedTime = int((endTime - initialTime) // FRAME_INTERVAL)
                for time in range(elapsedTime + 1):
                    rollTime = time * FRAME_INTERVAL
                    frameTable = table.roll(rollTime)
                    frameTable.time = initialTime + rollTime
                    frame = frameTable.svg()
                    tableFrames += frame + delimiter
                    # tableID = database.writeTable(frameTable)
                    # database.setTableShot(tableID, shotID)
                table = table.segment()
                tableFrames += table.svg() + delimiter

        if (table.isCueBallGone() == 0):
            pos = Coordinate( TABLE_WIDTH/2.0 + 1.0,
                TABLE_LENGTH - TABLE_WIDTH/2.0 );
            sb  = StillBall( 0, pos );
            table += sb
            tableFrames += table.svg() + delimiter

        database.close()
        return tableFrames, table
            