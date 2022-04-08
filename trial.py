from datetime import datetime as dt 

t1= dt.strptime("2022-03-18", "%Y-%m-%d")
t2= dt.strptime("2022-04-07", "%Y-%m-%d")
#print(abs(t2 - t1).days)
#print(dt.now().strftime("%Y-%m-%d"))
print(("2022-03-18" - dt.now().strftime("%Y-%m-%d")).days)