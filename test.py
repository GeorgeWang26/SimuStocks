import threading 
  
def update(): 
    print("GeeksforGeeks\n") 
  
timer = threading.Timer(5.0, update) 
timer.start() 
