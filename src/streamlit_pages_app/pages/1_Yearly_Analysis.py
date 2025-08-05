# pages/1_Yearly_Analysis.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.nuclear_scheduler import NuclearScheduler
from utils.tech_tree_data import tech_tree

st.set_page_config(
    page_title="Yearly Analysis - Nuclear Investment Analyzer",
    page_icon="📊",
    layout="wide"
)

# Apply the same CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        border-left: 4px solid #1f77b4;
        padding-left: 1rem;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Year-by-Year Technology Impact Analysis</div>', 
            unsafe_allow_html=True)

st.markdown("""
This analysis shows the **immediate impact** of accelerating each technology by one year 
in each specific year. The impact is measured in additional clean energy (TWh) generated 
over the technology's lifetime.
""")

# Sidebar configuration
with st.sidebar:
    st.header("Simulation Parameters")
    
    simulation_years = st.slider(
        "Simulation Years", 
        min_value=10, 
        max_value=50, 
        value=30,
        help="Number of years to simulate forward"
    )
    
    discount_rate = st.slider(
        "Discount Rate", 
        min_value=0.01, 
        max_value=0.10, 
        value=0.05, 
        step=0.01,
        format="%.2f",
        help="Annual discount rate for future energy benefits"
    )
    
    st.subheader("Model Assumptions")
    capacity_factor = st.slider(
        "Plant Capacity Factor", 
        min_value=0.70, 
        max_value=0.95, 
        value=0.90,
        step=0.01,
        help="Average capacity factor for nuclear plants"
    )
    
    avg_plant_size = st.slider(
        "Average Plant Size (MW)", 
        min_value=300, 
        max_value=1500, 
        value=1000,
        step=50,
        help="Average capacity of deployed nuclear plants"
    )

# Initialize scheduler
scheduler = NuclearScheduler(tech_tree)

# Run simulation
with st.spinner("Running year-by-year simulation..."):
    impact_data, status_data = scheduler.run_simulation(years_to_simulate=simulation_years)

# Create metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_techs = len(impact_data.keys())
    st.metric("Technologies Analyzed", total_techs)

with col2:
    active_techs = sum(1 for tech_data in impact_data.values() if any(impact > 0 for impact in tech_data.values()))
    st.metric("Technologies with Positive Impact", active_techs)

with col3:
    max_impact = max((max(yearly_impacts.values()) for yearly_impacts in impact_data.values() if yearly_impacts), default=0)
    st.metric("Maximum Single-Year Impact", f"{max_impact:.1f} TWh")

with col4:
    current_year = 2025
    current_opportunities = sum(1 for tech_data in impact_data.values() if tech_data.get(current_year, 0) > 0)
    st.metric(f"Investment Opportunities in {current_year}", current_opportunities)

# Heatmap visualization
st.markdown('<div class="section-header">Technology Impact Heatmap</div>', 
            unsafe_allow_html=True)

# Prepare heatmap data
heatmap_data = []
for tech, yearly_impact in impact_data.items():
    for year, impact in yearly_impact.items():
        heatmap_data.append([tech, int(year), impact])

if heatmap_data:
    df = pd.DataFrame(heatmap_data, columns=['Technology', 'Year', 'Impact (TWh)'])
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        min_impact = st.slider("Minimum Impact to Display (TWh)", 0.0, 5.0, 0.1, 0.1)
    with col2:
        show_all_techs = st.checkbox("Show All Technologies", value=False)
    
    # Filter data
    filtered_df = df[df['Impact (TWh)'] >= min_impact]
    
    if not show_all_techs and len(filtered_df) > 0:
        # Show only top technologies by maximum impact
        tech_max_impacts = filtered_df.groupby('Technology')['Impact (TWh)'].max().sort_values(ascending=False)
        top_techs = tech_max_impacts.head(15).index.tolist()
        filtered_df = filtered_df[filtered_df['Technology'].isin(top_techs)]
    
    if len(filtered_df) > 0:
        # Create pivot table for heatmap
        pivot_df = filtered_df.pivot_table(
            index='Technology', 
            columns='Year', 
            values='Impact (TWh)', 
            fill_value=0
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Viridis',
            colorbar=dict(title='Impact (TWh)'),
            hoverongaps=False,
            hovertemplate='Year: %{x}<br>Technology: %{y}<br>Impact: %{z:.2f} TWh<extra></extra>'
        ))
        
        fig.update_layout(
            title='Technology Acceleration Impact by Year',
            xaxis_title='Year',
            yaxis_title='Technology',
            height=max(400, len(pivot_df.index) * 25),
            yaxis=dict(autorange='reversed'),
            font=dict(size=10)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary table
        st.markdown('<div class="section-header">Investment Opportunities by Year</div>', 
                    unsafe_allow_html=True)
        
        # Let user select a year
        available_years = sorted(df['Year'].unique())
        selected_year = st.selectbox("Select Year for Detailed Analysis", available_years, 
                                   index=0 if available_years else 0)
        
        if selected_year:
            year_data = df[df['Year'] == selected_year].sort_values('Impact (TWh)', ascending=False)
            year_data = year_data[year_data['Impact (TWh)'] > 0].head(10)
            
            if len(year_data) > 0:
                st.dataframe(
                    year_data.reset_index(drop=True),
                    column_config={
                        "Technology": st.column_config.TextColumn("Technology", width="large"),
                        "Impact (TWh)": st.column_config.NumberColumn("Impact (TWh)", format="%.2f"),
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info(f"No investment opportunities with positive impact in {selected_year}")
    else:
        st.warning("No technologies meet the minimum impact threshold. Try lowering the minimum impact filter.")
else:
    st.error("No simulation data generated. Please check the configuration.")

# Additional analysis section
st.markdown('<div class="section-header">Technology Status Overview</div>', 
            unsafe_allow_html=True)

# Show technology status distribution
if status_data:
    status_summary = {}
    current_year = 2025
    
    for tech_name, yearly_status in status_data.items():
        current_status = yearly_status.get(current_year, "Unknown")
        if current_status not in status_summary:
            status_summary[current_status] = 0
        status_summary[current_status] += 1
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        active_count = status_summary.get("Active", 0)
        st.metric("Currently Active Technologies", active_count)
    
    with col2:
        pending_count = status_summary.get("Pending", 0)
        st.metric("Pending Technologies", pending_count)
    
    with col3:
        completed_count = status_summary.get("Completed", 0)
        st.metric("Completed Technologies", completed_count)
    
    # Show status breakdown
    if status_summary:
        st.subheader("Technology Status Breakdown")
        status_df = pd.DataFrame(list(status_summary.items()), columns=['Status', 'Count'])
        
        fig = go.Figure(data=[
            go.Bar(x=status_df['Status'], y=status_df['Count'], 
                   marker_color=['#2ecc71' if s == 'Active' else '#f39c12' if s == 'Pending' else '#95a5a6' 
                                for s in status_df['Status']])
        ])
        fig.update_layout(
            title=f'Technology Status Distribution in {current_year}',
            xaxis_title='Status',
            yaxis_title='Number of Technologies',
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)

# Key insights
st.markdown('<div class="section-header">Key Insights</div>', 
            unsafe_allow_html=True)

st.markdown("""
**Understanding the Results:**

1. **Active Technologies**: These are ready for acceleration investment and show immediate impact when funded.

2. **Pending Technologies**: Waiting for prerequisite technologies to complete before they can begin development.

3. **Impact Timing**: The heatmap shows when each technology investment would have maximum impact - this varies based on technology readiness and market conditions.

4. **Investment Strategy**: Focus on technologies that are currently active and show high impact values in near-term years for immediate returns.
""")