import numpy as n
from itertools import combinations as comb

inp = open("Extracted.txt","r")
out = open("Output.csv","a")

#counts the total number of lines in the journal file
nlines = 0
for line in inp:
	nlines = nlines+1

inp.close()


arr = []
y = []

arrtest = []
ytest = []

infile = open("Extracted.txt","r")
line=1
#Extracts all the parameter values and stores in an arrayIndexError: too many indices for array

for a in infile:
	isjr = a.find(";")
	ihind = a.find(";",isjr+1)
	itd = a.find(";",ihind+1)
	itd3 = a.find(";",itd+1)
	itr = a.find(";",itd3+1)
	itc = a.find(";",itr+1)
	icd = a.find(";",itc+1)
	icpd = a.find(";",icd+1)
	irpd = a.find(";",icpd+1)
	iimpact = a.find(";",irpd+1)
	sjr = a[isjr+1:ihind].replace(",","")
	if ( sjr!=""  and sjr[0]=='0' ): sjr  = float(sjr[1:])
	elif(sjr==""): continue 
	hind = float(a[ihind+1:itd])
	td = float(a[itd+1:itd3])
	td3 = float(a[itd3+1:itr])
	tr = float(a[itr+1:itc])
	tc = float(a[itc+1:icd])
	cd = float(a[icd+1:icpd])
	cpd = float(a[icpd+1:irpd].replace(",","."))
	rpd = float(a[irpd+1:iimpact].replace(",","."))
	impact = float(a[iimpact+1:])
	if line<=0.8*nlines:
		arr.append([sjr,hind,td,td3,tr,tc,cd,cpd,rpd])
		y.append([impact])
	else:
		arrtest.append([sjr,hind,td,td3,tr,tc,cd,cpd,rpd])
		ytest.append([impact])
	line=line+1


ARRAY = n.array(arr,dtype=float) #Entire array with values of all parameters
ARRTEST = n.array(arrtest,dtype=float)
#print(ARRAY)

Y = n.array(y) #Values of actual Impact Factors
YTEST = n.array(ytest)
#Combinations of parameters to regress with
lcol = []

for num in range(2,10):
	lcol=lcol+list(comb([0,1,2,3,4,5,6,7,8],num))

#Finding the errors for different combinations
for col in lcol:
	A = n.array(ARRAY[:,col])
	Atest = n.array(ARRTEST[:,col])

	AT = A.transpose()
	B = AT@A
	Bin = n.linalg.inv(B)
	#C = A@Bin
	P = Bin@AT
	x = P@Y

	Err = n.subtract(YTEST,Atest@x) #Array with all errors

	mabs=0
	msq=0

	for i in range(0,int(nlines*0.2)):
		mabs = mabs + abs(Err[i,0])
		msq = msq + (Err[i,0]*Err[i,0])
	
	mabs = mabs/int(nlines*0.2) #mean absolute error
	msq = msq/int(nlines*0.2) #mean square error

	combo = []

	for no in col:
		if no==0: combo.append("SJR")
		elif no==1: combo.append("H Index")
		elif no==2: combo.append("Total Docs.")
		elif no==3: combo.append("Total Docs(3years)")
		elif no==4: combo.append("Total Refs.")
		elif no==5: combo.append("Total Cites")
		elif no==6: combo.append("Citable Docs.")
		elif no==7: combo.append("Cites/Docs.")
		elif no==8: combo.append("Ref./Docs.")

	lin = str(combo)+";"+str(mabs)+";"+str(msq)+"\n"
	out.write(lin) #appended to final output file


infile.close()
out.close()

