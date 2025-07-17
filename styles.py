def get_custom_css():
    """Return custom CSS for the application"""
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Open+Sans:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Open Sans', sans-serif;
        background-color: #F5F5F5;
    }
    
    /* Main header styling */
    .main-header {
        background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-family: 'Roboto', sans-serif;
        font-weight: 700;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background-color: #2E7D32;
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .sidebar-header h2 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    /* Result cards */
    .result-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2E7D32;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .result-card h3 {
        color: #1B5E20;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    
    /* Eligibility tags */
    .eligibility-tag {
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    
    .eligibility-tag.eligible {
        background-color: #4CAF50;
        color: white;
    }
    
    .eligibility-tag.not-eligible {
        background-color: #FF5722;
        color: white;
    }
    
    /* Stats container */
    .stats-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .stats-container .metric-container {
        background: linear-gradient(135deg, #FFB300 0%, #FF8F00 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2E7D32;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 500;
        transition: background-color 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #1B5E20;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #4CAF50;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #2E7D32;
    }
    
    /* Search input */
    .stTextInput > div > div > input {
        border: 2px solid #2E7D32;
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4CAF50;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
    }
    
    /* Selectbox and multiselect */
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        border: 2px solid #2E7D32;
        border-radius: 6px;
    }
    
    /* Checkboxes */
    .stCheckbox > label {
        color: #1B5E20;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #E8F5E8;
        border: 1px solid #2E7D32;
        border-radius: 6px;
        color: #1B5E20;
        font-weight: 500;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FFB300;
        margin-bottom: 1rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #E8F5E8;
        border-radius: 8px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #1B5E20;
        font-weight: 500;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #2E7D32;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: white !important;
    }
    
    /* Footer */
    .footer {
        background-color: #2E7D32;
        color: white;
        padding: 2rem;
        text-align: center;
        border-radius: 10px;
        margin-top: 3rem;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    
    /* Spinner */
    .stSpinner {
        color: #2E7D32;
    }
    
    /* Success, info, error messages */
    .stSuccess {
        background-color: #E8F5E8;
        border: 1px solid #4CAF50;
        border-radius: 6px;
        color: #1B5E20;
    }
    
    .stInfo {
        background-color: #E3F2FD;
        border: 1px solid #2196F3;
        border-radius: 6px;
        color: #0D47A1;
    }
    
    .stError {
        background-color: #FFEBEE;
        border: 1px solid #F44336;
        border-radius: 6px;
        color: #B71C1C;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .result-card {
            padding: 1rem;
        }
        
        .stats-container {
            padding: 1rem;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F5F5;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2E7D32;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1B5E20;
    }
    
    /* Animation for result cards */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-card {
        animation: slideIn 0.3s ease-out;
    }
    </style>
    """
