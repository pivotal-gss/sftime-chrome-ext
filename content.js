/**
 * here we will inject javascript to automatically trigger the time
 * logging prompt on ticket update and also disable the automatic 
 * session time stopwatch from running
 */ 

window.addEventListener ("load", main, false);

function main (evt) {
    var stopwatchTimer = setInterval (timeCapture, 1000);

    function timeCapture() {
        disableStopwatch()
        postCapture()
        emailCapture()
    }

    function disableStopwatch () {
        console.debug("sftime:: checking if session timer stopwatch is present")
        // disable automatic time tracking as soon as it is loaded
        if (document.querySelector ("#stop")) {  
            // clearInterval (stopwatchTimer);
            document.getElementById("stop").click();
            console.log("sftime:: stopwatch paused")
        }  
    }

    function postCapture() {
        // Monitor for the button that get activited when the post button becomes active
        var selectCaseClickShareButton = document.querySelectorAll("div.slds-grid.bottomBar > div.bottomBarRight.slds-col--bump-left > button.slds-button.slds-button--neutral.cuf-publisherShareButton.qe-textPostDesktop.MEDIUM.uiButton--default.uiButton--brand.uiButton");
        if (Object.keys(selectCaseClickShareButton).length !== 0) {
            // When the user starts typing then button gets activited wait for the event.
            if (!selectCaseClickShareButton[0].disabled) {
                selectCaseClickShareButton[0].onclick = function () {
                    popUpTimer()
                }
            } 
        } 
    }

    function emailCapture() {
        // Hack the email button to track the time.
        var selectEmailSendButton = document.querySelectorAll("div.slds-grid.bottomBar > div.bottomBarRight.slds-col--bump-left > button.slds-button.slds-button--brand.cuf-publisherShareButton.MEDIUM.uiButton")
        if (Object.keys(selectEmailSendButton).length !== 0) {
            // When the user starts typing then button gets activited wait for the event.
            selectEmailSendButton[0].onclick = function () {
                    popUpTimer()
                }
        } 
    }

    function popUpTimer() {
        // Open up the modal of the timer
        var popUptheTimerModel = document.querySelectorAll("div.flexipageComponent > div.slds-hide.PCCTCaseTimer")
        popUptheTimerModel[0].classList.remove("slds-hide");
    }

}
