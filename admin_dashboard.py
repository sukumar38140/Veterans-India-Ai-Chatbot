"""
Veterans India AI Assistant - Admin Dashboard System
===================================================
Comprehensive admin management system with user management, 
subscription control, and impersonation features.

© 2025 Veterans India Team. All rights reserved.
"""

import streamlit as st
import sqlite3
import pandas as pd
import hashlib
import datetime
from typing import Optional, Dict, List
import uuid
import json

# Database setup and management
class DatabaseManager:
    def __init__(self, db_path="veterans_admin.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Admin table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
        ''')
        
        # Plans table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_name TEXT UNIQUE NOT NULL,
            device_limit INTEGER NOT NULL,
            price REAL NOT NULL,
            duration_days INTEGER NOT NULL,
            features TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan_id INTEGER,
            device_limit INTEGER DEFAULT 3,
            current_devices INTEGER DEFAULT 0,
            dealer_code TEXT,
            subscription_status TEXT DEFAULT 'active',
            subscription_start DATE,
            subscription_end DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        )
        ''')
        
        # Sessions table for impersonation
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            impersonated_user_id INTEGER,
            session_token TEXT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (admin_id) REFERENCES admins (id),
            FOREIGN KEY (impersonated_user_id) REFERENCES users (id)
        )
        ''')
        
        # Insert default admin if not exists
        cursor.execute("SELECT COUNT(*) FROM admins")
        if cursor.fetchone()[0] == 0:
            admin_password = self.hash_password("admin123")
            cursor.execute('''
            INSERT INTO admins (username, password_hash, email)
            VALUES (?, ?, ?)
            ''', ("admin", admin_password, "admin@veteransindia.org"))
        
        # Insert default plans if not exists
        cursor.execute("SELECT COUNT(*) FROM plans")
        if cursor.fetchone()[0] == 0:
            default_plans = [
                ("Basic", 3, 99.0, 30, json.dumps(["Chat Support", "Basic AI Features"]), 1),
                ("Standard", 10, 299.0, 90, json.dumps(["Chat Support", "Advanced AI", "Web Search"]), 1),
                ("Premium", 25, 799.0, 365, json.dumps(["All Features", "Priority Support", "Custom Training"]), 1),
                ("Enterprise", 100, 1999.0, 365, json.dumps(["Unlimited Features", "24/7 Support", "Custom Integration"]), 1)
            ]
            cursor.executemany('''
            INSERT INTO plans (plan_name, device_limit, price, duration_days, features, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', default_plans)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_admin(self, username: str, password: str) -> Optional[Dict]:
        """Verify admin credentials"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        cursor.execute('''
        SELECT id, username, email FROM admins 
        WHERE username = ? AND password_hash = ?
        ''', (username, password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "id": result[0],
                "username": result[1],
                "email": result[2]
            }
        return None
    
    def get_all_users(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get all users with pagination"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT u.id, u.username, u.email, u.device_limit, u.current_devices,
               u.dealer_code, u.subscription_status, u.subscription_end,
               p.plan_name
        FROM users u
        LEFT JOIN plans p ON u.plan_id = p.id
        ORDER BY u.created_at DESC
        LIMIT ? OFFSET ?
        ''', (limit, offset))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "device_limit": row[3],
                "current_devices": row[4],
                "dealer_code": row[5],
                "subscription_status": row[6],
                "subscription_end": row[7],
                "plan_name": row[8] or "No Plan"
            })
        
        conn.close()
        return users
    
    def get_user_count(self) -> int:
        """Get total user count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user details by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT u.*, p.plan_name, p.features
        FROM users u
        LEFT JOIN plans p ON u.plan_id = p.id
        WHERE u.id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "password_hash": row[3],
                "plan_id": row[4],
                "device_limit": row[5],
                "current_devices": row[6],
                "dealer_code": row[7],
                "subscription_status": row[8],
                "subscription_start": row[9],
                "subscription_end": row[10],
                "created_at": row[11],
                "updated_at": row[12],
                "plan_name": row[13] or "No Plan",
                "plan_features": row[14]
            }
        return None
    
    def update_user(self, user_id: int, user_data: Dict) -> bool:
        """Update user information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Build dynamic update query
            fields = []
            values = []
            
            for key, value in user_data.items():
                if key != 'id':
                    fields.append(f"{key} = ?")
                    values.append(value)
            
            if fields:
                fields.append("updated_at = CURRENT_TIMESTAMP")
                values.append(user_id)
                
                query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def get_all_plans(self) -> List[Dict]:
        """Get all plans"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, plan_name, device_limit, price, duration_days, features, is_active
        FROM plans
        ORDER BY price ASC
        ''')
        
        plans = []
        for row in cursor.fetchall():
            plans.append({
                "id": row[0],
                "plan_name": row[1],
                "device_limit": row[2],
                "price": row[3],
                "duration_days": row[4],
                "features": json.loads(row[5]) if row[5] else [],
                "is_active": bool(row[6])
            })
        
        conn.close()
        return plans
    
    def create_impersonation_session(self, admin_id: int, user_id: int) -> str:
        """Create impersonation session"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        session_token = str(uuid.uuid4())
        
        cursor.execute('''
        INSERT INTO admin_sessions (admin_id, impersonated_user_id, session_token)
        VALUES (?, ?, ?)
        ''', (admin_id, user_id, session_token))
        
        conn.commit()
        conn.close()
        return session_token

# Session management
class SessionManager:
    @staticmethod
    def init_session():
        """Initialize session state"""
        if 'admin_logged_in' not in st.session_state:
            st.session_state.admin_logged_in = False
        if 'admin_user' not in st.session_state:
            st.session_state.admin_user = None
        if 'impersonated_user' not in st.session_state:
            st.session_state.impersonated_user = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'login'
    
    @staticmethod
    def login_admin(admin_data):
        """Login admin"""
        st.session_state.admin_logged_in = True
        st.session_state.admin_user = admin_data
        st.session_state.current_page = 'dashboard'
    
    @staticmethod
    def logout_admin():
        """Logout admin"""
        st.session_state.admin_logged_in = False
        st.session_state.admin_user = None
        st.session_state.impersonated_user = None
        st.session_state.current_page = 'login'
    
    @staticmethod
    def impersonate_user(user_data):
        """Start user impersonation"""
        st.session_state.impersonated_user = user_data
        st.session_state.current_page = 'user_dashboard'
    
    @staticmethod
    def end_impersonation():
        """End user impersonation"""
        st.session_state.impersonated_user = None
        st.session_state.current_page = 'dashboard'

# UI Components
class AdminUI:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def render_login_page(self):
        """Render admin login page"""
        st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 style='color: #ff6600; margin-bottom: 2rem;'>🇮🇳 Veterans India Admin Dashboard</h1>
            <div style='background: linear-gradient(135deg, #ff6600, #138808, #000080); 
                        height: 4px; width: 100%; margin-bottom: 2rem;'></div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### 🔐 Administrator Login")
            
            with st.form("admin_login"):
                username = st.text_input("Username", placeholder="Enter admin username")
                password = st.text_input("Password", type="password", placeholder="Enter admin password")
                login_button = st.form_submit_button("Login", use_container_width=True)
                
                if login_button:
                    if username and password:
                        admin_data = self.db.verify_admin(username, password)
                        if admin_data:
                            SessionManager.login_admin(admin_data)
                            st.success("Login successful! Redirecting...")
                            st.rerun()
                        else:
                            st.error("Invalid username or password")
                    else:
                        st.error("Please enter both username and password")
            
            st.markdown("---")
            st.info("**Default Admin Credentials:**\n\nUsername: `admin`\nPassword: `admin123`")
    
    def render_sidebar(self):
        """Render admin sidebar navigation"""
        with st.sidebar:
            st.markdown("### 🇮🇳 Admin Dashboard")
            st.markdown(f"**Welcome:** {st.session_state.admin_user['username']}")
            
            if st.session_state.impersonated_user:
                st.warning(f"**Impersonating:** {st.session_state.impersonated_user['username']}")
                if st.button("🔙 Return to Admin", use_container_width=True):
                    SessionManager.end_impersonation()
                    st.rerun()
                st.markdown("---")
            
            # Navigation menu
            menu_items = {
                'dashboard': '📊 Dashboard Overview',
                'users': '👥 Manage Users',
                'plans': '💼 Manage Plans',
                'subscriptions': '📋 Subscriptions',
                'settings': '⚙️ Settings'
            }
            
            for page_key, page_name in menu_items.items():
                if st.button(page_name, use_container_width=True):
                    st.session_state.current_page = page_key
                    st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                SessionManager.logout_admin()
                st.rerun()
    
    def render_dashboard_overview(self):
        """Render dashboard overview"""
        st.markdown("# 📊 Dashboard Overview")
        
        # Statistics
        total_users = self.db.get_user_count()
        users = self.db.get_all_users(limit=1000)
        
        active_users = len([u for u in users if u['subscription_status'] == 'active'])
        expired_users = len([u for u in users if u['subscription_status'] == 'expired'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", total_users)
        
        with col2:
            st.metric("Active Users", active_users)
        
        with col3:
            st.metric("Expired Users", expired_users)
        
        with col4:
            st.metric("Total Plans", len(self.db.get_all_plans()))
        
        # Recent users
        st.markdown("### 📈 Recent Users")
        recent_users = self.db.get_all_users(limit=10)
        
        if recent_users:
            df = pd.DataFrame(recent_users)
            st.dataframe(df[['username', 'email', 'plan_name', 'subscription_status']], use_container_width=True)
        else:
            st.info("No users found")
    
    def render_users_page(self):
        """Render users management page"""
        st.markdown("# 👥 Manage Users")
        
        # Search and filters
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_term = st.text_input("🔍 Search users", placeholder="Search by username or email")
        
        with col2:
            status_filter = st.selectbox("Status Filter", ["All", "Active", "Expired", "Suspended"])
        
        with col3:
            if st.button("➕ Add New User", use_container_width=True):
                st.session_state.show_add_user = True
        
        # Pagination
        users_per_page = 20
        total_users = self.db.get_user_count()
        total_pages = (total_users - 1) // users_per_page + 1
        
        if 'current_user_page' not in st.session_state:
            st.session_state.current_user_page = 1
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_user_page <= 1):
                st.session_state.current_user_page -= 1
                st.rerun()
        
        with col2:
            st.markdown(f"<div style='text-align: center'>Page {st.session_state.current_user_page} of {total_pages}</div>", unsafe_allow_html=True)
        
        with col3:
            if st.button("Next ➡️", disabled=st.session_state.current_user_page >= total_pages):
                st.session_state.current_user_page += 1
                st.rerun()
        
        # Users table
        offset = (st.session_state.current_user_page - 1) * users_per_page
        users = self.db.get_all_users(limit=users_per_page, offset=offset)
        
        if users:
            st.markdown("### Users List")
            
            for i, user in enumerate(users):
                with st.container():
                    cols = st.columns([1, 2, 2, 1, 1, 1, 2, 3])
                    
                    with cols[0]:
                        st.write(f"**{offset + i + 1}**")
                    
                    with cols[1]:
                        st.write(f"**{user['username']}**")
                    
                    with cols[2]:
                        st.write(user['email'])
                    
                    with cols[3]:
                        st.write(f"{user['current_devices']}/{user['device_limit']}")
                    
                    with cols[4]:
                        st.write(user['dealer_code'] or "N/A")
                    
                    with cols[5]:
                        status_color = "🟢" if user['subscription_status'] == 'active' else "🔴"
                        st.write(f"{status_color} {user['subscription_status'].title()}")
                    
                    with cols[6]:
                        st.write(user['subscription_end'] or "N/A")
                    
                    with cols[7]:
                        action_cols = st.columns(3)
                        
                        with action_cols[0]:
                            if st.button("👤", key=f"login_{user['id']}", help="Login as User"):
                                SessionManager.impersonate_user(user)
                                st.rerun()
                        
                        with action_cols[1]:
                            if st.button("✏️", key=f"edit_{user['id']}", help="Edit User"):
                                st.session_state.edit_user_id = user['id']
                                st.session_state.current_page = 'edit_user'
                                st.rerun()
                        
                        with action_cols[2]:
                            if st.button("🗑️", key=f"delete_{user['id']}", help="Delete User"):
                                if self.db.delete_user(user['id']):
                                    st.success("User deleted successfully!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete user")
                    
                    st.divider()
        else:
            st.info("No users found")
    
    def render_edit_user_page(self):
        """Render edit user page"""
        if 'edit_user_id' not in st.session_state:
            st.session_state.current_page = 'users'
            st.rerun()
            return
        
        user = self.db.get_user_by_id(st.session_state.edit_user_id)
        if not user:
            st.error("User not found")
            return
        
        st.markdown(f"# ✏️ Edit User: {user['username']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.form("edit_user_form"):
                st.markdown("### Basic Information")
                
                new_username = st.text_input("Username", value=user['username'])
                new_email = st.text_input("Email", value=user['email'])
                
                # Plan selection
                st.markdown("### Subscription Plan")
                plans = self.db.get_all_plans()
                plan_options = {p['id']: f"{p['plan_name']} (₹{p['price']}, {p['device_limit']} devices)" for p in plans}
                plan_options[None] = "No Plan"
                
                current_plan_id = user['plan_id']
                plan_index = list(plan_options.keys()).index(current_plan_id) if current_plan_id in plan_options else 0
                
                selected_plan_id = st.selectbox(
                    "Select Plan",
                    options=list(plan_options.keys()),
                    format_func=lambda x: plan_options[x],
                    index=plan_index
                )
                
                # Device settings
                st.markdown("### Device Settings")
                new_device_limit = st.number_input("Device Limit", min_value=1, max_value=1000, value=user['device_limit'])
                new_current_devices = st.number_input("Current Devices", min_value=0, max_value=1000, value=user['current_devices'])
                
                # Subscription settings
                st.markdown("### Subscription")
                new_dealer_code = st.text_input("Dealer Code", value=user['dealer_code'] or "")
                new_status = st.selectbox("Status", ['active', 'expired', 'suspended'], 
                                        index=['active', 'expired', 'suspended'].index(user['subscription_status']))
                
                # Dates
                col_start, col_end = st.columns(2)
                with col_start:
                    new_start_date = st.date_input("Subscription Start", 
                                                 value=datetime.datetime.strptime(user['subscription_start'], '%Y-%m-%d').date() if user['subscription_start'] else datetime.date.today())
                
                with col_end:
                    new_end_date = st.date_input("Subscription End",
                                               value=datetime.datetime.strptime(user['subscription_end'], '%Y-%m-%d').date() if user['subscription_end'] else datetime.date.today())
                
                # Submit buttons
                col_save, col_cancel = st.columns(2)
                
                with col_save:
                    save_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
                
                with col_cancel:
                    cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if save_button:
                    update_data = {
                        'username': new_username,
                        'email': new_email,
                        'plan_id': selected_plan_id,
                        'device_limit': new_device_limit,
                        'current_devices': new_current_devices,
                        'dealer_code': new_dealer_code,
                        'subscription_status': new_status,
                        'subscription_start': new_start_date.isoformat(),
                        'subscription_end': new_end_date.isoformat()
                    }
                    
                    if self.db.update_user(user['id'], update_data):
                        st.success("User updated successfully!")
                        st.session_state.current_page = 'users'
                        st.rerun()
                    else:
                        st.error("Failed to update user")
                
                if cancel_button:
                    st.session_state.current_page = 'users'
                    st.rerun()
        
        with col2:
            st.markdown("### Current User Info")
            st.info(f"""
            **Username:** {user['username']}
            **Email:** {user['email']}
            **Plan:** {user['plan_name']}
            **Devices:** {user['current_devices']}/{user['device_limit']}
            **Status:** {user['subscription_status'].title()}
            **Created:** {user['created_at'][:10]}
            """)
    
    def render_user_dashboard(self):
        """Render impersonated user dashboard"""
        if not st.session_state.impersonated_user:
            st.session_state.current_page = 'dashboard'
            st.rerun()
            return
        
        user = st.session_state.impersonated_user
        
        st.markdown(f"# 👤 User Dashboard - {user['username']}")
        st.warning("🔄 You are viewing this as an administrator impersonating this user")
        
        # User info cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Plan", user['plan_name'])
        
        with col2:
            st.metric("Device Usage", f"{user['current_devices']}/{user['device_limit']}")
        
        with col3:
            status_emoji = "✅" if user['subscription_status'] == 'active' else "❌"
            st.metric("Status", f"{status_emoji} {user['subscription_status'].title()}")
        
        with col4:
            st.metric("Expires", user['subscription_end'] or "N/A")
        
        # Detailed user information
        st.markdown("### 📋 Account Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Username:** {user['username']}
            **Email:** {user['email']}
            **Dealer Code:** {user['dealer_code'] or 'N/A'}
            """)
        
        with col2:
            st.markdown(f"""
            **Subscription Start:** {user.get('subscription_start', 'N/A')}
            **Subscription End:** {user.get('subscription_end', 'N/A')}
            **Account Created:** {user.get('created_at', 'N/A')[:10] if user.get('created_at') else 'N/A'}
            """)
        
        # Usage simulation
        st.markdown("### 🤖 AI Assistant Features")
        st.info("This is where the user would interact with the Veterans India AI Assistant")
        
        # Mock features based on plan
        if user['plan_name'] != "No Plan":
            st.success("✅ Chat with AI Assistant")
            st.success("✅ Document Analysis")
            
            if user['plan_name'] in ['Standard', 'Premium', 'Enterprise']:
                st.success("✅ Real-time Web Search")
                st.success("✅ Advanced AI Features")
            
            if user['plan_name'] in ['Premium', 'Enterprise']:
                st.success("✅ Priority Support")
                st.success("✅ Custom Training")
            
            if user['plan_name'] == 'Enterprise':
                st.success("✅ Custom Integration")
                st.success("✅ 24/7 Support")
        else:
            st.warning("No active plan - Limited features available")

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Veterans India Admin Dashboard",
        page_icon="🇮🇳",
        layout="wide"
    )
    
    # Initialize database and session
    db_manager = DatabaseManager()
    SessionManager.init_session()
    ui = AdminUI(db_manager)
    
    # Route to appropriate page
    if not st.session_state.admin_logged_in:
        ui.render_login_page()
    else:
        # Render sidebar for logged-in admin
        ui.render_sidebar()
        
        # Route to current page
        current_page = st.session_state.current_page
        
        if current_page == 'dashboard':
            ui.render_dashboard_overview()
        elif current_page == 'users':
            ui.render_users_page()
        elif current_page == 'edit_user':
            ui.render_edit_user_page()
        elif current_page == 'user_dashboard':
            ui.render_user_dashboard()
        elif current_page == 'plans':
            st.markdown("# 💼 Manage Plans")
            st.info("Plans management feature coming soon...")
        elif current_page == 'subscriptions':
            st.markdown("# 📋 Subscriptions")
            st.info("Subscriptions management feature coming soon...")
        elif current_page == 'settings':
            st.markdown("# ⚙️ Settings")
            st.info("Settings page coming soon...")
        else:
            ui.render_dashboard_overview()

if __name__ == "__main__":
    main()
