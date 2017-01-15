import csv, os

class SalaryRow:
	def __init__(self, minsalary, maxsalary, count):
		self.minsalary = int(minsalary.replace(" ", "")) / 1000
		self.maxsalary = int(maxsalary.replace(" ", "")) / 1000
		self.avgsalary = (self.maxsalary + self.minsalary) / 2
		self.count = int(count.replace(" ", ""))
	def __str__(self):
		return "min {} max {} count {}".format(self.minsalary, self.maxsalary, self.count)
	def __repr__(self):
		return str(self)

def parse_monthly_csv(path):
	rows = []
	with open(path) as csvfile:
		csvreader = csv.reader(csvfile, delimiter=",")
		for csvrow in csvreader:
			row = SalaryRow(csvrow[0], csvrow[1], csvrow[4])
			rows.append(row)
	return rows

def parse_hourly_csv(path):
	pass

def read_data_files():
	private_service = parse_monthly_csv("private_service.csv")
	private_manual = parse_hourly_csv("private_manual_hourly.csv")
	public_landsting = parse_monthly_csv("public_landsting.csv")
	public_komun = parse_monthly_csv("public_komun.csv")
	public_stat = parse_monthly_csv("public_stat.csv")
	return { "private_service" : private_service,
			 "public_landsting" : public_landsting,
			 "public_komun" : public_komun,
			 "public_stat" : public_stat }

class PeopleRow():
	def __init__(self, min_year, max_year, men_count, women_count):
		self.min_year = int(min_year.replace(" ", ""))
		self.max_year = int(max_year.replace(" ", ""))
		self.men_count = int(men_count.replace(" ", ""))
		self.women_count = int(women_count.replace(" ", ""))
		self.total_count = self.women_count + self.men_count
	def __str__(self):
		return "{} - {}, women: {}, men {}".format(self.min_year, self.max_year, self.women_count, self.men_count)
	def __repr__(self):
		return str(self)

def read_people_file():
	with open("people_ages.csv", "r") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=",")
		rows = []
		for csvrow in csvreader:
			row = PeopleRow(csvrow[0], csvrow[1], csvrow[2], csvrow[3])
			rows.append(row)
		return rows

#levels, in thousands
BASIC_LEVEL = 7
MIMIMUM_SALARY = 20
CHILD_LEVEL = 0.75
PEOPLE_IN_SWEDEN = 9967274
OUT_OF_WORK = 0.074

def calc(salary_data, people_data):
	total_workers = 0
	total_salary = 0
	for key in salary_data:
		print "handling salaries for {}".format(key)
		rows = salary_data[key]
		key_workers = 0
		key_salary = 0
		for row in rows:
			if row.minsalary > 34: #too high salary, ignore
				continue
			else:
				new_workers = row.count
			if row.minsalary < MIMIMUM_SALARY: #too low salary, full rebate
				new_salary = (row.count * BASIC_LEVEL)
			else: #somewhere in the middle, some rebate
				diff = row.avgsalary - MIMIMUM_SALARY
				factor = diff * 0.5
				new_salary = (row.count * (BASIC_LEVEL - factor))
			key_salary += new_salary
			key_workers += new_workers
		total_workers += key_workers
		total_salary += key_salary

	for pd in people_data:
		if pd.max_year < 15: # child
			total_salary += pd.total_count * CHILD_LEVEL
		if pd.max_year > 16 or pd.min_year < 24: # 6.7% of people in 16-24 neither work nor study
			total_salary += (pd.total_count * 0.067) * BASIC_LEVEL #
		if pd.min_year > 65: # pension, assume full basic level
			total_salary += pd.total_count * BASIC_LEVEL

	total_salary += (PEOPLE_IN_SWEDEN * OUT_OF_WORK) * BASIC_LEVEL
	return int(total_salary)

def main():
	people_data = read_people_file()
	salary_data = read_data_files()
	result = calc(salary_data, people_data)
	print("Total cost: {}".format(result))

if __name__ == '__main__':
	main()