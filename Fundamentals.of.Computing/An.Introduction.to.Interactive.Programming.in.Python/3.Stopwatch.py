# http://www.codeskulptor.org/

# Import modules
import simplegui

# define global variables
currentTime = 0
stopwatchIsRunning = False
successfulAttempts = 0
totalAttempts = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    
    minutes = t / 600
    seconds = (t % 600) // 10
    tenths = t % 10
    
    if (seconds < 10):
        formattedTime = str(minutes) + ":0" + str(seconds) + "." + str(tenths)
    else:
        formattedTime = str(minutes) + ":" + str(seconds) + "." + str(tenths)
    
    
    return formattedTime
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    """Start the timer."""
    global stopwatchIsRunning
    
    stopwatchIsRunning = True
    
def stop_button_handler():
    """Stop the timer."""
    global stopwatchIsRunning
    global successfulAttempts
    global totalAttempts
    
    if (stopwatchIsRunning):
        stopwatchIsRunning = False
        
        if ((currentTime % 10) == 0):
            successfulAttempts += 1
        totalAttempts += 1
        
def reset_button_handler():
    """Reset the timer."""
    global currentTime
    global stopwatchIsRunning
    global successfulAttempts
    global totalAttempts
    
    stopwatchIsRunning = False
    
    currentTime = 0
    successfulAttempts = 0
    totalAttempts = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global stopwatchIsRunning
    global currentTime
    
    if stopwatchIsRunning:
        currentTime += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(str(successfulAttempts) + "/" + str(totalAttempts), [430, 20], 20, "Red")
    canvas.draw_text(format(currentTime), [250, 250], 50, "Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", 500, 500)

# register event handlers
frame.add_button("Start", start_button_handler)
frame.add_button("Stop", stop_button_handler)
frame.add_button("Reset", reset_button_handler)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()
timer.start()

# Please remember to review the grading rubric
