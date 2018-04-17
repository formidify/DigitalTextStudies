import csv
import pandas

def main():
	myfile = open("metoo_d3.csv",'w')
	writer = csv.writer(myfile)
	writer.writerow(["topic", "word", "count"])

	file = open("metoo-count.txt")

	for line in file:
		l = line.split()
		word = l[1]
		for i in range(len(l)-2):
			cur = [int(i) for i in l[i+2].split(":")]
			topic = cur[0]
			count = cur[1]
			writer.writerow([topic, word, count])
main()
