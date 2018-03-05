def main():
	with open("136598840398995_facebook_statuses.csv") as file:
		reader = csv.DictReader(file, delimiter = ',')
		a = 0
		for row in reader:
			line = row['status_message']
			name = str(a) + ".txt"
			txt_file = open(name,"w+")
			txt_file.write(line) 
			txt_file.close()
			a = a+1
main()