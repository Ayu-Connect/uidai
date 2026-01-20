
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. Page Configuration & Title
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Aadhar Enrolment Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# 2. Custom CSS for "Advanced" Look
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Card-like styling for metrics */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e0e0;
    }

    /* Header styling */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Data Loading Function
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    files = [
        "api_data_aadhar_enrolment_0_500000.csv",
        "api_data_aadhar_enrolment_500000_1000000.csv",
        "api_data_aadhar_enrolment_1000000_1006029.csv"
    ]
    
    dfs = []
    for f in files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            st.error(f"Error loading {f}: {e}")
            
    if not dfs:
        return pd.DataFrame()
        
    final_df = pd.concat(dfs, ignore_index=True)
    
    # Data Cleaning & Type Conversion
    final_df['date'] = pd.to_datetime(final_df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Ensure numeric columns are strictly numeric
    num_cols = ['age_0_5', 'age_5_17', 'age_18_greater']
    for col in num_cols:
        final_df[col] = pd.to_numeric(final_df[col], errors='coerce').fillna(0)
    
    # Filter out invalid states (e.g., '100000')
    final_df['state'] = final_df['state'].astype(str)
    final_df = final_df[~final_df['state'].str.match(r'^\d+$')]
        
    final_df['Total Enrolments'] = final_df['age_0_5'] + final_df['age_5_17'] + final_df['age_18_greater']
    
    return final_df

df = load_data()

if df.empty:
    st.warning("No data loaded. Please check if the CSV files exist in the same directory.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. Sidebar Filters
# -----------------------------------------------------------------------------
st.sidebar.header("Filter Dashboard")

# Date Filter
min_date = df['date'].min()
max_date = df['date'].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply Date Filter
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    filtered_df = df.loc[mask]
else:
    filtered_df = df.copy()

# State Filter
all_states = sorted(filtered_df['state'].unique().tolist())
selected_states = st.sidebar.multiselect("Select State(s)", all_states, default=all_states[:1] if all_states else None)

if selected_states:
    filtered_df = filtered_df[filtered_df['state'].isin(selected_states)]

# District Filter (Dependent on State)
all_districts = sorted(filtered_df['district'].unique().tolist())
selected_districts = st.sidebar.multiselect("Select District(s)", all_districts)

if selected_districts:
    filtered_df = filtered_df[filtered_df['district'].isin(selected_districts)]

# -----------------------------------------------------------------------------
# 5. Dashboard Main Area
# -----------------------------------------------------------------------------
st.title("🇮🇳 Aadhar Enrolment Analytics Dashboard")
st.markdown("### Interactive insights into enrolment trends across demographics and regions")
st.markdown("---")

# ---- KPIS ----
total_enrolments = filtered_df['Total Enrolments'].sum()
avg_daily = filtered_df.groupby('date')['Total Enrolments'].sum().mean()
top_state = filtered_df.groupby('state')['Total Enrolments'].sum().idxmax() if not filtered_df.empty else "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Enrolments", f"{total_enrolments:,.0f}")
col2.metric("Avg Daily Enrolments", f"{avg_daily:,.0f}")
col3.metric("Top State (Selection)", top_state)
col4.metric("Data Points", f"{len(filtered_df):,.0f}")

st.markdown("---")

# ---- TABS FOR LAYOUT ----
tab1, tab2, tab3 = st.tabs(["📈 Trends & Analysis", "🗺️ Geographic View", "👥 Demographics"])

with tab1:
    st.subheader("Enrolment Trends Over Time")
    
    # Consolidate by date
    daily_trend = filtered_df.groupby('date')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    
    fig_line = px.line(
        daily_trend, 
        x='date', 
        y=['age_0_5', 'age_5_17', 'age_18_greater'],
        title='Daily Enrolments by Age Group',
        labels={'value': 'Enrolments', 'variable': 'Age Group'},
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_line.update_layout(xaxis_title="Date", yaxis_title="Number of Enrolments", hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("State-wise Performance")
    
    state_perf = filtered_df.groupby('state')['Total Enrolments'].sum().reset_index().sort_values('Total Enrolments', ascending=False)
    
    fig_bar = px.bar(
        state_perf,
        x='state',
        y='Total Enrolments',
        color='Total Enrolments',
        title='Total Enrolments by State',
        color_continuous_scale='Viridis',
        text_auto='.2s'
    )
    fig_bar.update_layout(xaxis_title="State", yaxis_title="Total Enrolments")
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed Data Table
    st.expander("View Detailed District Data").dataframe(
        filtered_df.groupby(['state', 'district'])[['age_0_5', 'age_5_17', 'age_18_greater', 'Total Enrolments']].sum().style.background_gradient(cmap="Blues"),
        use_container_width=True
    )

with tab3:
    st.subheader("Demographic Split")
    
    col_demo_1, col_demo_2 = st.columns(2)
    
    # Pie Chart
    total_0_5 = filtered_df['age_0_5'].sum()
    total_5_17 = filtered_df['age_5_17'].sum()
    total_18_plus = filtered_df['age_18_greater'].sum()
    
    labels = ['Age 0-5', 'Age 5-17', 'Age 18+']
    values = [total_0_5, total_5_17, total_18_plus]
    
    fig_pie = px.pie(
        names=labels, 
        values=values, 
        title='Distribution by Age Group',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    col_demo_1.plotly_chart(fig_pie, use_container_width=True)
    
    # Stacked Bar for breakdown comparison (if multiple states selected)
    if len(selected_states) > 0:
        state_breakdown = filtered_df.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
        fig_stack = px.bar(
            state_breakdown,
            x='state',
            y=['age_0_5', 'age_5_17', 'age_18_greater'],
            title='Age Distribution per State',
            barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        col_demo_2.plotly_chart(fig_stack, use_container_width=True)
    else:
        col_demo_2.info("Select specific states in the sidebar to see comparative breakdown here.")

# Footer
st.markdown("---")
st.markdown("© 2026 Aadhar Dashboard Analytics | Created with Streamlit")