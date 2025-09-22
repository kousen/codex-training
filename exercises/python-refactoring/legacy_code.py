# Legacy calculator and data processor code - needs major refactoring!

def calc(x,y,op):
    if op=="add":
        return x+y
    elif op=="sub":
        return x-y
    elif op=="mul":
        return x*y
    elif op=="div":
        return x/y
    else:
        return None

class DataProcessor:
    def __init__(self):
        self.data = []

    def process_file(self, filename):
        f = open(filename, 'r')
        lines = f.readlines()
        for l in lines:
            parts = l.split(',')
            if len(parts) == 3:
                try:
                    self.data.append({
                        'name': parts[0],
                        'age': int(parts[1]),
                        'salary': float(parts[2])
                    })
                except:
                    pass
        f.close()

    def get_avg_salary(self):
        total = 0
        count = 0
        for d in self.data:
            total = total + d['salary']
            count = count + 1
        return total / count

    def find_person(self, name):
        for d in self.data:
            if d['name'] == name:
                return d
        return None

    def filter_by_age(self, min_age, max_age):
        result = []
        for d in self.data:
            if d['age'] >= min_age and d['age'] <= max_age:
                result.append(d)
        return result

    def sort_by_salary(self):
        # Bubble sort - inefficient!
        n = len(self.data)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data[j]['salary'] > self.data[j+1]['salary']:
                    temp = self.data[j]
                    self.data[j] = self.data[j+1]
                    self.data[j+1] = temp
        return self.data

# Global variables - bad practice!
global_cache = {}
counter = 0

def process_complex_data(input_data):
    global counter
    counter += 1

    # Magic numbers everywhere
    if len(input_data) < 5:
        return None

    result = []
    for item in input_data:
        # No validation
        value = item * 1.5 + 10
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        result.append(value)

    # Store in global cache - memory leak potential
    global_cache[counter] = result
    return result

class FileManager:
    def read_config(self, path):
        # No error handling
        file = open(path)
        config = {}
        for line in file:
            if '=' in line:
                key, val = line.split('=')
                config[key.strip()] = val.strip()
        # File never closed - resource leak!
        return config

    def write_data(self, path, data):
        # No error handling
        file = open(path, 'w')
        for item in data:
            file.write(str(item) + '\n')
        # File never closed - resource leak!

def convert_temperature(temp, from_unit, to_unit):
    # Long if-else chain - needs refactoring
    if from_unit == 'C' and to_unit == 'F':
        return temp * 9/5 + 32
    elif from_unit == 'F' and to_unit == 'C':
        return (temp - 32) * 5/9
    elif from_unit == 'C' and to_unit == 'K':
        return temp + 273.15
    elif from_unit == 'K' and to_unit == 'C':
        return temp - 273.15
    elif from_unit == 'F' and to_unit == 'K':
        return (temp - 32) * 5/9 + 273.15
    elif from_unit == 'K' and to_unit == 'F':
        return (temp - 273.15) * 9/5 + 32
    else:
        return temp

# Bad class design - does too many things
class SuperClass:
    def __init__(self):
        self.users = []
        self.products = []
        self.orders = []

    def add_user(self, name, email):
        self.users.append({'name': name, 'email': email})

    def add_product(self, name, price):
        self.products.append({'name': name, 'price': price})

    def create_order(self, user_name, product_name):
        user = None
        product = None
        for u in self.users:
            if u['name'] == user_name:
                user = u
                break
        for p in self.products:
            if p['name'] == product_name:
                product = p
                break
        if user and product:
            self.orders.append({
                'user': user,
                'product': product,
                'status': 'pending'
            })

    def calculate_total(self):
        total = 0
        for order in self.orders:
            total += order['product']['price']
        return total

    def send_email(self, user_name, message):
        # Fake email sending
        print(f"Sending email to {user_name}: {message}")

    def generate_report(self):
        # Mixed responsibilities
        report = "Sales Report\n"
        report += "=" * 20 + "\n"
        for order in self.orders:
            report += f"{order['user']['name']}: ${order['product']['price']}\n"
        report += "=" * 20 + "\n"
        report += f"Total: ${self.calculate_total()}\n"
        return report