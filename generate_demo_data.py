"""
Veterans India AI Assistant - Demo Data Generator
===============================================
Generates realistic demo data for testing the admin dashboard
with sample users, subscriptions, and usage patterns.

© 2025 Veterans India Team. All rights reserved.
"""

import sqlite3
import random
import datetime
from faker import Faker
import json

fake = Faker('en_IN')  # Indian locale for realistic data

class DemoDataGenerator:
    def __init__(self, db_path="veterans_admin.db"):
        self.db_path = db_path
    
    def generate_demo_users(self, count=50):
        """Generate demo users with realistic data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get plan IDs
        cursor.execute("SELECT id FROM plans")
        plan_ids = [row[0] for row in cursor.fetchall()]
        
        demo_users = []
        statuses = ['active', 'expired', 'suspended']
        
        for i in range(count):
            # Generate user data
            username = fake.user_name() + str(random.randint(100, 999))
            email = fake.email()
            password_hash = "demo_hash_" + str(i)  # Demo password hash
            
            # Random plan assignment
            plan_id = random.choice(plan_ids) if plan_ids else None
            
            # Device limits based on plan
            if plan_id == 1:  # Basic
                device_limit = 3
            elif plan_id == 2:  # Standard
                device_limit = 10
            elif plan_id == 3:  # Premium
                device_limit = 25
            else:  # Enterprise
                device_limit = 100
            
            current_devices = random.randint(1, min(device_limit, 15))
            
            # Dealer codes for some users
            dealer_code = f"DLR{random.randint(1000, 9999)}" if random.random() > 0.3 else None
            
            # Subscription status
            subscription_status = random.choices(
                statuses, 
                weights=[70, 20, 10]  # 70% active, 20% expired, 10% suspended
            )[0]
            
            # Generate dates
            start_date = fake.date_between(start_date='-1y', end_date='today')
            
            if subscription_status == 'active':
                # Active users have future end dates
                end_date = fake.date_between(start_date='today', end_date='+6m')
            elif subscription_status == 'expired':
                # Expired users have past end dates
                end_date = fake.date_between(start_date=start_date, end_date='today')
            else:
                # Suspended users might have various dates
                end_date = fake.date_between(start_date=start_date, end_date='+3m')
            
            user_data = (
                username, email, password_hash, plan_id, device_limit, current_devices,
                dealer_code, subscription_status, start_date.isoformat(), end_date.isoformat()
            )
            
            demo_users.append(user_data)
        
        # Insert users
        cursor.executemany('''
        INSERT INTO users (
            username, email, password_hash, plan_id, device_limit, current_devices,
            dealer_code, subscription_status, subscription_start, subscription_end
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', demo_users)
        
        conn.commit()
        conn.close()
        
        print(f"Generated {count} demo users")
    
    def generate_demo_devices(self, max_per_user=5):
        """Generate device data for users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all user IDs
        cursor.execute("SELECT id, current_devices FROM users")
        users = cursor.fetchall()
        
        device_types = ['Mobile', 'Desktop', 'Tablet', 'Laptop']
        device_names = {
            'Mobile': ['iPhone 13', 'Samsung Galaxy S21', 'OnePlus 9', 'Xiaomi Mi 11'],
            'Desktop': ['Windows PC', 'Mac Studio', 'Linux Workstation', 'Gaming PC'],
            'Tablet': ['iPad Pro', 'Samsung Tab S7', 'Surface Pro', 'Lenovo Tab'],
            'Laptop': ['MacBook Pro', 'Dell XPS', 'HP Spectre', 'Lenovo ThinkPad']
        }
        
        demo_devices = []
        
        for user_id, device_count in users:
            for i in range(min(device_count, max_per_user)):
                device_type = random.choice(device_types)
                device_name = random.choice(device_names[device_type])
                device_id = f"DEV_{user_id}_{i}_{random.randint(10000, 99999)}"
                
                # Random last active time
                last_active = fake.date_time_between(start_date='-30d', end_date='now')
                is_active = random.random() > 0.2  # 80% of devices are active
                
                demo_devices.append((
                    user_id, device_name, device_type, device_id, 
                    last_active.isoformat(), is_active
                ))
        
        cursor.executemany('''
        INSERT INTO user_devices (
            user_id, device_name, device_type, device_id, last_active, is_active
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', demo_devices)
        
        conn.commit()
        conn.close()
        
        print(f"Generated {len(demo_devices)} demo devices")
    
    def generate_subscription_history(self):
        """Generate subscription history for users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get users with plans
        cursor.execute('''
        SELECT u.id, u.plan_id, u.subscription_start 
        FROM users u 
        WHERE u.plan_id IS NOT NULL
        ''')
        users = cursor.fetchall()
        
        actions = ['created', 'renewed', 'upgraded', 'downgraded']
        demo_history = []
        
        for user_id, current_plan_id, start_date in users:
            # Initial subscription creation
            start_dt = datetime.datetime.fromisoformat(start_date)
            
            demo_history.append((
                user_id, current_plan_id, 'created', None,
                start_date, start_date, random.uniform(99, 1999)
            ))
            
            # Generate some historical changes
            history_count = random.randint(0, 3)
            for i in range(history_count):
                action = random.choice(actions[1:])  # Skip 'created'
                action_date = fake.date_between(
                    start_date=start_dt.date(), 
                    end_date='today'
                ).isoformat()
                
                demo_history.append((
                    user_id, current_plan_id, action, current_plan_id,
                    action_date, action_date, random.uniform(99, 1999)
                ))
        
        cursor.executemany('''
        INSERT INTO subscription_history (
            user_id, plan_id, action, previous_plan_id, start_date, end_date, amount
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', demo_history)
        
        conn.commit()
        conn.close()
        
        print(f"Generated {len(demo_history)} subscription history records")
    
    def generate_admin_logs(self, count=100):
        """Generate admin activity logs"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get admin and user IDs
        cursor.execute("SELECT id FROM admins")
        admin_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM users LIMIT 20")
        user_ids = [row[0] for row in cursor.fetchall()]
        
        actions = [
            'user_created', 'user_updated', 'user_deleted', 'user_impersonated',
            'plan_created', 'plan_updated', 'subscription_renewed', 'login'
        ]
        
        target_types = ['user', 'plan', 'subscription', 'system']
        
        demo_logs = []
        
        for i in range(count):
            admin_id = random.choice(admin_ids) if admin_ids else 1
            action = random.choice(actions)
            target_type = random.choice(target_types)
            target_id = random.choice(user_ids) if user_ids else 1
            
            details = json.dumps({
                'action': action,
                'timestamp': fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
                'ip_address': fake.ipv4(),
                'user_agent': fake.user_agent()
            })
            
            demo_logs.append((admin_id, action, target_type, target_id, details))
        
        cursor.executemany('''
        INSERT INTO admin_logs (admin_id, action, target_type, target_id, details)
        VALUES (?, ?, ?, ?, ?)
        ''', demo_logs)
        
        conn.commit()
        conn.close()
        
        print(f"Generated {count} admin log entries")
    
    def generate_all_demo_data(self):
        """Generate complete demo dataset"""
        print("Generating comprehensive demo data...")
        
        self.generate_demo_users(50)
        self.generate_demo_devices()
        self.generate_subscription_history()
        self.generate_admin_logs(100)
        
        print("Demo data generation complete!")
        print("\nDemo data includes:")
        print("- 50 realistic users with Indian names and data")
        print("- Varied subscription plans and statuses")
        print("- Device registrations for each user")
        print("- Subscription history and changes")
        print("- Admin activity logs")
        print("\nYou can now test the admin dashboard with realistic data!")

def main():
    """Generate demo data for testing"""
    generator = DemoDataGenerator()
    
    # Check if demo data already exists
    conn = sqlite3.connect("veterans_admin.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    conn.close()
    
    if user_count > 5:  # Already has some data
        print(f"Database already contains {user_count} users.")
        choice = input("Do you want to add more demo data? (y/n): ")
        if choice.lower() != 'y':
            return
    
    generator.generate_all_demo_data()

if __name__ == "__main__":
    main()
