from datetime import timedelta, date
#today= dt.strptime(dt.now().strftime("%Y-%m-%d"), "%Y-%m-%d")

#t1= dt.strptime(dt.today().strftime("%Y/%m/%d"), ("%Y/%m/%d"))
#t2= t1 - timedelta(10)

T1= date.today()
T2= T1 - timedelta(10)

print(T1)
print(T2)