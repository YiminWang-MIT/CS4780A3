from math import *

trainl=[[[1,5],-1],[[3,5],-1],[[4,7],1],[[4,9],1],[[6,9],1],[[3,1],-1]]
temptrain=[[[1,5],-1],[[3,5],-1],[[4,7],1],[[4,9],1],[[6,9],1],[[3,1],-1]]

def dotp(x,y):
  if len(x)!=len(y): return -1
  sum=0;
  for i in range(len(x)):
    sum+=x[i]*y[i]
  return sum

print '-----Part A-----'
update=1
w=[0,0,0]
for ex in temptrain:
  ex[0].append(1)
while update:
  update=0
  for ex in temptrain:
    predict=(dotp(w,ex[0]))*ex[1]
    if predict<=0:
      for i in range(len(w)):
        w[i]+=ex[1]*ex[0][i]
      update=1
    
print w
print '-----Part C-----'
gamma=5**0.5/2
betal=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]
w=[0,0.0000001]
b=1
hp=[]
for beta in betal:
  update=1
  while update:
    update=0
    for ex in trainl:
      predict=(dotp(w,ex[0])+b)*ex[1]/(dotp(w,w)**0.5)
      if predict<beta*gamma:
        for i in range(len(w)):
          w[i]+=ex[1]*ex[0][i]
          b+=ex[1]
        update=1
  hp.append([w,b])  

print hp 
