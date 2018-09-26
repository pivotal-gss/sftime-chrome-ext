/**
 * here we will inject javascript to automatically trigger the time
 * logging prompt on ticket update and also disable the automatic 
 * session time stopwatch from running
 */ 

window.addEventListener ("load", main, false);

function main (evt) {
    var stopwatchTimer = setInterval (disableStopwatch, 1000);

    function disableStopwatch () {
        console.debug("sftime:: checking if session timer stopwatch is present")
        // disable automatic time tracking as soon as it is loaded
        if (document.querySelector ("#stop")) {  
            // clearInterval (stopwatchTimer);
            document.getElementById("stop").click();
            console.log("sftime:: stopwatch paused")
        }
    }
}
