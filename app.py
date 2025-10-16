import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

# Page configuration
st.set_page_config(
    page_title="Old Age Home Connect",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Authentication Data
MOCK_USERS = {
    "resident": {"password": "pass123", "role": "Resident", "name": "Mrs. Sharma"},
    "volunteer": {"password": "pass123", "role": "Volunteer", "name": "Rahul Kumar"},
    "admin": {"password": "pass123", "role": "Admin", "name": "Admin User"}
}

# Generate Dummy Data Functions
def generate_dummy_requests():
    """Generate realistic service requests"""
    service_types = [
        "🚶 Morning Walk", "🛒 Grocery Shopping", "👨‍⚕️ Doctor Visit",
        "🏠 Home Help", "💊 Medicine Pickup", "📞 Phone Call",
        "🧹 Cleaning Help", "🍳 Cooking Assistance", "📖 Reading Companion"
    ]
    residents = ["Mrs. Sharma", "Mr. Gupta", "Mrs. Patel", "Mr. Singh", "Ms. Kapoor", 
                 "Mr. Rao", "Mrs. Khan", "Mr. Verma", "Ms. Joshi", "Mrs. Mehta"]
    volunteers = ["Rahul Kumar", "Priya Sharma", "Amit Patel", "Sneha Singh", 
                  "Vikram Reddy", "Anjali Gupta", "Rohan Das", "TBD"]
    statuses = ["Pending", "In Progress", "Completed", "Cancelled"]
    urgencies = ["Low", "Medium", "High", "Urgent"]
    
    requests = []
    for i in range(25):
        created_date = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        requests.append({
            "ID": f"REQ{i+1:03d}",
            "Type": random.choice(service_types),
            "Description": f"Request for assistance with daily activities. Special requirements noted.",
            "Time": f"{random.randint(8, 18):02d}:{random.choice(['00', '15', '30', '45'])}",
            "Urgency": random.choice(urgencies),
            "Status": random.choice(statuses) if i < 20 else "Pending",
            "Created": created_date.strftime("%Y-%m-%d %H:%M"),
            "Volunteer": random.choice(volunteers),
            "Resident": random.choice(residents)
        })
    return requests

def generate_dummy_donations():
    """Generate realistic donation data spanning multiple dates"""
    donors = [
        "Rajesh Kumar", "Priya Sharma", "Anonymous", "Amit Patel", "Sneha Gupta",
        "Vikram Industries", "Rahul Verma", "Anjali Singh", "Anonymous", "Tech Corp",
        "Rohan Das", "Kavita Reddy", "Anonymous", "Sunita Joshi", "Ramesh & Family",
        "Anonymous", "Neha Kapoor", "Arjun Mehta", "Anonymous", "Senior Care Foundation"
    ]
    
    donations = []
    # Generate donations over last 30 days
    for i in range(60):
        donation_date = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
        amount = random.choice([100, 200, 500, 1000, 1500, 2000, 2500, 5000, 10000])
        
        donations.append({
            "Amount": amount,
            "Donor": random.choice(donors),
            "Date": donation_date,
            "Campaign": random.choice(["Winter Care", "Medical Fund", "General Support", "Food Program"])
        })
    
    # Sort by date
    donations.sort(key=lambda x: x['Date'], reverse=True)
    return donations

# Initialize session state with dummy data
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'requests' not in st.session_state:
    st.session_state.requests = generate_dummy_requests()  # Pre-populated
if 'donations' not in st.session_state:
    st.session_state.donations = generate_dummy_donations()  # Pre-populated
if 'notifications' not in st.session_state:
    # Pre-populate notifications
    st.session_state.notifications = [
        {"time": "14:30", "msg": "New volunteer Rahul Kumar accepted your walk request", "type": "success"},
        {"time": "13:45", "msg": "Donation of ₹5,000 received from Anonymous donor", "type": "success"},
        {"time": "12:20", "msg": "Your grocery order #G123 is out for delivery", "type": "info"},
        {"time": "11:15", "msg": "Reminder: Doctor appointment tomorrow at 10:00 AM", "type": "warning"},
        {"time": "10:05", "msg": "Medicine pickup request REQ015 completed", "type": "success"},
    ]
if 'font_size' not in st.session_state:
    st.session_state.font_size = 16
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'theme_color' not in st.session_state:
    st.session_state.theme_color = "#4CAF50"

# IMPROVED CSS with Better Visibility and Contrast
st.markdown(f"""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Main Background - Subtle Light Gradient */
        .main {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 25%, #f8f9fa 50%, #e3e9f0 75%, #f0f4f8 100%);
            font-family: 'Inter', sans-serif;
        }}
        
        /* Block Container - Solid White Background */
        .block-container {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 20px;
            padding: 2rem 3rem !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }}
        
        /* Sidebar - Solid Gradient with Good Contrast */
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            background: transparent;
        }}
        
        /* All Sidebar Text - White and Bold */
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        [data-testid="stSidebar"] label {{
            color: white !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: white !important;
        }}
        
        /* Headers - Dark and Clear */
        h1 {{
            font-size: {st.session_state.font_size * 2.2}px !important;
            color: #1a1a1a !important;
            font-weight: 800 !important;
            text-align: center;
            margin-bottom: 0.5rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.05);
        }}
        
        h2 {{
            font-size: {st.session_state.font_size * 1.7}px !important;
            color: #2d3748 !important;
            font-weight: 700 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
        }}
        
        h3 {{
            font-size: {st.session_state.font_size * 1.4}px !important;
            color: #4a5568 !important;
            font-weight: 600 !important;
        }}
        
        /* All Body Text - Dark and Readable */
        p, div, span, label, li {{
            color: #2d3748 !important;
            font-size: {st.session_state.font_size}px !important;
            line-height: 1.6 !important;
        }}
        
        /* Card Container Style - Solid Background */
        .card {{
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border: 1px solid #e2e8f0;
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        }}
        
        /* Enhanced Buttons with Better Visibility */
        .stButton > button {{
            font-size: {st.session_state.font_size * 1.1}px !important;
            padding: 0.75rem 2rem !important;
            border-radius: 12px !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 700 !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
        }}
        
        /* Metric Cards - White Background with Dark Text */
        [data-testid="stMetricValue"] {{
            font-size: {st.session_state.font_size * 2.2}px !important;
            color: #1a1a1a !important;
            font-weight: 800 !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            font-size: {st.session_state.font_size * 1}px !important;
            color: #4a5568 !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        [data-testid="stMetricDelta"] {{
            color: #2d3748 !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="metric-container"] {{
            background: white;
            padding: 1.5rem !important;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }}
        
        [data-testid="metric-container"]:hover {{
            transform: scale(1.03);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }}
        
        /* Enhanced Input Fields - White Background */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {{
            font-size: {st.session_state.font_size}px !important;
            border-radius: 10px !important;
            border: 2px solid #cbd5e0 !important;
            padding: 0.75rem !important;
            background: white !important;
            color: #2d3748 !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
        }}
        
        /* Input Labels - Dark and Bold */
        .stTextInput label,
        .stSelectbox label,
        .stTextArea label,
        .stNumberInput label,
        .stDateInput label,
        .stTimeInput label {{
            color: #2d3748 !important;
            font-weight: 600 !important;
            font-size: {st.session_state.font_size * 1.05}px !important;
        }}
        
        /* Tabs - Better Visibility */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
            background: #f7fafc;
            border-radius: 12px;
            padding: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            font-size: {st.session_state.font_size * 1.1}px !important;
            padding: 0.75rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            color: #4a5568 !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTabs [data-baseweb="tab"]:hover {{
            background: #e2e8f0;
            color: #2d3748 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }}
        
        /* Progress Bar */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        }}
        
        .stProgress > div > div {{
            background-color: #e2e8f0 !important;
        }}
        
        /* DataFrames - White Background with Dark Text */
        [data-testid="stDataFrame"] {{
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
            background: white !important;
        }}
        
        [data-testid="stDataFrame"] table {{
            color: #2d3748 !important;
        }}
        
        [data-testid="stDataFrame"] th {{
            background: #f7fafc !important;
            color: #1a1a1a !important;
            font-weight: 700 !important;
        }}
        
        /* Alert Boxes - Better Contrast */
        .stAlert {{
            border-radius: 12px !important;
            border: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
            background: white !important;
            color: #2d3748 !important;
            border-left: 4px solid #667eea !important;
        }}
        
        /* Expander */
        .streamlit-expanderHeader {{
            background: #f7fafc !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            color: #2d3748 !important;
            border: 1px solid #e2e8f0 !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: #edf2f7 !important;
        }}
        
        /* Slider */
        .stSlider > div > div > div {{
            color: #2d3748 !important;
            font-weight: 600 !important;
        }}
        
        /* Radio Buttons */
        [data-testid="stRadio"] label {{
            color: #2d3748 !important;
            font-weight: 600 !important;
        }}
        
        /* Form borders */
        [data-testid="stForm"] {{
            background: white;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px;
            padding: 1.5rem;
        }}
    </style>
""", unsafe_allow_html=True)

# Cached Data Loading
@st.cache_data(ttl=300)
def load_volunteer_tasks():
    return pd.DataFrame({
        "Service": ["Morning Walk", "Grocery Shopping", "Doctor Visit", "Emotional Support", "Medicine Pickup"],
        "Resident": ["Mrs. Patel", "Mr. Rao", "Ms. Gupta", "Mr. Khan", "Mrs. Singh"],
        "Time": ["08:00 AM", "04:30 PM", "10:00 AM Tomorrow", "Now", "02:00 PM"],
        "Urgency": ["Low", "Medium", "High", "Urgent", "Medium"],
        "Status": ["Open", "Open", "Open", "In Progress", "Open"]
    })

# Helper Functions
def add_notification(msg, type="info"):
    timestamp = datetime.now().strftime('%H:%M:%S')
    st.session_state.notifications.insert(0, {"time": timestamp, "msg": msg, "type": type})
    if len(st.session_state.notifications) > 15:
        st.session_state.notifications.pop()

def create_metric_card(label, value, delta=None, icon="📊"):
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f"<div style='font-size: 3rem;'>{icon}</div>", unsafe_allow_html=True)
    with col2:
        st.metric(label, value, delta)

