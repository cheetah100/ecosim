import model
import random
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

def get_best_price(industry, min_price):
	chosen_company = None
	best_price = 1000000	
	industry_companies = industries[industry]
	for company in industry_companies:
		if company.price < best_price and company.price > min_price and company.stock > 0:
			chosen_company = company
			best_price = company.price
	return chosen_company

def buy(person, company):

	if person.alive:
		price = company.price * person.consumption
		company.demand = company.demand + person.consumption
		if person.balance > price and company.stock >= person.consumption:
			person.balance = person.balance - price
			company.balance = company.balance + price
			company.stock = company.stock - person.consumption
			if person.pain > -20:
				person.pain = person.pain - 1		
		else :
			person.pain = person.pain + 1
	
def find_employee(max_salary):
	for person in people:
		if person.employer == None and person.salary < max_salary and person.alive :
			return person
	return None

def scale(l, max_value):
	
	list_max = 0
	for v in l:
		if v > list_max:
			list_max = v

	divisor = list_max / max_value

	r = []
	for v in l:
		r.append(int(v / divisor))

	return r



# SET UP COMPANIES
companies = []
industries = {'food':[],'housing':[],'power':[],'transport':[]}
company_wealth = []
company_demand = []
company_production = []
company_costs = []
company_revenue = []
company_stock = []

for industry in industries:
	for x in range(1,4):
		company = model.Company()
		company.industry = industry
		company.balance = 1000000
		company.stock = 1000
		company.price = 10 + random.randint(1,10)
		company.max_salary = 40 + random.randint(1,40)
		companies.append(company)
		industries[industry].append(company)

# SET UP PEOPLE
people = []
people_wealth = []
people_alive = []

for x in range(1,100):
	person = model.Person()
	person.balance = 1000
	person.consumption = 1
	person.productivity = 1 + random.randint(1,3)
	person.salary = 10 + random.randint(1,90)
	person.min_price = 10 + random.randint(1,10)	
	people.append(person)

# ITERATE EACH WEEK FOR A YEAR
for week in range(1,500):

	print('Week', week)

	# ITERATE PEOPLE - PURCHASE GOOD / SERVICES
	w = 0
	a = 0
	for person in people:
		if person.alive:
			w = w + person.balance
			a = a + 1
			for industry in industries:
				company = get_best_price(industry, person.min_price)
				if company != None:
					buy(person, company)
				else :
					person.pain = person.pain + 1

			# Too Much Adversity and they Die
			if person.pain > 20:
				person.alive = False

	people_wealth.append(w)
	people_alive.append(a)
	
	# ITERATE COMPANIES - PRODUCE GOODS / PAY STAFF

	d = 0
	p = 0
	s = 0
	for company in companies:
		print('Company ', company.balance)

		d = d + company.demand
		s = s + company.stock

		# Produce New Goods / Services, Pay Living Staff
		company.production = 0
		company.cost = 0
		for employee in company.employees:
			if employee.alive:
				company.production = company.production + employee.productivity
				company.cost = company.cost + employee.salary
				employee.balance = employee.balance + employee.salary
		company.balance = company.balance - company.cost
		company.stock = company.stock + company.production

		p = p + company.production

		# New Employment (does production meet demand?)

		print( 'Demand', company.demand, 'Production', company.production)

		x = company.production - company.demand
		if x < 0:
			employee = find_employee(company.max_salary)
			if employee != None:
				employee.employer = company
				company.employees.append(employee)
				print('New Hire', employee.salary)
			else:
				print('No Hire Found',  company.max_salary, x)
				company.max_salary = company.max_salary + 5
		else:
			if len( company.employees ) > 0:
				employee = company.employees[0]
				employee.employer = None
				company.employees = company.employees[1:]
				print('Employee Fired', employee.salary)
			
			
		if company.demand == 0 and company.price > 5:
			company.price = company.price - 1
			print("No Demand, reducing price",company.price)
				
		if company.cost > 0:
			unit_cost = company.production / company.cost
			if company.price < unit_cost:
				company.price = int(unit_cost) + 1
				print("Not covering costs, increasing price", company.price)
			

		# Reset Demand
		company.demand = 0

	company_demand.append(d)
	company_production.append(p)
	company_stock.append(s)


print('Final Results - People')
for person in people:
	print(person.productivity, person.min_price, person.balance, person.pain)

print('Final Results - Companies')
for company in companies:
	print(company.price, company.balance, company.stock, company.demand)


# Plot Results

# xref = range(0,len(people_alive)*20,20)

xref = range(0,len(people_alive),1)

y_pos = np.arange(len(people_alive))
plt.plot(xref, scale(people_wealth,100), label='Wealth' )
plt.plot(xref, scale(people_alive,100), label='Population' )
plt.plot(xref, scale(company_demand,100), label='Demand' )
plt.plot(xref, scale(company_production,100), label='Production' )
plt.plot(xref, scale(company_stock,100), label='Stock' )
# plt.xticks(xref, y_pos)
# plt.ylabel('Dollars')
plt.xlabel('Week')
plt.title('Economic Simulation Results')
 
plt.show()

