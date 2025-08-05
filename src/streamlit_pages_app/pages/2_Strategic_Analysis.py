# pages/2_Strategic_Analysis.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.nuclear_scheduler import StrategicNuclearScheduler
from utils.tech_tree_data import tech_tree

st.set_page_config(
    page_title="Strategic Analysis - Nuclear Investment Analyzer",
    page_icon="🎯",
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
    .highlight-box {
        background-color: #e3f2fd;
        border: 1px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        border: 1px solid #ff9800;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #f3e5f5;
        border: 1px solid #9c27b0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Strategic Long-term Investment Analysis</div>', 
            unsafe_allow_html=True)

st.markdown("""
This analysis calculates the **cumulative long-term impact** of accelerating technologies,
considering compound effects and technology interdependencies over multiple decades.
""")

# Sidebar configuration
with st.sidebar:
    st.header("Analysis Parameters")
    
    investment_year = st.selectbox("Investment Year", range(2025, 2035), index=0)
    
    analysis_horizon = st.selectbox("Analysis Horizon (Years)", [10, 15, 20, 25, 30], index=2)
    
    st.subheader("Advanced Options")
    
    discount_rate = st.slider(
        "Discount Rate", 
        min_value=0.01, 
        max_value=0.10, 
        value=0.05, 
        step=0.01,
        format="%.2f",
        help="Annual discount rate for future energy benefits"
    )
    
    confidence_threshold = st.slider(
        "Minimum Confidence Threshold",
        min_value=0.1,
        max_value=0.9,
        value=0.7,
        step=0.1,
        help="Minimum success probability for technology deployment"
    )
    
    show_zero_impact = st.checkbox("Show Zero Impact Technologies", value=False)

# Initialize strategic scheduler
strategic_scheduler = StrategicNuclearScheduler(tech_tree)

# Run strategic analysis
with st.spinner("Running strategic investment analysis..."):
    try:
        investment_options = strategic_scheduler.find_optimal_long_term_investment(
            current_year=investment_year,
            years_ahead=analysis_horizon
        )
        
        # Separate positive and zero impact options
        positive_options = [opt for opt in investment_options if opt['cumulative_impact_twh'] > 0.001]
        zero_options = [opt for opt in investment_options if opt['cumulative_impact_twh'] <= 0.001]
        
        # Display results
        if positive_options:
            # Executive summary
            best_option = positive_options[0]
            tech_name = strategic_scheduler.nodes[best_option['investment_tech']]['label']
            
            st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
            st.markdown(f"**Recommended Investment**: {tech_name}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Cumulative Impact", f"{best_option['cumulative_impact_twh']:,.0f} TWh")
            with col2:
                st.metric("ROI Multiple", f"{best_option['roi_multiple']:.1f}x")
            with col3:
                st.metric("Baseline Energy", f"{best_option['baseline_twh']:,.0f} TWh")
            with col4:
                st.metric("Accelerated Energy", f"{best_option['accelerated_twh']:,.0f} TWh")
            
            # Investment opportunities table
            st.markdown('<div class="section-header">Top Investment Opportunities</div>', 
                        unsafe_allow_html=True)
            
            # Convert to DataFrame for display
            display_data = []
            for i, option in enumerate(positive_options[:15]):  # Show top 15
                tech_name = strategic_scheduler.nodes[option['investment_tech']]['label']
                display_data.append({
                    'Rank': i + 1,
                    'Technology': tech_name,
                    'Cumulative Impact (TWh)': option['cumulative_impact_twh'],
                    'ROI Multiple': option['roi_multiple'],
                    'Baseline (TWh)': option['baseline_twh'],
                    'Accelerated (TWh)': option['accelerated_twh']
                })
            
            df_display = pd.DataFrame(display_data)
            st.dataframe(
                df_display,
                column_config={
                    "Cumulative Impact (TWh)": st.column_config.NumberColumn(format="%.0f"),
                    "ROI Multiple": st.column_config.NumberColumn(format="%.1f"),
                    "Baseline (TWh)": st.column_config.NumberColumn(format="%.0f"),
                    "Accelerated (TWh)": st.column_config.NumberColumn(format="%.0f"),
                },
                hide_index=True,
                use_container_width=True
            )
            
            # Visualization
            st.markdown('<div class="section-header">Investment Impact Comparison</div>', 
                        unsafe_allow_html=True)
            
            if len(positive_options) > 1:
                # Bar chart of top options
                top_options = positive_options[:10]
                tech_names = [strategic_scheduler.nodes[opt['investment_tech']]['label'][:30] for opt in top_options]
                impacts = [opt['cumulative_impact_twh'] for opt in top_options]
                
                fig = go.Figure(data=[
                    go.Bar(x=impacts, y=tech_names, orientation='h',
                          marker_color='steelblue')
                ])
                fig.update_layout(
                    title='Cumulative Impact of Top Investment Options',
                    xaxis_title='Cumulative Impact (TWh)',
                    height=400,
                    yaxis={'categoryorder':'total ascending'}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # ROI vs Impact scatter plot
                roi_data = []
                for opt in positive_options[:15]:
                    tech_name = strategic_scheduler.nodes[opt['investment_tech']]['label'][:25]
                    roi_data.append({
                        'Technology': tech_name,
                        'ROI Multiple': opt['roi_multiple'],
                        'Cumulative Impact': opt['cumulative_impact_twh'],
                        'Category': strategic_scheduler.nodes[opt['investment_tech']].get('category', 'Other')
                    })
                
                if roi_data:
                    df_roi = pd.DataFrame(roi_data)
                    
                    fig_scatter = px.scatter(df_roi, 
                                           x='ROI Multiple', 
                                           y='Cumulative Impact',
                                           color='Category',
                                           hover_name='Technology',
                                           title='ROI vs Cumulative Impact Analysis')
                    
                    fig_scatter.update_layout(height=400)
                    st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Category analysis
            st.markdown('<div class="section-header">Technology Category Analysis</div>', 
                        unsafe_allow_html=True)
            
            # Group by technology type
            fusion_techs = []
            fission_techs = []
            enabling_techs = []
            
            for option in positive_options:
                tech = strategic_scheduler.nodes[option['investment_tech']]
                if 'Fusion' in tech.get('category', ''):
                    fusion_techs.append(option)
                elif 'Fission' in tech.get('category', ''):
                    fission_techs.append(option)
                else:
                    enabling_techs.append(option)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Fusion Technologies**")
                if fusion_techs:
                    avg_impact = sum(t['cumulative_impact_twh'] for t in fusion_techs) / len(fusion_techs)
                    best_fusion = max(fusion_techs, key=lambda x: x['cumulative_impact_twh'])
                    best_fusion_name = strategic_scheduler.nodes[best_fusion['investment_tech']]['label'][:20]
                    
                    st.metric("Count", len(fusion_techs))
                    st.metric("Avg Impact", f"{avg_impact:.0f} TWh")
                    st.metric("Best Option", f"{best_fusion['cumulative_impact_twh']:.0f} TWh")
                    st.caption(f"Best: {best_fusion_name}")
                else:
                    st.info("No viable fusion options")
            
            with col2:
                st.markdown("**Fission Technologies**")
                if fission_techs:
                    avg_impact = sum(t['cumulative_impact_twh'] for t in fission_techs) / len(fission_techs)
                    best_fission = max(fission_techs, key=lambda x: x['cumulative_impact_twh'])
                    best_fission_name = strategic_scheduler.nodes[best_fission['investment_tech']]['label'][:20]
                    
                    st.metric("Count", len(fission_techs))
                    st.metric("Avg Impact", f"{avg_impact:.0f} TWh")
                    st.metric("Best Option", f"{best_fission['cumulative_impact_twh']:.0f} TWh")
                    st.caption(f"Best: {best_fission_name}")
                else:
                    st.info("No viable fission options")
            
            with col3:
                st.markdown("**Enabling Technologies**")
                if enabling_techs:
                    avg_impact = sum(t['cumulative_impact_twh'] for t in enabling_techs) / len(enabling_techs)
                    best_enabling = max(enabling_techs, key=lambda x: x['cumulative_impact_twh'])
                    best_enabling_name = strategic_scheduler.nodes[best_enabling['investment_tech']]['label'][:20]
                    
                    st.metric("Count", len(enabling_techs))
                    st.metric("Avg Impact", f"{avg_impact:.0f} TWh")
                    st.metric("Best Option", f"{best_enabling['cumulative_impact_twh']:.0f} TWh")
                    st.caption(f"Best: {best_enabling_name}")
                else:
                    st.info("No viable enabling options")
            
            # Portfolio analysis
            st.markdown('<div class="section-header">Portfolio Optimization</div>', 
                        unsafe_allow_html=True)
            
            st.markdown("""
            **Investment Strategy Recommendations:**
            """)
            
            # Calculate portfolio metrics
            total_impact = sum(opt['cumulative_impact_twh'] for opt in positive_options[:5])
            avg_roi = sum(opt['roi_multiple'] for opt in positive_options[:5]) / min(5, len(positive_options))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Top 5 Combined Impact", f"{total_impact:,.0f} TWh")
            with col2:
                st.metric("Average ROI (Top 5)", f"{avg_roi:.1f}x")
            
            # Risk-adjusted recommendations
            high_impact_low_risk = [opt for opt in positive_options 
                                  if opt['cumulative_impact_twh'] > 100 and opt['roi_multiple'] > 2.0]
            
            if high_impact_low_risk:
                st.markdown("**High Impact, High ROI Opportunities:**")
                for i, opt in enumerate(high_impact_low_risk[:3]):
                    tech_name = strategic_scheduler.nodes[opt['investment_tech']]['label']
                    st.write(f"{i+1}. {tech_name} - {opt['cumulative_impact_twh']:.0f} TWh ({opt['roi_multiple']:.1f}x ROI)")
        
        else:
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("**Warning**: No technologies show positive long-term impact in the selected timeframe.")
            st.markdown("This might indicate that most technologies are not currently ready for acceleration or are blocked by prerequisites.")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show zero impact technologies if requested
        if show_zero_impact and zero_options:
            st.markdown('<div class="section-header">Zero Impact Analysis</div>', 
                        unsafe_allow_html=True)
            
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown(f"""
            **{len(zero_options)} technologies show zero long-term impact**, likely because they are:
            
            - Not currently active or ready for acceleration
            - Blocked by incomplete prerequisite technologies
            - Not on the critical path to reactor deployment
            - Outside the selected analysis time horizon
            - Below the confidence threshold for deployment
            """)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show examples
            zero_tech_names = [strategic_scheduler.nodes[opt['investment_tech']]['label'] for opt in zero_options[:10]]
            
            st.markdown("**Examples of zero-impact technologies:**")
            for i, name in enumerate(zero_tech_names):
                st.write(f"{i+1}. {name}")
            
            if len(zero_options) > 10:
                st.write(f"... and {len(zero_options) - 10} more")
    
    except Exception as e:
        st.error(f"Error running strategic analysis: {str(e)}")
        st.info("Please check the configuration parameters and try again.")

# Key insights
st.markdown('<div class="section-header">Key Insights</div>', 
            unsafe_allow_html=True)

st.markdown("""
**Understanding Strategic vs Short-term Impact:**

1. **Cumulative Effects**: Strategic analysis captures compound benefits that accrue over decades, revealing technologies with high long-term value despite low immediate impact.

2. **Technology Interdependencies**: Some technologies unlock entire pathways - their strategic value comes from enabling multiple downstream innovations.

3. **Timing Considerations**: Early investment in foundational technologies can yield exponentially higher returns than later-stage investments.

4. **Portfolio Approach**: Diversifying across fusion, fission, and enabling technologies reduces risk while maximizing expected returns.

5. **ROI Analysis**: Technologies with ROI multiples above 3x represent exceptional investment opportunities with high confidence.
""")