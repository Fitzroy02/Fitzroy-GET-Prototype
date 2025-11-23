import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

def init_users_db():
    """Initialize users database"""
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_login TEXT
    )
    """)
    conn.commit()
    return conn, c

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username_or_email, password):
    """Verify user credentials"""
    conn, c = init_users_db()
    password_hash = hash_password(password)
    
    c.execute("""
        SELECT id, username, email, role FROM users 
        WHERE (username = ? OR email = ?) AND password_hash = ?
    """, (username_or_email, username_or_email, password_hash))
    
    user = c.fetchone()
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "role": user[3]
        }
    return None

def register_user(username, email, password, role):
    """Register a new user"""
    conn, c = init_users_db()
    password_hash = hash_password(password)
    
    try:
        c.execute("""
            INSERT INTO users (username, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, role, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username or email already exists"

def login_register_window():
    """Display login/register window"""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 500px;
            margin: 50px auto;
            padding: 30px;
            background-color: #ffffff;
            border: 2px solid #2E86AB;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .auth-title {
            color: #2E86AB;
            text-align: center;
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 20px;
        }
        .auth-divider {
            border-top: 1px solid #e0e0e0;
            margin: 20px 0;
        }
        .auth-options {
            text-align: center;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">🔐 Login / Register</div>', unsafe_allow_html=True)
    
    # Tab selection
    auth_mode = st.radio("Select authentication mode", ["Login", "Register"], horizontal=True, label_visibility="collapsed")
    
    st.markdown('<div class="auth-divider"></div>', unsafe_allow_html=True)
    
    if auth_mode == "Login":
        # Login form
        st.subheader("Login to Your Account")
        
        username_or_email = st.text_input("Username / Email", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        
        if col1.button("🔓 Login", use_container_width=True):
            if not username_or_email or not password:
                st.error("Please fill in all fields")
            else:
                user = verify_user(username_or_email, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user_id'] = user['username']
                    st.session_state['user_email'] = user['email']
                    st.session_state['role'] = user['role']
                    
                    # Update last login
                    conn, c = init_users_db()
                    c.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                             (datetime.now().isoformat(), user['id']))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Welcome back, {user['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid username/email or password")
        
        if col2.button("👤 Continue as Guest", use_container_width=True):
            st.session_state['authenticated'] = True
            st.session_state['user_id'] = "guest"
            st.session_state['role'] = "student"
            st.session_state['is_guest'] = True
            st.info("Continuing as guest (limited features)")
            st.rerun()
        
        st.markdown('<div class="auth-options">', unsafe_allow_html=True)
        if st.button("🔑 Forgot Password?", key="forgot_password"):
            st.info("Password reset functionality coming soon. Contact your administrator.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Registration form
        st.subheader("Create New Account")
        
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        role = st.selectbox(
            "Select Role",
            ["student", "practitioner", "author"],
            format_func=lambda x: {
                "student": "📚 Student - Access learning content",
                "practitioner": "👨‍⚕️ Practitioner - Upload & manage content",
                "author": "✍️ Author - Publish & monetize content"
            }[x]
        )
        
        if st.button("📝 Register", use_container_width=True):
            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif "@" not in email:
                st.error("Please enter a valid email address")
            else:
                success, message = register_user(username, email, password, role)
                if success:
                    st.success(message + " Please login to continue.")
                else:
                    st.error(message)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="auth-options">', unsafe_allow_html=True)
    st.caption("🔒 Your password is securely hashed. We never store plain text passwords.")
    st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Logout current user"""
    st.session_state['authenticated'] = False
    st.session_state['user_id'] = None
    st.session_state['role'] = None
    st.session_state['user_email'] = None
    if 'is_guest' in st.session_state:
        del st.session_state['is_guest']
    st.rerun()

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    return st.session_state['authenticated']

def get_current_user():
    """Get current logged in user"""
    return {
        'user_id': st.session_state.get('user_id', 'guest'),
        'role': st.session_state.get('role', 'student'),
        'email': st.session_state.get('user_email', ''),
        'is_guest': st.session_state.get('is_guest', False)
    }