def filter_items(items, search_query, fields):
    if not search_query:
        return items
    return [item for item in items if any(search_query.lower() in str(item.get(f, "")).lower() for f in fields)]

# ==================== AUTHENTICATION PAGE ====================
if not st.session_state.logged_in:
    st.markdown("""
        <div style='text-align: center; padding: 3rem 0;'>
            <h1 style='font-size: 4rem; margin-bottom: 1rem;'>❤️</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("Old Age Home Connect")
    st.markdown("<p style='text-align: center; font-size: 1.3rem; color: #4a5568; font-weight: 500;'>Empowering Seniors with Care, Connection, and Community</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            st.subheader("🔐 Login to Continue")
            with st.form("login_form", clear_on_submit=True):
                username = st.text_input("👤 Username", placeholder="Enter username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    submit = st.form_submit_button("Login", use_container_width=True)
                with col_b:
                    demo = st.form_submit_button("Demo Login", use_container_width=True)
                
                if submit or demo:
                    if demo:
                        username, password = "admin", "pass123"
                    
                    if username in MOCK_USERS and MOCK_USERS[username]["password"] == password:
                        with st.spinner("🔄 Authenticating..."):
                            time.sleep(0.5)
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.user_role = MOCK_USERS[username]["role"]
                            add_notification(f"Welcome {MOCK_USERS[username]['name']}! 👋", "success")
                            st.success("✅ Login successful!")
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.error("❌ Invalid credentials!")
            
            st.info("💡 Demo Credentials: `admin/pass123` | `resident/pass123` | `volunteer/pass123`")
    st.stop()

# ==================== DYNAMIC SIDEBAR ====================
with st.sidebar:
    st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.15); border-radius: 12px; margin-bottom: 1.5rem;'>
            <h2 style='color: white; margin: 0; font-size: 1.8rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>❤️ OAH Connect</h2>
        </div>
    """, unsafe_allow_html=True)
    
    user_name = MOCK_USERS[st.session_state.username]["name"]
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.2); padding: 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid rgba(255,255,255,0.3);'>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 0.95rem; font-weight: 500;'>Logged in as</p>
            <h3 style='color: white; margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: 700; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>{user_name}</h3>
            <p style='color: rgba(255,255,255,0.85); margin: 0.25rem 0 0 0; font-size: 0.9rem; font-weight: 600;'>{st.session_state.user_role}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: white; font-size: 1.2rem; margin-bottom: 0.5rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>🔍 Quick Search</h3>", unsafe_allow_html=True)
    search = st.text_input("Search anything...", value=st.session_state.search_query, label_visibility="collapsed", key="sidebar_search")
    if search != st.session_state.search_query:
        st.session_state.search_query = search
        st.rerun()
    
    st.markdown("<h3 style='color: white; font-size: 1.2rem; margin: 1.5rem 0 0.5rem 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>⚙️ Settings</h3>", unsafe_allow_html=True)
    new_font = st.slider("Font Size", 12, 24, st.session_state.font_size, key="font_slider")
    if new_font != st.session_state.font_size:
        st.session_state.font_size = new_font
        st.rerun()
    
    st.markdown("<h3 style='color: white; font-size: 1.2rem; margin: 1.5rem 0 0.5rem 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>📊 Quick Stats</h3>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.3);'>
            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem; font-weight: 600;'>Active Requests</p>
            <h3 style='color: white; margin: 0.25rem 0 0 0; font-size: 1.8rem; font-weight: 800; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>{len(st.session_state.requests)}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; border: 1px solid rgba(255,255,255,0.3);'>
            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem; font-weight: 600;'>Cart Items</p>
            <h3 style='color: white; margin: 0.25rem 0 0 0; font-size: 1.8rem; font-weight: 800; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>{len(st.session_state.cart)}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.3);'>
            <p style='color: rgba(255,255,255,0.8); margin: 0; font-size: 0.85rem; font-weight: 600;'>Notifications</p>
            <h3 style='color: white; margin: 0.25rem 0 0 0; font-size: 1.8rem; font-weight: 800; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>{len(st.session_state.notifications)}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.rerun()

# ==================== MAIN HEADER ====================
st.title("Old Age Home Connect")
st.markdown(f"""
    <p style='text-align: center; font-size: 1.2rem; color: #4a5568; margin-bottom: 2rem; font-weight: 500;'>
        Welcome back, <strong style='color: #1a1a1a;'>{user_name}</strong> • {st.session_state.user_role} Dashboard • 
        {datetime.now().strftime('%B %d, %Y • %I:%M %p')}
    </p>
""", unsafe_allow_html=True)

# ==================== DYNAMIC TABS ====================
if st.session_state.user_role == "Resident":
    tab_list = ["🏠 Dashboard", "📋 My Requests", "🛒 Marketplace", "💕 Companionship", "💬 Messages", "👤 Profile"]
elif st.session_state.user_role == "Volunteer":
    tab_list = ["🏠 Dashboard", "👥 My Tasks", "💬 Messages", "👤 Profile"]
else:  # Admin
    tab_list = ["🏠 Dashboard", "📋 All Requests", "👥 Volunteer Tasks", "❤️ Fundraising", "📊 Analytics", "👤 Settings"]

tabs = st.tabs(tab_list)

# ==================== DASHBOARD TAB (Common) ====================
with tabs[0]:
    st.header("📊 Dashboard Overview")
    
    # Metrics Row with Real Data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        active_requests = len([r for r in st.session_state.requests if r['Status'] in ['Pending', 'In Progress']])
        create_metric_card("Active Requests", active_requests, "+2", "📋")
    with col2:
        total_donations = sum([d.get('Amount', 0) for d in st.session_state.donations])
        create_metric_card("Total Donations", f"₹{total_donations:,}", "+₹15,000", "💰")
    with col3:
        create_metric_card("Volunteers", 24, "+3", "👥")
    with col4:
        create_metric_card("Satisfaction", "98%", "+2%", "⭐")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Progress Indicators
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Service Fulfillment")
        completed = len([r for r in st.session_state.requests if r['Status'] == 'Completed'])
        total_req = len(st.session_state.requests)
        fulfillment_rate = completed / total_req if total_req > 0 else 0
        st.progress(fulfillment_rate, text=f"{fulfillment_rate*100:.0f}% Complete")
        st.caption(f"{completed} out of {total_req} requests fulfilled")
    with col6:
        st.subheader("Fundraising Goal")
        goal = 200000
        progress_val = min(total_donations / goal, 1.0)
        st.progress(progress_val, text=f"₹{total_donations:,} / ₹{goal:,}")
        st.caption(f"{progress_val*100:.1f}% of monthly goal achieved")
    
    # Recent Activity
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📢 Recent Activity")
    
    if st.session_state.notifications:
        for notif in st.session_state.notifications[:5]:
            icon = "✅" if notif['type'] == "success" else "ℹ️"
            st.info(f"{icon} [{notif['time']}] {notif['msg']}")
    else:
        st.info("No recent activity. Your day is calm! 😊")

# ==================== ROLE-SPECIFIC TABS ====================

# RESIDENT TABS
if st.session_state.user_role == "Resident":
    # Service Requests Tab
    with tabs[1]:
        st.header("📋 My Service Requests")
        
        # Request Form Card
        with st.expander("➕ Create New Request", expanded=False):
            with st.form("new_request_form"):
                col1, col2 = st.columns(2)
                with col1:
                    service_type = st.selectbox(
                        "Service Type",
                        ["🚶 Morning Walk", "🛒 Grocery Shopping", "👨‍⚕️ Doctor Visit", 
                         "🏠 Home Help", "💊 Medicine Pickup", "📞 Phone Call", "Other"]
                    )
                    description = st.text_area("Description *", height=100, max_chars=200, 
                                              placeholder="Please describe your request in detail...")
                with col2:
                    preferred_time = st.time_input("Preferred Time")
                    urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Urgent"])
                    preferred_volunteer = st.text_input("Preferred Volunteer (Optional)")
                
                submit_btn = st.form_submit_button("✅ Submit Request", use_container_width=True)
                
                if submit_btn:
                    if not description.strip():
                        st.error("❌ Please provide a description!")
                    else:
                        with st.spinner("🔄 Creating request..."):
                            time.sleep(0.5)
                            new_req = {
                                "ID": f"REQ{len(st.session_state.requests)+1:03d}",
                                "Type": service_type,
                                "Description": description.strip(),
                                "Time": str(preferred_time),
                                "Urgency": urgency,
                                "Status": "Pending",
                                "Created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "Volunteer": preferred_volunteer or "TBD",
                                "Resident": user_name
                            }
                            st.session_state.requests.insert(0, new_req)
                            add_notification(f"New request created: {service_type}", "success")
                            st.success("✅ Request submitted successfully!")
                            time.sleep(0.5)
                            st.rerun()
        
        # Display Requests
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(f"📝 All Service Requests ({len(st.session_state.requests)} total)")
        
        # Filter controls
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Pending", "In Progress", "Completed", "Cancelled"])
        with col2:
            urgency_filter = st.selectbox("Filter by Urgency", ["All", "Low", "Medium", "High", "Urgent"])
        with col3:
            sort_by = st.selectbox("Sort By", ["Created Date (Newest)", "Created Date (Oldest)", "Urgency"])
        
        # Apply filters
        filtered_requests = st.session_state.requests.copy()
        if status_filter != "All":
            filtered_requests = [r for r in filtered_requests if r['Status'] == status_filter]
        if urgency_filter != "All":
            filtered_requests = [r for r in filtered_requests if r['Urgency'] == urgency_filter]
        if st.session_state.search_query:
            filtered_requests = filter_items(filtered_requests, st.session_state.search_query, ["Type", "Description", "Resident"])
        
        # Sort
        if "Newest" in sort_by:
            filtered_requests.sort(key=lambda x: x['Created'], reverse=True)
        elif "Oldest" in sort_by:
            filtered_requests.sort(key=lambda x: x['Created'])
        
        st.info(f"Showing {len(filtered_requests)} of {len(st.session_state.requests)} requests")
        
        if filtered_requests:
            # Display as dataframe with better formatting
            df_requests = pd.DataFrame(filtered_requests)
            st.dataframe(
                df_requests[['ID', 'Type', 'Description', 'Resident', 'Time', 'Urgency', 'Status', 'Volunteer', 'Created']],
                use_container_width=True,
                hide_index=True
            )
            
            # Show detailed cards for top 5
            st.subheader("📌 Recent Requests (Detailed View)")
            for req in filtered_requests[:5]:
                urgency_color = {
                    "Low": "#4CAF50",
                    "Medium": "#FF9800",
                    "High": "#F44336",
                    "Urgent": "#D32F2F"
                }.get(req['Urgency'], "#666")
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.markdown(f"**{req['ID']}** • {req['Type']}")
                        st.caption(f"{req['Description'][:80]}...")
                        st.caption(f"👤 Resident: {req['Resident']}")
                    with col2:
                        st.markdown(f"⏰ Time: {req['Time']}")
                        st.caption(f"👨‍💼 Volunteer: {req['Volunteer']}")
                        st.caption(f"📅 Created: {req['Created']}")
                    with col3:
                        st.markdown(f"<div style='background: {urgency_color}; color: white; padding: 0.5rem; border-radius: 8px; text-align: center; font-weight: 700; margin-bottom: 0.5rem;'>{req['Urgency']}</div>", unsafe_allow_html=True)
                        status_color = {"Pending": "#FF9800", "In Progress": "#2196F3", "Completed": "#4CAF50", "Cancelled": "#9E9E9E"}.get(req['Status'], "#666")
                        st.markdown(f"<div style='background: {status_color}; color: white; padding: 0.5rem; border-radius: 8px; text-align: center; font-weight: 600;'>{req['Status']}</div>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.warning("No requests match your filters. Try adjusting the criteria.")
    
    # Marketplace Tab (same as before)
    with tabs[2]:
        st.header("🛒 Marketplace")
        
        categories = {
            "🏥 Healthcare": [
                ("Adult Diapers (Pack of 10)", 899),
                ("Blood Pressure Monitor", 1299),
                ("Walking Stick", 499),
                ("Medicine Organizer", 299)
            ],
            "🍎 Groceries": [
                ("Fresh Fruits (1kg)", 120),
                ("Milk (1L)", 60),
                ("Whole Wheat Bread", 45),
                ("Eggs (12 pcs)", 84)
            ],
            "📚 Leisure": [
                ("Large Print Books", 299),
                ("Puzzle Games", 199),
                ("Reading Glasses", 499)
            ]
        }
        
        for category, products in categories.items():
            st.subheader(category)
            cols = st.columns(4)
            
            filtered_products = [p for p in products if st.session_state.search_query.lower() in p[0].lower()] if st.session_state.search_query else products
            
            for idx, (name, price) in enumerate(filtered_products):
                with cols[idx % 4]:
                    st.markdown(f"""
                        <div style='background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0; text-align: center;'>
                            <p style='font-weight: 600; color: #2d3748; margin: 0.5rem 0;'>{name}</p>
                            <p style='font-size: 1.5rem; color: #667eea; font-weight: 800; margin: 0.5rem 0;'>₹{price}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"Add to Cart", key=f"add_{category}_{idx}", use_container_width=True):
                        st.session_state.cart.append({"Item": name, "Price": price, "Qty": 1})
                        add_notification(f"Added {name} to cart", "success")
                        st.rerun()
        
        if st.session_state.cart:
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("🛍️ Your Shopping Cart")
            
            df_cart = pd.DataFrame(st.session_state.cart)
            df_cart['Total'] = df_cart['Price'] * df_cart['Qty']
            
            st.dataframe(df_cart, use_container_width=True, hide_index=True)
            
            total = df_cart['Total'].sum()
            col1, col2, col3 = st.columns([2, 1, 1])
            with col2:
                st.metric("Cart Total", f"₹{total:,}")
            with col3:
                if st.button("💳 Checkout", use_container_width=True, key="checkout_btn"):
                    with st.spinner("Processing order..."):
                        time.sleep(1)
                        add_notification(f"Order placed! Total: ₹{total}", "success")
                        st.success("✅ Order confirmed! Delivery in 2 business days.")
                        st.balloons()
                        st.session_state.cart = []
                        time.sleep(1)
                        st.rerun()

    # Companionship Tab (same as before)
    with tabs[3]:
        st.header("💕 Companionship & Emotional Support")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📞 Schedule a Session")
            with st.form("companionship_form"):
                session_type = st.selectbox(
                    "Session Type",
                    ["📞 Audio Call", "📹 Video Call", "💬 Chat Session", "🤝 In-Person Visit"]
                )
                preferred_date = st.date_input("Preferred Date", min_value=datetime.now().date())
                duration = st.slider("Duration (minutes)", 15, 120, 30, step=15)
                notes = st.text_area("Additional Notes", placeholder="Any specific topics you'd like to discuss?")
                
                if st.form_submit_button("📅 Schedule Session", use_container_width=True):
                    with st.spinner("Scheduling..."):
                        time.sleep(0.5)
                        add_notification(f"{session_type} scheduled for {preferred_date}", "success")
                        st.success("✅ Session scheduled! You'll receive a confirmation email.")
                        st.rerun()
        
        with col2:
            st.subheader("💌 Quick Message")
            quick_msg = st.text_area("Send a message to support team", height=150, 
                                    placeholder="How are you feeling today? Any concerns?")
            if st.button("📨 Send Message", use_container_width=True):
                if quick_msg.strip():
                    add_notification("Message sent to support team", "success")
                    st.success("✅ Message sent successfully!")
                else:
                    st.error("❌ Please write a message first!")

# VOLUNTEER TABS
elif st.session_state.user_role == "Volunteer":
    with tabs[1]:
        st.header("👥 Available Tasks")
        
        tasks_df = load_volunteer_tasks()
        
        if st.session_state.search_query:
            mask = tasks_df.apply(lambda row: st.session_state.search_query.lower() in ' '.join(row.astype(str)).lower(), axis=1)
            tasks_df = tasks_df[mask]
        
        st.metric("Available Tasks", len(tasks_df[tasks_df['Status'] == 'Open']))
        
        for idx, task in tasks_df.iterrows():
            with st.expander(f"🎯 {task['Service']} for {task['Resident']} - {task['Urgency']} Priority"):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.markdown(f"**Service:** {task['Service']}")
                    st.markdown(f"**Resident:** {task['Resident']}")
                with col2:
                    st.markdown(f"**Time:** {task['Time']}")
                    st.markdown(f"**Urgency:** {task['Urgency']}")
                with col3:
                    if task['Status'] == 'Open':
                        if st.button("✅ Accept", key=f"accept_{idx}"):
                            with st.spinner("Assigning task..."):
                                time.sleep(0.5)
                                add_notification(f"Task accepted: {task['Service']} for {task['Resident']}", "success")
                                st.success("✅ Task assigned to you!")
                                st.rerun()
                    else:
                        st.info(f"Status: {task['Status']}")

# ADMIN TABS
elif st.session_state.user_role == "Admin":
    # All Requests Tab (Admin view)
    with tabs[1]:
        st.header("📋 All Service Requests Management")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Requests", len(st.session_state.requests))
        with col2:
            pending = len([r for r in st.session_state.requests if r['Status'] == 'Pending'])
            st.metric("Pending", pending, delta=f"{pending}")
        with col3:
            in_progress = len([r for r in st.session_state.requests if r['Status'] == 'In Progress'])
            st.metric("In Progress", in_progress)
        with col4:
            completed = len([r for r in st.session_state.requests if r['Status'] == 'Completed'])
            st.metric("Completed", completed, delta=f"+{completed}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filters
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Pending", "In Progress", "Completed", "Cancelled"], key="admin_status")
        with col2:
            urgency_filter = st.selectbox("Urgency", ["All", "Low", "Medium", "High", "Urgent"], key="admin_urgency")
        with col3:
            resident_filter = st.selectbox("Resident", ["All"] + list(set([r['Resident'] for r in st.session_state.requests])))
        with col4:
            service_filter = st.selectbox("Service Type", ["All"] + list(set([r['Type'] for r in st.session_state.requests])))
        
        # Apply filters
        filtered_requests = st.session_state.requests.copy()
        if status_filter != "All":
            filtered_requests = [r for r in filtered_requests if r['Status'] == status_filter]
        if urgency_filter != "All":
            filtered_requests = [r for r in filtered_requests if r['Urgency'] == urgency_filter]
        if resident_filter != "All":
            filtered_requests = [r for r in filtered_requests if r['Resident'] == resident_filter]
        if service_filter != "All":
            filtered_requests = [r for r in filtered_requests if r['Type'] == service_filter]
        if st.session_state.search_query:
            filtered_requests = filter_items(filtered_requests, st.session_state.search_query, ["Type", "Description", "Resident", "Volunteer"])
        
        st.info(f"📊 Showing {len(filtered_requests)} of {len(st.session_state.requests)} requests")
        
        if filtered_requests:
            df_requests = pd.DataFrame(filtered_requests)
            st.dataframe(
                df_requests[['ID', 'Type', 'Resident', 'Time', 'Urgency', 'Status', 'Volunteer', 'Created']],
                use_container_width=True,
                hide_index=True,
                height=400
            )
            
            # Export option
            if st.button("📥 Export to CSV", key="export_requests"):
                csv = df_requests.to_csv(index=False)
                st.download_button("Download CSV", csv, "requests_export.csv", "text/csv")
        else:
            st.warning("No requests match your filters.")
    
    # Fundraising Tab with Rich Data
    with tabs[3]:
        st.header("❤️ Fundraising Campaigns")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Current Campaign: Winter Care Package 2025")
            total_raised = sum([d.get('Amount', 0) for d in st.session_state.donations])
            goal = 200000
            progress = min(total_raised / goal, 1.0)
            
            st.progress(progress, text=f"₹{total_raised:,} / ₹{goal:,} ({progress*100:.1f}%)")
            
            # Campaign stats
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total Donors", len(st.session_state.donations))
            with col_b:
                avg_donation = total_raised / len(st.session_state.donations) if st.session_state.donations else 0
                st.metric("Avg Donation", f"₹{avg_donation:,.0f}")
            with col_c:
                largest = max([d['Amount'] for d in st.session_state.donations]) if st.session_state.donations else 0
                st.metric("Largest Gift", f"₹{largest:,}")
            
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 2rem; border-radius: 15px; color: white; margin: 1rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>
                    <h3 style='color: white; margin: 0; font-weight: 700;'>🎯 Campaign Goal</h3>
                    <p style='color: rgba(255,255,255,0.95); font-size: 1rem; font-weight: 500;'>Provide warm clothing, blankets, and heaters for 50 elderly residents this winter.</p>
                    <p style='color: white; font-weight: 600;'><strong>{len(st.session_state.donations)} donors</strong> have contributed so far! Days remaining: 45</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("💰 Quick Donate")
            with st.form("donation_form"):
                amount = st.number_input("Amount (₹)", min_value=100, max_value=100000, step=100, value=500)
                donor_name = st.text_input("Donor Name (Optional)")
                
                if st.form_submit_button("❤️ Donate Now", use_container_width=True):
                    if amount >= 100:
                        with st.spinner("Processing donation..."):
                            time.sleep(0.5)
                            donation = {
                                "Amount": amount,
                                "Donor": donor_name or "Anonymous",
                                "Date": datetime.now(),
                                "Campaign": "Winter Care"
                            }
                            st.session_state.donations.insert(0, donation)
                            add_notification(f"₹{amount} donated by {donor_name or 'Anonymous'}", "success")
                            st.success(f"✅ Thank you for your donation of ₹{amount}!")
                            st.balloons()
                            time.sleep(0.5)
                            st.rerun()
                    else:
                        st.error("Minimum donation: ₹100")
        
        # Recent Donations with full data
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader(f"🏆 Recent Donors (Showing 20 of {len(st.session_state.donations)})")
        if st.session_state.donations:
            df_donations = pd.DataFrame(st.session_state.donations[:20])
            df_donations['Date'] = pd.to_datetime(df_donations['Date']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df_donations, use_container_width=True, hide_index=True, height=400)
            
            # Export
            if st.button("📥 Export Donations", key="export_donations"):
                csv = pd.DataFrame(st.session_state.donations).to_csv(index=False)
                st.download_button("Download CSV", csv, "donations_export.csv", "text/csv")
    
    # Analytics Tab with Rich Visualizations
    with tabs[4]:
        st.header("📊 Analytics Dashboard")
        
        # Donation Analytics
        st.subheader("💰 Donation Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Daily Donation Trends")
            if st.session_state.donations:
                df_don = pd.DataFrame(st.session_state.donations)
                df_don['Date'] = pd.to_datetime(df_don['Date']).dt.date
                daily = df_don.groupby('Date')['Amount'].agg(['sum', 'count']).reset_index()
                daily.columns = ['Date', 'Total Amount', 'Number of Donations']
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=daily['Date'], 
                    y=daily['Total Amount'],
                    mode='lines+markers',
                    name='Daily Amount',
                    line=dict(color='#667eea', width=3),
                    fill='tozeroy'
                ))
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#2d3748', size=12, family='Inter'),
                    xaxis_title="Date",
                    yaxis_title="Amount (₹)",
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No donation data available yet.")
        
        with col2:
            st.markdown("### 🎯 Campaign Distribution")
            if st.session_state.donations:
                df_don = pd.DataFrame(st.session_state.donations)
                campaign_totals = df_don.groupby('Campaign')['Amount'].sum().reset_index()
                
                fig = px.pie(
                    campaign_totals, 
                    values='Amount', 
                    names='Campaign',
                    color_discrete_sequence=['#667eea', '#764ba2', '#f093fb', '#4facfe']
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#2d3748', size=12, family='Inter'),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Request Analytics
        st.subheader("📋 Request Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Status Distribution")
            if st.session_state.requests:
                status_counts = pd.DataFrame(st.session_state.requests)['Status'].value_counts().reset_index()
                status_counts.columns = ['Status', 'Count']
                
                fig = px.bar(
                    status_counts, 
                    x='Status', 
                    y='Count',
                    color='Status',
                    color_discrete_map={
                        'Pending': '#FF9800',
                        'In Progress': '#2196F3',
                        'Completed': '#4CAF50',
                        'Cancelled': '#9E9E9E'
                    }
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#2d3748', size=12, family='Inter'),
                    showlegend=False,
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ Urgency Levels")
            if st.session_state.requests:
                urgency_counts = pd.DataFrame(st.session_state.requests)['Urgency'].value_counts().reset_index()
                urgency_counts.columns = ['Urgency', 'Count']
                
                fig = px.pie(
                    urgency_counts, 
                    values='Count', 
                    names='Urgency',
                    color='Urgency',
                    color_discrete_map={
                        'Low': '#4CAF50',
                        'Medium': '#FF9800',
                        'High': '#F44336',
                        'Urgent': '#D32F2F'
                    }
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#2d3748', size=12, family='Inter'),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Service Type Analysis
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🎯 Top Service Types")
        if st.session_state.requests:
            service_counts = pd.DataFrame(st.session_state.requests)['Type'].value_counts().head(10).reset_index()
            service_counts.columns = ['Service Type', 'Count']
            
            fig = px.bar(
                service_counts, 
                x='Count', 
                y='Service Type',
                orientation='h',
                color='Count',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#2d3748', size=12, family='Inter'),
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional Metrics
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Response Time", "2.5 hrs", "-0.5 hrs")
        with col2:
            fulfillment = len([r for r in st.session_state.requests if r['Status'] == 'Completed']) / len(st.session_state.requests) * 100
            st.metric("Fulfillment Rate", f"{fulfillment:.0f}%", "+5%")
        with col3:
            st.metric("Volunteer Efficiency", "87%", "+3%")
        with col4:
            st.metric("Resident Satisfaction", "4.8/5", "+0.2")

# ==================== COMMON TABS ====================

# Messages/Notifications Tab
messages_tab_idx = {"Resident": 4, "Volunteer": 2, "Admin": -2}.get(st.session_state.user_role, -2)
with tabs[messages_tab_idx]:
    st.header("💬 Messages & Notifications")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📢 Recent Notifications")
        if st.session_state.notifications:
            for notif in st.session_state.notifications:
                icon = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "❌"}.get(notif['type'], "📌")
                st.markdown(f"""
                    <div style='background: white;
                                padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
                                border-left: 4px solid #667eea; box-shadow: 0 2px 6px rgba(0,0,0,0.08);'>
                        <strong style='color: #1a1a1a;'>{icon} [{notif['time']}]</strong> 
                        <span style='color: #4a5568;'>{notif['msg']}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            if st.button("🗑️ Clear All Notifications", key="clear_notifs"):
                st.session_state.notifications = []
                st.rerun()
        else:
            st.info("🎉 All caught up! No new notifications.")
    
    with col2:
        st.subheader("💬 Quick Chat")
        chat_msg = st.text_area("Message", height=150, placeholder="Type your message here...")
        if st.button("📤 Send", use_container_width=True):
            if chat_msg.strip():
                add_notification(f"Message sent: {chat_msg[:30]}...", "success")
                st.success("✅ Message sent!")
            else:
                st.error("❌ Please type a message!")

# Profile/Settings Tab
profile_tab_idx = -1
with tabs[profile_tab_idx]:
    st.header("👤 Profile & Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Personal Information")
        full_name = st.text_input("Full Name", value=user_name)
        email = st.text_input("Email", value=f"{st.session_state.username}@oahconnect.org")
        phone = st.text_input("Phone Number", placeholder="+91 XXXXX XXXXX")
        
        st.subheader("Preferences")
        language = st.selectbox("Preferred Language", ["English", "Hindi", "Telugu", "Tamil", "Bengali"])
        notifications_enabled = st.checkbox("Enable Notifications", value=True)
    
    with col2:
        st.subheader("Account Settings")
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        st.subheader("Appearance")
        theme_color = st.color_picker("Theme Color", st.session_state.theme_color)
        if theme_color != st.session_state.theme_color:
            st.session_state.theme_color = theme_color
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("💾 Save Changes", use_container_width=True):
            add_notification("Profile updated successfully!", "success")
            st.success("✅ Changes saved!")
    with col3:
        if st.button("🔄 Reset", use_container_width=True):
            st.info("Settings reset to default.")
    
    # Activity Log
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📜 Recent Activity Log")
    activity_data = pd.DataFrame({
        "Timestamp": [(datetime.now() - timedelta(hours=i)).strftime("%Y-%m-%d %H:%M:%S") for i in range(10)],
        "Action": ["Logged in", "Created request", "Added item to cart", "Sent message", "Updated profile",
                  "Viewed analytics", "Downloaded report", "Accepted donation", "Reviewed request", "Changed settings"],
        "Status": ["Success"] * 10
    })
    st.dataframe(activity_data, use_container_width=True, hide_index=True)

# ==================== FOOTER ====================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='background: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.08);'>
        <h4 style='color: #1a1a1a; margin: 0; font-weight: 700;'>Old Age Home Connect v2.0</h4>
        <p style='color: #4a5568; margin: 0.5rem 0 0 0; font-weight: 500;'>
            Empowering seniors with technology • Built with ❤️ using Streamlit<br>
            📧 support@oahconnect.org • 📞 1800-XXX-XXXX • 🌐 www.oahconnect.org
        </p>
        <p style='color: #718096; font-size: 0.9rem; margin: 0.5rem 0 0 0;'>
            © 2025 Old Age Home Connect. All rights reserved. | Privacy Policy | Terms of Service
        </p>
    </div>
""", unsafe_allow_html=True)
