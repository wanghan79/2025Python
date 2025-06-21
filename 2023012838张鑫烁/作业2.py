import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union


class RandomSampleGenerator:
    """A flexible random sample generator that creates data based on user-defined structures."""
    
    def __init__(self, seed=None):
        """Initialize the generator with an optional seed for reproducibility."""
        if seed:
            random.seed(seed)
    
    def generate_value(self, field_type: str, **kwargs) -> Any:
        """Generate a single value based on the specified type."""
        generators = {
            'int': self._generate_int,
            'float': self._generate_float,
            'string': self._generate_string,
            'bool': self._generate_bool,
            'date': self._generate_date,
            'choice': self._generate_choice,
            'name': self._generate_name,
            'email': self._generate_email,
            'phone': self._generate_phone,
            'id': self._generate_id
        }
        
        generator = generators.get(field_type, self._generate_string)
        return generator(**kwargs)
    
    def _generate_int(self, min_val=0, max_val=100, **kwargs):
        """Generate a random integer."""
        return random.randint(min_val, max_val)
    
    def _generate_float(self, min_val=0.0, max_val=100.0, decimals=2, **kwargs):
        """Generate a random float."""
        return round(random.uniform(min_val, max_val), decimals)
    
    def _generate_string(self, min_length=5, max_length=10, chars=None, **kwargs):
        """Generate a random string."""
        if chars is None:
            chars = string.ascii_letters + string.digits
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _generate_bool(self, true_probability=0.5, **kwargs):
        """Generate a random boolean."""
        return random.random() < true_probability
    
    def _generate_date(self, start_date=None, end_date=None, format='%Y-%m-%d', **kwargs):
        """Generate a random date."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)
        else:
            start_date = datetime.strptime(start_date, format)
        
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, format)
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        random_date = start_date + timedelta(days=random_days)
        
        return random_date.strftime(format)
    
    def _generate_choice(self, choices, **kwargs):
        """Generate a random choice from a list."""
        return random.choice(choices)
    
    def _generate_name(self, **kwargs):
        """Generate a random name."""
        first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank', 
                      'Grace', 'Henry', 'Iris', 'Jack', 'Kate', 'Leo',
                      'Maria', 'Nathan', 'Olivia', 'Peter', 'Quinn', 'Rachel']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 
                     'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_email(self, **kwargs):
        """Generate a random email address."""
        username = self._generate_string(min_length=5, max_length=10, chars=string.ascii_lowercase)
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'example.com', 'mail.com']
        return f"{username}@{random.choice(domains)}"
    
    def _generate_phone(self, format='XXX-XXX-XXXX', **kwargs):
        """Generate a random phone number."""
        return ''.join(str(random.randint(0, 9)) if c == 'X' else c for c in format)
    
    def _generate_id(self, prefix='ID', length=8, **kwargs):
        """Generate a random ID."""
        id_part = self._generate_string(min_length=length, max_length=length, 
                                       chars=string.ascii_uppercase + string.digits)
        return f"{prefix}{id_part}"
    
    def generate_sample(self, structure: Dict[str, Union[str, Dict]]) -> Dict[str, Any]:
        """Generate a single sample based on the provided structure."""
        sample = {}
        for field_name, field_spec in structure.items():
            if isinstance(field_spec, str):
                # Simple type specification
                sample[field_name] = self.generate_value(field_spec)
            elif isinstance(field_spec, dict):
                # Complex type with parameters
                field_type = field_spec.pop('type', 'string')
                sample[field_name] = self.generate_value(field_type, **field_spec)
                field_spec['type'] = field_type  # Restore the type
        return sample
    
    def generate_samples(self, count: int, structure: Dict[str, Union[str, Dict]]) -> List[Dict[str, Any]]:
        """Generate multiple samples based on the provided structure."""
        return [self.generate_sample(structure) for _ in range(count)]


# ============= Usage Examples =============

if __name__ == "__main__":
    # Create a generator instance
    generator = RandomSampleGenerator(seed=42)  # Use seed for reproducible results
    
    print("=" * 50)
    print("Example 1: Simple User Data")
    print("=" * 50)
    
    # Define the structure for user data
    user_structure = {
        'id': 'id',
        'name': 'name',
        'age': {'type': 'int', 'min_val': 18, 'max_val': 65},
        'email': 'email',
        'is_active': 'bool',
        'balance': {'type': 'float', 'min_val': 0, 'max_val': 10000, 'decimals': 2}
    }
    
    # Generate samples
    users = generator.generate_samples(3, user_structure)
    for i, user in enumerate(users, 1):
        print(f"User {i}: {user}")
    
    print("\n" + "=" * 50)
    print("Example 2: Product Data with Categories")
    print("=" * 50)
    
    # More complex structure
    product_structure = {
        'product_id': {'type': 'id', 'prefix': 'PROD', 'length': 6},
        'name': {'type': 'choice', 'choices': ['Laptop', 'Phone', 'Tablet', 'Monitor', 'Keyboard']},
        'category': {'type': 'choice', 'choices': ['Electronics', 'Computers', 'Accessories']},
        'price': {'type': 'float', 'min_val': 99.99, 'max_val': 2999.99, 'decimals': 2},
        'in_stock': {'type': 'bool', 'true_probability': 0.8},
        'quantity': {'type': 'int', 'min_val': 0, 'max_val': 100},
        'last_updated': {'type': 'date', 'start_date': '2024-01-01', 'end_date': '2024-12-31'}
    }
    
    products = generator.generate_samples(5, product_structure)
    for i, product in enumerate(products, 1):
        print(f"Product {i}: {product}")
    
    print("\n" + "=" * 50)
    print("Example 3: Custom Structure from User Input")
    print("=" * 50)
    
    # Function to create samples based on user input
    def create_custom_samples():
        # In real usage, these would come from user input
        count = 4
        custom_structure = {
            'transaction_id': {'type': 'id', 'prefix': 'TXN', 'length': 10},
            'customer_name': 'name',
            'amount': {'type': 'float', 'min_val': 10.0, 'max_val': 1000.0, 'decimals': 2},
            'status': {'type': 'choice', 'choices': ['pending', 'completed', 'failed', 'cancelled']},
            'timestamp': {'type': 'date', 'format': '%Y-%m-%d %H:%M:%S'}
        }
        
        samples = generator.generate_samples(count, custom_structure)
        return samples
    
    transactions = create_custom_samples()
    for i, transaction in enumerate(transactions, 1):
        print(f"Transaction {i}: {transaction}")
    
    print("\n" + "=" * 50)
    print("Example 4: Nested/Complex Data Structure")
    print("=" * 50)
    
    # Generate samples with nested data
    def generate_complex_sample():
        # First generate basic info
        basic_info = generator.generate_sample({
            'user_id': {'type': 'id', 'prefix': 'USR', 'length': 8},
            'username': {'type': 'string', 'min_length': 6, 'max_length': 12},
            'created_at': 'date'
        })
        
        # Then add nested data
        basic_info['profile'] = {
            'full_name': generator.generate_value('name'),
            'phone': generator.generate_value('phone'),
            'preferences': {
                'newsletter': generator.generate_value('bool'),
                'theme': generator.generate_value('choice', choices=['light', 'dark', 'auto'])
            }
        }
        
        return basic_info
    
    complex_samples = [generate_complex_sample() for _ in range(2)]
    for i, sample in enumerate(complex_samples, 1):
        print(f"Complex Sample {i}:")
        print(f"  Basic: {sample['user_id']}, {sample['username']}, {sample['created_at']}")
        print(f"  Profile: {sample['profile']}")
    
    print("\n" + "=" * 50)
    print("Available Field Types:")
    print("=" * 50)
    print("- 'int': Integer with min_val, max_val")
    print("- 'float': Float with min_val, max_val, decimals")
    print("- 'string': String with min_length, max_length, chars")
    print("- 'bool': Boolean with true_probability")
    print("- 'date': Date with start_date, end_date, format")
    print("- 'choice': Random choice from choices list")
    print("- 'name': Random full name")
    print("- 'email': Random email address")
    print("- 'phone': Phone number with format (X for digit)")
    print("- 'id': ID with prefix and length")