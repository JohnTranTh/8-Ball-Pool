$(document).ready(function() {
    var cueBallX, cueBallY;
    var pt, lineEnd;
    var isDragging = false;
    var line = null;
    var currentTime = 0.0;
    var frameInterval = 0.01;
    var svg;
    var serverURL = "table-";
    var serverEnd = ".svg";
    var myInterval;
    var counter = 0;
    var numberOfFrames = 0;
    var tableFrames;
    var currentPlayer = Math.floor(Math.random() * 2);
    var high = 0;
    var oldLowBalls = 0;
    var oldHighBalls = 0;
    var newLowBalls = 0;
    var newHighBalls = 0;
    var blackBall = 0;
    const player1Name = $("#player1").val()
    const player2Name = $("#player2").val()
    const LOW = 0;
    const HIGH = 1;
    var player1LowHigh;
    var player2LowHigh;
    var firstSink = 0;
    const PLAYER1 = 0
    const PLAYER2 = 1;

    if (currentPlayer == 0) {
        $("#player-turn").html("Current turn: " + player1Name);
    }
    else {
        $("#player-turn").html("Current turn: " + player2Name);
    }

    $(document).on("mousedown", "#cue-ball", function(event) {
        svg = document.getElementById('pool-table');
        cueBallX = $("#cue-ball").attr("cx");
        cueBallY = $("#cue-ball").attr("cy");
        isDragging = true;

        pt = new DOMPoint(event.clientX, event.clientY);

        // Transform pt into svg coordinates
        svg = document.getElementById('pool-table');
        lineEnd = pt.matrixTransform(svg.getScreenCTM().inverse());

        line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        $(line).attr({
            'x1': cueBallX,
            'y1': cueBallY,
            'x2': lineEnd.x,
            'y2': lineEnd.y,
            'stroke': 'black',
            'stroke-width': 3
          });
        $("#pool-table").append(line);

    });

    $(document).on("mousemove", function(event) {
        if (isDragging) {
            pt = new DOMPoint(event.clientX, event.clientY);
            lineEnd = pt.matrixTransform(svg.getScreenCTM().inverse());

            $("line").attr({
                'x2': lineEnd.x,
                'y2': lineEnd.y
            });

        }
    });

    $(document).on("mouseup", function(event) {
        if (isDragging) {
            isDragging = false;
            line.remove();
            var velX = cueBallX - lineEnd.x;
            var velY = cueBallY - lineEnd.y;

            $.ajax({
                url: 'poolGame.html',
                type: 'POST',
                data: JSON.stringify({velX: velX, velY: velY}),
                contentType: 'application/json',
                success: function(response) {
                    tableFrames = response.split("*");
                    numberOfFrames = tableFrames.length - 1;
                    oldLowBalls = $("[id=low-ball]").length;
                    oldHighBalls = $("[id=high-ball]").length;
                    myInterval = setInterval(animateShot, 10);
                }
            });
        }
    });

    function animateShot() {
        if (tableFrames[counter] != '') {
            $("#pool-table-container").html(tableFrames[counter]);
        }
        counter++;
        if (counter > numberOfFrames) {
            counter = 0;
            clearInterval(myInterval);
            newLowBalls = $("[id=low-ball]").length;
            newHighBalls = $("[id=high-ball]").length;
            blackBall = $("[id=black-ball]").length;

            if (firstSink == 0) {
                // First shot, black ball sunk
                if (blackBall == 0) {
                    blackBallSinkLose();
                }
                // Start table with no balls sunk
                else if ((newLowBalls + newHighBalls) == 14) {
                    switchTurnValue();
                    switchTurnText();
                }
                // Assign low balls to player. If a low and high are sunk, player is assigned lows.
                else if (newLowBalls < oldLowBalls) {
                    if (currentPlayer == PLAYER1) {
                        $("#player1-text").append(" Low");
                        $("#player2-text").append(" High");
                        player1LowHigh = LOW;
                        player2LowHigh = HIGH;
                    }
                    else {
                        $("#player1-text").append(" High");
                        $("#player2-text").append(" Low");  
                        player1LowHigh = HIGH;
                        player2LowHigh = LOW;
                    }
                    firstSink = 1;
                }
                else if (newHighBalls < oldHighBalls) {
                    if (currentPlayer == PLAYER1) {
                        $("#player1-text").append(" High");
                        $("#player2-text").append(" Low");
                        player1LowHigh = HIGH;
                        player2LowHigh = LOW;
                    }
                    else {
                        $("#player1-text").append(" Low");
                        $("#player2-text").append(" High");  
                        player1LowHigh = LOW;
                        player2LowHigh = HIGH;
                    }
                    firstSink = 1;
                }
            }
            else if (firstSink == 1) {

                if (blackBall == 0) {
                    if (currentPlayer == PLAYER1) {
                        if ((player1LowHigh == LOW) && (newLowBalls != 0)) {
                            blackBallSinkLose();
                        }
                        else if ((player1LowHigh == HIGH) && (newHighBalls != 0)) {
                            blackBallSinkLose();
                        }
                        else {
                            blackBallSinkWin();
                        }
                    }
                    else {
                        if ((player2LowHigh == LOW) && (newLowBalls != 0)) {
                            blackBallSinkLose();
                        }
                        else if ((player2LowHigh == HIGH) && (newHighBalls != 0)) {
                            blackBallSinkLose();
                        }
                        else {
                            blackBallSinkWin();
                        }
                    }
                }
                else if ((currentPlayer == PLAYER1) && (player1LowHigh == LOW) && (newLowBalls == oldLowBalls)) {
                    switchTurnValue();
                    switchTurnText();
                }
                else if ((currentPlayer == PLAYER1) && (player1LowHigh == HIGH) && (newHighBalls == oldHighBalls)) {
                    switchTurnValue();
                    switchTurnText();
                }
                else if ((currentPlayer == PLAYER2) && (player2LowHigh == LOW) && (newLowBalls == oldLowBalls)) {
                    switchTurnValue();
                    switchTurnText();
                }
                else if ((currentPlayer == PLAYER2) && (player2LowHigh == HIGH) && (newHighBalls == oldHighBalls)) {
                    switchTurnValue();
                    switchTurnText();
                }
            }
        }
    }

    function switchTurnValue() {
        currentPlayer++;
        currentPlayer = currentPlayer % 2;
    }

    function switchTurnText() {
        if (currentPlayer == 0) {
            $("#player-turn").html("Current turn: " + player1Name);
        }
        else {
            $("#player-turn").html("Current turn: " + player2Name);
        }
    }

    function blackBallSinkLose() {
        switchTurnValue();
        if (currentPlayer == 0) {
            $("#win-message").html(player1Name + " wins!");
        }
        else {
            $("#win-message").html(player2Name + " wins!");
        }    
    }

    function blackBallSinkWin() {
        if (currentPlayer == 0) {
            $("#win-message").html(player1Name + " wins!");
        }
        else {
            $("#win-message").html(player2Name + " wins!");
        }     
    }

    // function animateShot() {
    //     $("#pool-table").load(serverURL + currentTime.toFixed(2) + serverEnd,
    //         function (responseText, textStatus, XMLHttpRequest) {
    //             if (textStatus != "success") {
    //                 clearInterval(myInterval);
    //                 //alert("clear");
    //             }
    //             // else {
    //             //     alert(textStatus);
    //             // }
    //         });
    //     currentTime += frameInterval;
    // }

    // animateShot();

    // myInterval = setInterval(animateShot, 10);

});