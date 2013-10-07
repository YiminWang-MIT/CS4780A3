w0=[0,0]
b=1
trainingSet=[
    [ 1,1,5],
    [ 1,3,5],
    [-1,4,7],
    [-1,4,9],
    [-1,6,9],
    [ 1,3,1]]
print trainingSet

def dot(w, v):
  sum=0;
  print "dot"
  
  print w
  print v

  for i in range(len(w)):
    sum+=w[i]*v[i]
  print sum
  return sum

def sum(w, v):
    print "sum"
    print w
    print v

    for i in range(len(w)):
      w[i]=w[i]+v[i]
    return w

for v in trainingSet:
  newV=[v[1],v[2]]
  temp=dot(w0,newV)
  if (v[0]*(temp+b)<=0):
    #made mistake
    w0=sum(w0,[v[0]*v[1],v[0]*v[2]])


