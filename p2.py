import sys
import os
from math import *
import random

#generating training data for all four class
def partition(s,k):
  dl=[]
  inputfile=s+".train"
  with open(inputfile) as f:
    for line in f:
      dl.append(line)
  lnew=list(dl)
  num=len(dl)/k
  ssl=[]
  if k==1:
    os.system("cp %s %s0.train"%(inputfile,s))
    os.system("cp %s.test %s0.test"%(s,s))
  else:
    for i in range(k):
      ltmp=[]
      for j in range(num):
        index=int(floor(random.uniform(0,len(lnew))))
        ltmp.append(lnew[index])
        del lnew[index]
      f1name=s+"%d.train"%i
      f2name=s+"%d.test"%i
      cout=file(f1name,"w")
      ltrain=lnew+ssl
      for line in ltrain:
        cout.write(line)
      cout.close()
      cout=file(f2name,"w")
      for line in ltmp:
        cout.write(line)
      cout.close()
      ssl=ssl+ltmp

def minput(s,k,cl):
  for j in range(k):
    for i in range(1,cl+1):
      iname=s+'%d.train'%j
      oname=s+"%d.train%d"%(j,i)
      cout=file(oname,"w")
      with open(iname) as f:
        for line in f:
          sep=line.partition(' ')
          c=int(sep[0])
          if c==i:
            cout.write("%d %s"%(1,sep[2]))
          else:
            cout.write("%d %s"%(-1,sep[2]))
      cout.close()

def svm(s,fold,cl,c):
  traintmp=0
  testtmp=0
  for j in range(fold):
    train=[]
    fname=s+"%d.train"%j
    f=file(fname,"r")
    for line in f:
      sep=line.partition(' ')
      train.append([int(sep[0])])
    f.close()
    test=[]
    fname=s+"%d.test"%j
    f=file(fname,"r")
    for line in f:
      sep=line.partition(' ')
      test.append([int(sep[0])])
    f.close()
    for i in range(1,cl+1):
      cmd1="./svm_learn -c %f %s%d.train%d %s%d.class%d > log "%(c,s,j,i,s,j,i)
      os.system(cmd1)
      cmd3="./svm_classify %s%d.train %s%d.class%d %s%d.0result%d > log"%(s,j,s,j,i,s,j,i)
      os.system(cmd3)
      fname="%s%d.0result%d"%(s,j,i)
      f=file(fname,"r")
      ln=0
      for line in f:
        train[ln].append(float(line))
        ln+=1
      f.close()
      cmd2="./svm_classify %s%d.test %s%d.class%d %s%d.1result%d >log"%(s,j,s,j,i,s,j,i)
      os.system(cmd2)
      fname="%s%d.1result%d"%(s,j,i)
      f=file(fname,"r")
      ln=0
      for line in f:
        test[ln].append(float(line))
        ln+=1
      f.close()
    cor=0
    tot=0
    for news in train:
      tot+=1
      m=-100
      pos=0
      for i in range(1,cl+1):
        if news[i]>m:
          m=news[i]
          pos=i
      if pos==news[0]: cor+=1
    traintmp+=(float(cor)/float(tot))
    cor=0
    tot=0
    for news in test:
      tot+=1
      m=-100
      pos=0
      for i in range(1,5):
        if news[i]>m:
          m=news[i]
          pos=i
      if pos==news[0]: cor+=1
    testtmp+=(float(cor)/float(tot))
  return [traintmp/fold,testtmp/fold]

def normalize(s):
  s1="%sN"%s
  extl=[".train",".test"]
  for ext in extl:
    sout=s1+ext
    cout=file(sout,"w")
    sin=s+ext
    with open(sin) as f:
      for line in f:
        cl=0
        ft=[]
        sep=line.partition(' ')
        line=sep[2]
        cl=sep[0]
        while line.find(':')>=0:
          sep=line.partition(':')
          index=int(sep[0])
          line=sep[-1]
          sep=line.partition(' ')
          mag=float(sep[0])
          ft.append([index,mag])
          line=sep[-1]
        length=sum([fe[1]**2 for fe in ft])**0.5
        cout.write(cl)
        for fe in ft:
          st=" %d:%f"%(fe[0],fe[1]/length)
          cout.write(st)
        cout.write("\n")
    cout.close()
  return s1

#----part A----
print "\n----Part A----"
def partA(s):
  clist=[0.001,0.01,0.1,0.5,1.0,2.0,5.0,10.0,100.0]
  testc=[]
  trainc=[]
  partition(s,5)
  minput(s,5,4)
  for c in clist:
    #generate classifier for each group
    a=svm(s,5,4,c)
    testc.append(a[1])
    trainc.append(a[0])
  print trainc
  print testc
  cbest=0
  maxacc=0
  for i in range(len(testc)):
    if testc[i]>maxacc: 
      cbest=clist[i]
      maxacc=testc[i]
  return cbest
cb=partA("groups2")
 
#----Part B----
def partB(s,c):
  testc=[]
  trainc=[]
  print "c=%f"%c
  partition(s,1)
  minput(s,1,4)
  a=svm(s,1,4,c)
  print a[0]
  print a[1]

print "\n----Part B----"
partB("groups2",cb)

#----Part C----
s1=normalize("groups2")
print "\n----Part C----"
cb=partA(s1)
partB(s1,cb)
