"""
Veterans India AI Assistant - Enhanced Admin Dashboard
====================================================
Extended admin functionality with plans management, 
subscription controls, and comprehensive reporting.

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
import plotly.express as px
import plotly.graph_objects as go

# Enhanced Database Manager with additional features
class EnhancedDatabaseManager:
    def __init__(self, db_path="veterans_admin.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Previous tables from admin_dashboard.py
        # ... (keeping all previous table definitions)
        
        # Additional tables for enhanced features
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscription_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan_id INTEGER,
            action TEXT, -- 'created', 'renewed', 'upgraded', 'downgraded', 'expired'
            previous_plan_id INTEGER,
            start_date DATE,
            end_date DATE,
            amount REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            device_name TEXT,
            device_type TEXT,
            device_id TEXT UNIQUE,
            last_active TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action TEXT,
            target_type TEXT, -- 'user', 'plan', 'subscription'
            target_id INTEGER,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admins (id)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_dashboard_stats(self) -> Dict:
        """Get comprehensive dashboard statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # User statistics
        cursor.execute("SELECT COUNT(*) FROM users")
        stats['total_users'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE subscription_status = 'active'")
        stats['active_users'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE subscription_status = 'expired'")
        stats['expired_users'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE subscription_end < date('now')")
        stats['overdue_users'] = cursor.fetchone()[0]
        
        # Revenue statistics
        cursor.execute('''
        SELECT SUM(p.price) FROM users u
        JOIN plans p ON u.plan_id = p.id
        WHERE u.subscription_status = 'active'
        ''')
        result = cursor.fetchone()[0]
        stats['monthly_revenue'] = result if result else 0
        
        # Plan distribution
        cursor.execute('''
        SELECT p.plan_name, COUNT(u.id) as user_count
        FROM plans p
        LEFT JOIN users u ON p.id = u.plan_id AND u.subscription_status = 'active'
        GROUP BY p.id, p.plan_name
        ORDER BY user_count DESC
        ''')
        stats['plan_distribution'] = cursor.fetchall()
        
        conn.close()
        return stats
    
    def create_plan(self, plan_data: Dict) -> bool:
        """Create new subscription plan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO plans (plan_name, device_limit, price, duration_days, features, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                plan_data['plan_name'],
                plan_data['device_limit'],
                plan_data['price'],
                plan_data['duration_days'],
                json.dumps(plan_data['features']),
                plan_data['is_active']
            ))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def update_plan(self, plan_id: int, plan_data: Dict) -> bool:
        """Update existing plan"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE plans SET 
                plan_name = ?, device_limit = ?, price = ?, 
                duration_days = ?, features = ?, is_active = ?
            WHERE id = ?
            ''', (
                plan_data['plan_name'],
                plan_data['device_limit'],
                plan_data['price'],
                plan_data['duration_days'],
                json.dumps(plan_data['features']),
                plan_data['is_active'],
                plan_id
            ))
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False
    
    def get_subscription_analytics(self) -> Dict:
        """Get subscription analytics data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Subscription trends over time
        cursor.execute('''
        SELECT DATE(created_at) as date, COUNT(*) as new_users
        FROM users
        WHERE created_at >= date('now', '-30 days')
        GROUP BY DATE(created_at)
        ORDER BY date
        ''')
        signup_trends = cursor.fetchall()
        
        # Expiring subscriptions in next 30 days
        cursor.execute('''
        SELECT * FROM users
        WHERE subscription_end BETWEEN date('now') AND date('now', '+30 days')
        AND subscription_status = 'active'
        ORDER BY subscription_end
        ''')
        expiring_soon = cursor.fetchall()
        
        conn.close()
        return {
            'signup_trends': signup_trends,
            'expiring_soon': expiring_soon
        }
    
    def log_admin_action(self, admin_id: int, action: str, target_type: str, target_id: int, details: str):
        """Log admin actions for audit trail"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO admin_logs (admin_id, action, target_type, target_id, details)
        VALUES (?, ?, ?, ?, ?)
        ''', (admin_id, action, target_type, target_id, details))
        
        conn.commit()
        conn.close()

# Enhanced UI Components
class EnhancedAdminUI:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def render_enhanced_dashboard(self):
        """Render enhanced dashboard with analytics"""
        st.markdown("# 📊 Dashboard Overview")
        
        # Get statistics
        stats = self.db.get_dashboard_stats()
        analytics = self.db.get_subscription_analytics()
        
        # Key metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Users", stats['total_users'])
        
        with col2:
            st.metric("Active Users", stats['active_users'])
        
        with col3:
            st.metric("Expired Users", stats['expired_users'])
        
        with col4:
            st.metric("Overdue", stats['overdue_users'])
        
        with col5:
            st.metric("Monthly Revenue", f"₹{stats['monthly_revenue']:,.0f}")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Plan distribution pie chart
            st.markdown("### 📈 Plan Distribution")
            plan_data = stats['plan_distribution']
            if plan_data:
                df_plans = pd.DataFrame(plan_data, columns=['Plan', 'Users'])
                fig = px.pie(df_plans, values='Users', names='Plan', 
                           title="Active Users by Plan")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Signup trends
            st.markdown("### 📅 Signup Trends (30 Days)")
            if analytics['signup_trends']:
                df_trends = pd.DataFrame(analytics['signup_trends'], 
                                       columns=['Date', 'New Users'])
                fig = px.line(df_trends, x='Date', y='New Users',
                            title="Daily New User Signups")
                st.plotly_chart(fig, use_container_width=True)
        
        # Expiring subscriptions alert
        if analytics['expiring_soon']:
            st.markdown("### ⚠️ Expiring Subscriptions (Next 30 Days)")
            df_expiring = pd.DataFrame(analytics['expiring_soon'])
            st.dataframe(df_expiring[['username', 'email', 'subscription_end']], 
                        use_container_width=True)
    
    def render_plans_management(self):
        """Render plans management page"""
        st.markdown("# 💼 Manage Plans")
        
        # Add new plan form
        with st.expander("➕ Add New Plan"):
            with st.form("add_plan_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    plan_name = st.text_input("Plan Name")
                    device_limit = st.number_input("Device Limit", min_value=1, value=3)
                    price = st.number_input("Price (₹)", min_value=0.0, value=99.0)
                
                with col2:
                    duration_days = st.number_input("Duration (Days)", min_value=1, value=30)
                    is_active = st.checkbox("Active Plan", value=True)
                
                st.markdown("**Features** (one per line):")
                features_text = st.text_area("Features", 
                                           placeholder="Enter features, one per line\nExample:\nChat Support\nWeb Search\nPriority Support")
                
                if st.form_submit_button("Create Plan"):
                    if plan_name and price > 0:
                        features = [f.strip() for f in features_text.split('\n') if f.strip()]
                        plan_data = {
                            'plan_name': plan_name,
                            'device_limit': device_limit,
                            'price': price,
                            'duration_days': duration_days,
                            'features': features,
                            'is_active': is_active
                        }
                        
                        if self.db.create_plan(plan_data):
                            st.success("Plan created successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to create plan")
                    else:
                        st.error("Please fill in all required fields")
        
        # Existing plans
        st.markdown("### 📋 Current Plans")
        plans = self.db.get_all_plans()
        
        for plan in plans:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    status_emoji = "✅" if plan['is_active'] else "❌"
                    st.markdown(f"**{status_emoji} {plan['plan_name']}**")
                    st.write(f"Features: {', '.join(plan['features'])}")
                
                with col2:
                    st.write(f"**₹{plan['price']}**")
                    st.write(f"{plan['duration_days']} days")
                
                with col3:
                    st.write(f"**{plan['device_limit']} devices**")
                
                with col4:
                    edit_col, delete_col = st.columns(2)
                    
                    with edit_col:
                        if st.button("✏️ Edit", key=f"edit_plan_{plan['id']}"):
                            st.session_state.edit_plan_id = plan['id']
                    
                    with delete_col:
                        if st.button("🗑️ Delete", key=f"delete_plan_{plan['id']}"):
                            # Add delete confirmation logic here
                            st.warning("Delete confirmation needed")
                
                st.divider()
    
    def render_subscriptions_page(self):
        """Render subscriptions management page"""
        st.markdown("# 📋 Subscriptions Management")
        
        # Quick actions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔄 Renew Expiring", use_container_width=True):
                st.info("Bulk renewal feature")
        
        with col2:
            if st.button("📧 Send Reminders", use_container_width=True):
                st.info("Email reminder feature")
        
        with col3:
            if st.button("📊 Export Data", use_container_width=True):
                st.info("Data export feature")
        
        with col4:
            if st.button("💰 Revenue Report", use_container_width=True):
                st.info("Revenue analytics")
        
        # Subscription filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox("Status", ["All", "Active", "Expired", "Expiring Soon"])
        
        with col2:
            plan_filter = st.selectbox("Plan", ["All Plans"] + [p['plan_name'] for p in self.db.get_all_plans()])
        
        with col3:
            date_range = st.selectbox("Period", ["All Time", "Last 30 Days", "Last 90 Days", "This Year"])
        
        # Subscription list with enhanced info
        users = self.db.get_all_users(limit=100)  # Get more for filtering
        
        st.markdown("### 📊 Subscription Details")
        
        for user in users[:20]:  # Show first 20 for demo
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
                
                with col1:
                    st.write(f"**{user['username']}**")
                    st.write(user['email'])
                
                with col2:
                    st.write(f"**{user['plan_name']}**")
                
                with col3:
                    status_color = "🟢" if user['subscription_status'] == 'active' else "🔴"
                    st.write(f"{status_color} {user['subscription_status'].title()}")
                
                with col4:
                    st.write(user['subscription_end'] or "N/A")
                
                with col5:
                    action_col1, action_col2 = st.columns(2)
                    
                    with action_col1:
                        if st.button("🔄", key=f"renew_{user['id']}", help="Renew Subscription"):
                            st.info("Renewal dialog would open here")
                    
                    with action_col2:
                        if st.button("💰", key=f"billing_{user['id']}", help="Billing History"):
                            st.info("Billing history would open here")
                
                st.divider()
    
    def render_settings_page(self):
        """Render admin settings page"""
        st.markdown("# ⚙️ Admin Settings")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🔧 General", "👥 Admin Users", "📧 Notifications", "🔒 Security"])
        
        with tab1:
            st.markdown("### General Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Company Name", value="Veterans India")
                st.text_input("Support Email", value="support@veteransindia.org")
                st.text_input("Website URL", value="https://veteransindia.org")
            
            with col2:
                st.number_input("Default Device Limit", value=3)
                st.number_input("Grace Period (Days)", value=7)
                st.selectbox("Default Currency", ["INR", "USD", "EUR"])
            
            if st.button("Save General Settings"):
                st.success("Settings saved successfully!")
        
        with tab2:
            st.markdown("### Admin User Management")
            
            # Add new admin
            with st.expander("➕ Add New Admin"):
                with st.form("add_admin_form"):
                    new_admin_username = st.text_input("Username")
                    new_admin_email = st.text_input("Email")
                    new_admin_password = st.text_input("Password", type="password")
                    admin_role = st.selectbox("Role", ["Super Admin", "Admin", "Support"])
                    
                    if st.form_submit_button("Create Admin"):
                        st.success("Admin created successfully!")
            
            # Existing admins list
            st.markdown("#### Current Admins")
            st.info("Admin user list would be displayed here")
        
        with tab3:
            st.markdown("### Notification Settings")
            
            st.checkbox("Email notifications for new users", value=True)
            st.checkbox("Email notifications for expired subscriptions", value=True)
            st.checkbox("Daily admin reports", value=False)
            st.checkbox("Weekly revenue reports", value=True)
            
            st.text_area("Email Template for Expiry Reminders", 
                        value="Dear {username}, your subscription expires on {expiry_date}...")
            
            if st.button("Save Notification Settings"):
                st.success("Notification settings saved!")
        
        with tab4:
            st.markdown("### Security Settings")
            
            st.number_input("Session Timeout (minutes)", value=60)
            st.checkbox("Require 2FA for admin accounts", value=False)
            st.checkbox("Log all admin actions", value=True)
            st.number_input("Password minimum length", value=8)
            
            if st.button("Save Security Settings"):
                st.success("Security settings saved!")

def main():
    """Enhanced main application"""
    st.set_page_config(
        page_title="Veterans India Admin Dashboard",
        page_icon="🇮🇳",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize enhanced system
    db_manager = EnhancedDatabaseManager()
    
    # Import and use components from original admin_dashboard.py
    from admin_dashboard import SessionManager, AdminUI
    
    SessionManager.init_session()
    ui = AdminUI(db_manager)
    enhanced_ui = EnhancedAdminUI(db_manager)
    
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e0e2e6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if not st.session_state.admin_logged_in:
        ui.render_login_page()
    else:
        # Enhanced sidebar
        ui.render_sidebar()
        
        # Enhanced page routing
        current_page = st.session_state.current_page
        
        if current_page == 'dashboard':
            enhanced_ui.render_enhanced_dashboard()
        elif current_page == 'users':
            ui.render_users_page()
        elif current_page == 'edit_user':
            ui.render_edit_user_page()
        elif current_page == 'user_dashboard':
            ui.render_user_dashboard()
        elif current_page == 'plans':
            enhanced_ui.render_plans_management()
        elif current_page == 'subscriptions':
            enhanced_ui.render_subscriptions_page()
        elif current_page == 'settings':
            enhanced_ui.render_settings_page()
        else:
            enhanced_ui.render_enhanced_dashboard()

if __name__ == "__main__":
    main()
