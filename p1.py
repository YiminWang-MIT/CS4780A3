w0=[0,0]
b=0
trainingSet=[
    # y,xx,xy,b
    [ 1,1,5,1],
    [ 1,3,5,1],
    [-1,4,7,1],
    [-1,4,9,1],
    [-1,6,9,1],
    [ 1,3,1,1]]
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
  if (v[0]*(dot(w0,newV)+b)<=0):
    #made mistake
    w0=sum(w0,[v[0]*v[1],v[0]*v[2]])
    b=b+v[0];
print w0
print b

