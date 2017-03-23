import random

def roll_die(numbers, n):
    ranges={}
    for x in range(0, numbers):
        ranges[x]=(x*n,x*n+20)    
    
    r = random.randint(0, n*numbers)  
    
    for key, value in ranges.items():
        if value[0]<=r and value[1]>=r:
            return key
        

if __name__ == "__main__":
    for _ in range(0,100):
        print(roll_die(6,20))
