# app.py - Main Streamlit application (Home page)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.nuclear_scheduler import NuclearScheduler, StrategicNuclearScheduler
from utils.tech_tree_data import tech_tree

# Page configuration
st.set_page_config(
    page_title="Nuclear Technology Investment Analyzer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
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
    .info-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .feature-box {
        background-color: #ffffff;
        border: 2px solid #e9ecef;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .navigation-card {
        background-color: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    .metric-highlight {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title
    st.markdown('<div class="main-header">Nuclear Technology Investment Analyzer</div>', 
                unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    **A comprehensive analysis platform for nuclear technology R&D investment decisions**
    
    This application provides data-driven insights to optimize nuclear technology investment strategies, 
    combining short-term impact analysis with long-term strategic planning.
    """)
    
    # Navigation cards
    st.markdown('<div class="section-header">Analysis Modules</div>', 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="navigation-card">', unsafe_allow_html=True)
        st.markdown("### Yearly Analysis")
        st.markdown("""
        **Year-by-Year Impact Assessment**
        
        Analyze the immediate impact of accelerating each technology by one year. 
        Features interactive heatmaps and timeline analysis.
        
        - Technology impact heatmaps
        - Investment opportunity identification
        - Status tracking across years
        - Filtering and visualization tools
        """)
        st.markdown("**→ Go to: Pages > 1_Yearly_Analysis**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="navigation-card">', unsafe_allow_html=True)
        st.markdown("### Strategic Analysis")
        st.markdown("""
        **Long-term Cumulative Impact**
        
        Calculate compound effects and technology interdependencies over decades 
        to identify high-value strategic investments.
        
        - Cumulative impact modeling
        - ROI multiple calculations
        - Portfolio optimization
        - Risk-adjusted returns
        """)
        st.markdown("**→ Go to: Pages > 2_Strategic_Analysis**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="navigation-card">', unsafe_allow_html=True)
        st.markdown("### Technology Comparison")
        st.markdown("""
        **Pathway & Timeline Analysis**
        
        Compare nuclear technology pathways, deployment timelines, and 
        success probabilities across fusion and fission options.
        
        - Technology pathway comparison
        - Deployment timeline visualization
        - Risk-return analysis
        - Dependency mapping
        """)
        st.markdown("**→ Go to: Pages > 3_Technology_Comparison**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick overview
    st.markdown('<div class="section-header">Technology Portfolio Overview</div>', 
                unsafe_allow_html=True)
    
    # Initialize scheduler for overview
    scheduler = NuclearScheduler(tech_tree)
    
    # Count technologies by type
    fusion_count = len([n for n in scheduler.nodes.values() if n.get('category') == 'Fusion'])
    fission_count = len([n for n in scheduler.nodes.values() if n.get('category') == 'Fission'])
    milestone_count = len([n for n in scheduler.nodes.values() if n.get('type') == 'Milestone'])
    enabling_count = len([n for n in scheduler.nodes.values() if n.get('type') == 'EnablingTechnology'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Fusion Technologies", fusion_count)
    with col2:
        st.metric("Fission Technologies", fission_count)
    with col3:
        st.metric("Key Milestones", milestone_count)
    with col4:
        st.metric("Enabling Technologies", enabling_count)
    
    # Technology distribution chart
    tech_data = {
        'Technology Type': ['Fusion Concepts', 'Fission Concepts', 'Milestones', 'Enabling Technologies'],
        'Count': [fusion_count, fission_count, milestone_count, enabling_count]
    }
    
    df_tech = pd.DataFrame(tech_data)
    
    fig = px.bar(df_tech, x='Technology Type', y='Count',
                 title='Nuclear Technology Portfolio Composition',
                 color='Technology Type',
                 color_discrete_sequence=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
    
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Key features
    st.markdown('<div class="section-header">Key Features</div>', 
                unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("### Advanced Modeling")
        st.markdown("""
        - **Critical Path Analysis**: Identifies bottleneck technologies
        - **TRL-based Risk Assessment**: Success probabilities based on technology readiness
        - **Dependency Mapping**: Models technology interdependencies
        - **NPV Calculations**: Discounted cash flow analysis for energy benefits
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("### Interactive Analysis")
        st.markdown("""
        - **Configurable Parameters**: Adjust discount rates, timelines, and assumptions
        - **Dynamic Filtering**: Focus on specific technology types or timeframes
        - **Scenario Modeling**: Compare baseline vs accelerated development paths
        - **Visual Analytics**: Interactive charts and heatmaps
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Methodology overview
    st.markdown('<div class="section-header">Methodology</div>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### Analysis Framework
    
    **1. Technology Readiness Assessment**
    - Current TRL (Technology Readiness Level) evaluation
    - Success probability mapping based on historical data
    - Time-to-deployment estimates using industry benchmarks
    
    **2. Impact Calculation**
    - Energy production potential (TWh over plant lifetime)
    - Net present value analysis with configurable discount rates
    - Compound effect modeling for strategic technologies
    
    **3. Risk Analysis**
    - Technology development risk assessment
    - Market deployment probability calculations
    - Portfolio risk diversification analysis
    
    **4. Investment Optimization**
    - ROI multiple calculations
    - Short-term vs long-term impact comparison
    - Strategic pathway identification
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data sources and assumptions
    with st.expander("Data Sources and Key Assumptions"):
        st.markdown("""
        ### Data Sources
        - Public roadmaps from major nuclear programs (ITER, private fusion companies)
        - Academic literature on advanced reactor development
        - Industry TRL assessments and expert evaluations
        - Historical technology development timelines
        
        ### Key Assumptions
        - **Average Plant Capacity**: 1,000 MW (configurable: 300-1,500 MW)
        - **Capacity Factor**: 90% (configurable: 70-95%)
        - **Plant Lifetime**: 60 years
        - **Discount Rate**: 5% annually (configurable: 1-10%)
        - **Deployment Threshold**: 70% success probability for commercial deployment
        
        ### Model Limitations
        - Simplified dependency modeling (linear relationships)
        - Does not account for policy/regulatory changes
        - Limited modeling of market competition effects
        - Assumes deterministic outcomes above probability thresholds
        """)
    
    # Getting started
    st.markdown('<div class="section-header">Getting Started</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    ### Quick Start Guide
    
    1. **For immediate impact analysis**: Start with the **Yearly Analysis** page to see which technologies offer the best near-term investment opportunities.
    
    2. **For strategic planning**: Use the **Strategic Analysis** page to identify technologies with high long-term cumulative impact.
    
    3. **For technology comparison**: Visit the **Technology Comparison** page to compare different nuclear pathways and their risk-return profiles.
    
    ### Configuration Tips
    - Adjust the simulation parameters in the sidebar of each page
    - Use filters to focus on specific technology categories
    - Compare different scenarios by changing discount rates and timelines
    - Export data using the download buttons (where available)
    """)

if __name__ == "__main__":
    main()