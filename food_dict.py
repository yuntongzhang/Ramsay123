# -*- coding: utf-8 -*-
import random 

def check(info):#take in list
	
	rownum=0
	output = []
	alterput = []
	alterput2=[]
	for row in reader:
	# Save header row.
		if rownum ==0:
			header = row
		else:
			colnum = 0
			counter = 0
			for col in row[2:6]:
				if float(info[colnum]) <= float(col):
					counter+=1
					#print colnum
				colnum+=1
				if float(info[colnum]) >= float(col):
					counter+=1

				if counter == 8:
					#print row[:5]
					output.append(row[:6])
				elif len(output)==0:
					if counter == 7:
						alterput.append(row[:6])
					elif counter == 6:
						alterput2.append(row[:6])
				colnum+=1
			 
		rownum += 1
	if len(output)>0:
		return output
	elif len(alterput)>0:
		print("This is one of the best alternatives we can find")
		return alterput
	elif len(alterput)>0:
		print("This is one of the best alternatives we can find")
		return alterput2
	else:
		print("Oops")
		return 0