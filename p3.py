import sys
import os
from math import *

def trainGen(name,sneg):
  ifile=name
  ofile=name+"%d"%sneg
  with open(ifile) as f:
    i=0
    cout=file(ofile,"w")
    for line in f:
      if i==sneg: break
      pn=int(line.partition(' ')[0])
      if pn==-1:
        i+=1
      cout.write(line)
  cout.close()
  return ofile

def plot(name,clist,j):
  posf=name+"pos"
  negf=name+"neg"
  coutp=file(posf,"w")
  coutn=file(negf,"w")
  with open(name) as f:
    for line in f:
      sep=line.partition(' ')
      value=int(sep[0])
      sep=sep[2].partition(' ')
      x=float(sep[0].partition(':')[2])
      y=float(sep[2].partition(':')[2])
      if value==1:
        coutp.write("%f %f\n"%(x,y))
      else:
        coutn.write("%f %f\n"%(x,y))
  coutp.close()
  coutn.close()
  name=name+'j%.2f'%j

  gnucmd=file("gnup.cmd","w")
  gnucmd.write("set terminal png\n")
  gnucmd.write("set size square\n")
  gnucmd.write("set key default\n")
  gnucmd.write("set key bottom right\n")
  gnucmd.write("set xrange [0.0:1.0]\n")
  gnucmd.write("set yrange [0.0:1.0]\n")
  gnucmd.write("set grid xtics lt 0 lw 1 lc rgb \"#bbbbbb\"\n")
  gnucmd.write("set grid ytics lt 0 lw 1 lc rgb \"#bbbbbb\"\n")
  gnucmd.write("set out '%s.png'\n"%name)
  gnucmd.write("plot \'%s\' u 1:2 w points pt 1 lt 1 notitle, "%posf)
  for i in range(len(clist)):
    cl=clist[i][1]
    a=cl[0]/(-cl[1])
    b=cl[2]/(cl[1])
    c=clist[i][0]
    gnucmd.write("%f*x+%f w line lt %d title 'C=%d', "%(a,b,i+3,c))
  gnucmd.write("\'%s\' u 1:2 w points pt 6 lt 2 notitle\n"%negf)
  gnucmd.close()
  os.system("gnuplot gnup.cmd")
    
def readclf(clfname):
  with open(clfname) as f:
    i=0
    wx=0
    wy=0
    for line in f:
      i+=1
      if i==10: n=int(line.partition(' ')[0])
      if i==11: b=float(line.partition(' ')[0])
      if i>11:
        sep=line.partition(' ')
        value=float(sep[0])
        sep=sep[2].partition(' ')
        x=float(sep[0].partition(':')[2])
        y=float(sep[2].partition(':')[2].partition(' ')[0])
        wx+=x*value
        wy+=y*value
  return [wx,wy,b]

def svmplot(name,sneg,clist,jlist):
  train=trainGen(name,sneg)
  for j in jlist:
    classifier=[]
    for c in clist:
      cmd1="./svm_learn -c %d -j %f %s %dtmp%f.class > log "%(c,j,train,c,j)
      os.system(cmd1)
      clf=readclf('%dtmp%f.class'%(c,j))
      classifier.append([c,clf])
    plot(train,classifier,j)

def svm(name,sneg,clist,jlist):
  test=name+".test"
  train=name+".train"
  train=trainGen(train,sneg)
  summary=[]
  for j in jlist:
    for c in clist:
      plist=[]
      cmd1="./svm_learn -c %d -j %f %s %dtmp%f.class > log "%(c,j,train,c,j)
      os.system(cmd1)
      cmd2="./svm_classify %s %dtmp%f.class %dboxes%f.result > log "%(test,c,j,c,j)
      os.system(cmd2)
      f=file(test,"r")
      for line in f:
        plist.append([int(line.partition(' ')[0])])
      f=file("%dboxes%f.result"%(c,j),"r")
      ln=0
      for line in f:
        plist[ln].append(float(line))
        ln+=1
      cor=0
      fneg=0
      fpos=0
      for en in plist:
        if (en[0]>0) and (en[1]<0):
          fneg+=1
        elif (en[0]<0) and (en[1]>0):
          fpos+=1
        else: cor+=1
      summary.append([c,j,cor,fpos,fneg])
  return summary

#----partB----
sl={10,50,100}
cl={1,1000}
jl={1}
for s in sl:
  svmplot("boxes.train",s,cl,jl)

#----partE----
sl={10}
cl={1}
jl={0.5,0.1,0.05}
for s in sl:
  svmplot("boxes.train",s,cl,jl)

#----partF----
sl={10}
cl={1}
jl={0.5,0.1,0.05}
for s in sl:
  print "S=%d"%s
  print svm("boxes",s,cl,jl)
  print "" 
