# app.py - Main Streamlit application
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.nuclear_scheduler import NuclearScheduler, StrategicNuclearScheduler
from utils.tech_tree_data import tech_tree
import json

# Page configuration
st.set_page_config(
    page_title="Nuclear Technology Investment Analyzer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 20px;
        background-color: #f0f2f6;
        border-radius: 10px 10px 0px 0px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title
    st.markdown('<div class="main-header">⚛️ Nuclear Technology Investment Analyzer</div>', 
                unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Global parameters
        st.subheader("Simulation Parameters")
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
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Year-by-Year Impact Analysis", 
        "🎯 Strategic Investment Analysis",
        "📈 Technology Comparison"
    ])
    
    with tab1:
        show_yearly_analysis(simulation_years, discount_rate, capacity_factor, avg_plant_size)
    
    with tab2:
        show_strategic_analysis(simulation_years, discount_rate, capacity_factor, avg_plant_size)
    
    with tab3:
        show_technology_comparison(simulation_years, discount_rate, capacity_factor, avg_plant_size)

def show_yearly_analysis(simulation_years, discount_rate, capacity_factor, avg_plant_size):
    """Show the original year-by-year impact heatmap analysis."""
    
    st.header("📊 Year-by-Year Technology Impact Analysis")
    st.markdown("""
    This analysis shows the **immediate impact** of accelerating each technology by one year 
    in each specific year. The impact is measured in additional clean energy (TWh) generated 
    over the technology's lifetime.
    """)
    
    # Initialize scheduler with updated parameters
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
    st.subheader("🔥 Technology Impact Heatmap")
    
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
            st.subheader("📋 Top Investment Opportunities by Year")
            
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

def show_strategic_analysis(simulation_years, discount_rate, capacity_factor, avg_plant_size):
    """Show the strategic long-term investment analysis."""
    
    st.header("🎯 Strategic Long-term Investment Analysis")
    st.markdown("""
    This analysis calculates the **cumulative long-term impact** of accelerating technologies,
    considering compound effects and technology interdependencies over multiple decades.
    """)
    
    # Parameters for strategic analysis
    col1, col2 = st.columns(2)
    with col1:
        investment_year = st.selectbox("Investment Year", range(2025, 2035), index=0)
    with col2:
        analysis_horizon = st.selectbox("Analysis Horizon (Years)", [10, 15, 20, 25, 30], index=2)
    
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
                
                st.success(f"🎯 **Recommended Investment**: {tech_name}")
                
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
                st.subheader("📋 Top Investment Opportunities")
                
                # Convert to DataFrame for display
                display_data = []
                for i, option in enumerate(positive_options[:10]):
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
                st.subheader("📊 Investment Impact Comparison")
                
                if len(positive_options) > 1:
                    # Bar chart of top options
                    top_options = positive_options[:8]
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
                
                # Category analysis
                st.subheader("🔍 Technology Category Analysis")
                
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
                    st.markdown("**🔥 Fusion Technologies**")
                    if fusion_techs:
                        avg_impact = sum(t['cumulative_impact_twh'] for t in fusion_techs) / len(fusion_techs)
                        st.metric("Count", len(fusion_techs))
                        st.metric("Avg Impact", f"{avg_impact:.0f} TWh")
                    else:
                        st.info("No viable fusion options")
                
                with col2:
                    st.markdown("**⚛️ Fission Technologies**")
                    if fission_techs:
                        avg_impact = sum(t['cumulative_impact_twh'] for t in fission_techs) / len(fission_techs)
                        st.metric("Count", len(fission_techs))
                        st.metric("Avg Impact", f"{avg_impact:.0f} TWh")
                    else:
                        st.info("No viable fission options")
                
                with col3:
                    st.markdown("**🔧 Enabling Technologies**")
                    if enabling_techs:
                        avg_impact = sum(t['cumulative_impact_twh'] for t in enabling_techs) / len(enabling_techs)
                        st.metric("Count", len(enabling_techs))
                        st.metric("Avg Impact", f"{avg_impact:.0f} TWh")
                    else:
                        st.info("No viable enabling options")
            
            else:
                st.warning("⚠️ No technologies show positive long-term impact in the selected timeframe.")
                st.info("This might indicate that most technologies are not currently ready for acceleration or are blocked by prerequisites.")
            
            # Show zero impact technologies
            if zero_options:
                with st.expander(f"ℹ️ Technologies with Zero Impact ({len(zero_options)} total)"):
                    st.markdown("""
                    These technologies show no measurable long-term impact, likely because they are:
                    * Not currently active/ready for acceleration
                    * Blocked by incomplete prerequisites
                    * Not on the critical path to reactor deployment
                    * Outside the simulation time horizon
                    """)
                    
                    zero_tech_names = [strategic_scheduler.nodes[opt['investment_tech']]['label'] for opt in zero_options[:10]]
                    for name in zero_tech_names:
                        st.write(f"• {name}")
                    
                    if len(zero_options) > 10:
                        st.write(f"... and {len(zero_options) - 10} more")
        
        except Exception as e:
            st.error(f"Error running strategic analysis: {str(e)}")
            st.info("This feature requires the full strategic scheduler implementation.")

def show_technology_comparison(simulation_years, discount_rate, capacity_factor, avg_plant_size):
    """Show detailed technology comparison and pathway analysis."""
    
    st.header("📈 Technology Pathway Comparison")
    st.markdown("""
    Compare different nuclear technology pathways and their deployment timelines, 
    success probabilities, and energy production potential.
    """)
    
    # Initialize scheduler
    scheduler = NuclearScheduler(tech_tree)
    
    # Get technology information
    fusion_concepts = []
    fission_concepts = []
    
    for node_id, node in scheduler.nodes.items():
        if node.get('type') == 'ReactorConcept':
            if 'Fusion' in node.get('category', ''):
                fusion_concepts.append((node_id, node))
            elif 'Fission' in node.get('category', ''):
                fission_concepts.append((node_id, node))
    
    # Technology pathway visualization
    st.subheader("🛤️ Technology Deployment Pathways")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔥 Fusion Pathways**")
        if fusion_concepts:
            fusion_data = []
            for node_id, node in fusion_concepts:
                # Calculate critical path
                try:
                    time_to_deploy, success_prob = scheduler._find_critical_path(node_id, scheduler.nodes)
                    deployment_year = 2025 + time_to_deploy
                    
                    fusion_data.append({
                        'Technology': node['label'],
                        'Current TRL': node.get('trl_current', 'Unknown'),
                        'Deployment Year': f"{deployment_year:.0f}" if deployment_year != float('inf') else "TBD",
                        'Success Probability': f"{success_prob:.1%}",
                        'Time to Deploy': f"{time_to_deploy:.1f} years" if time_to_deploy != float('inf') else "TBD"
                    })
                except:
                    fusion_data.append({
                        'Technology': node['label'],
                        'Current TRL': node.get('trl_current', 'Unknown'),
                        'Deployment Year': "Error",
                        'Success Probability': "Error",
                        'Time to Deploy': "Error"
                    })
            
            df_fusion = pd.DataFrame(fusion_data)
            st.dataframe(df_fusion, hide_index=True, use_container_width=True)
        else:
            st.info("No fusion concepts found in the technology tree")
    
    with col2:
        st.markdown("**⚛️ Fission Pathways**")
        if fission_concepts:
            fission_data = []
            for node_id, node in fission_concepts:
                # Calculate critical path
                try:
                    time_to_deploy, success_prob = scheduler._find_critical_path(node_id, scheduler.nodes)
                    deployment_year = 2025 + time_to_deploy
                    
                    fission_data.append({
                        'Technology': node['label'],
                        'Current TRL': node.get('trl_current', 'Unknown'),
                        'Deployment Year': f"{deployment_year:.0f}" if deployment_year != float('inf') else "TBD",
                        'Success Probability': f"{success_prob:.1%}",
                        'Time to Deploy': f"{time_to_deploy:.1f} years" if time_to_deploy != float('inf') else "TBD"
                    })
                except:
                    fission_data.append({
                        'Technology': node['label'],
                        'Current TRL': node.get('trl_current', 'Unknown'),
                        'Deployment Year': "Error",
                        'Success Probability': "Error",
                        'Time to Deploy': "Error"
                    })
            
            df_fission = pd.DataFrame(fission_data)
            st.dataframe(df_fission, hide_index=True, use_container_width=True)
        else:
            st.info("No fission concepts found in the technology tree")
    
    # Timeline visualization
    st.subheader("📅 Technology Deployment Timeline")
    
    # Prepare timeline data
    timeline_data = []
    all_concepts = fusion_concepts + fission_concepts
    
    for node_id, node in all_concepts:
        try:
            time_to_deploy, success_prob = scheduler._find_critical_path(node_id, scheduler.nodes)
            if time_to_deploy != float('inf'):
                deployment_year = 2025 + time_to_deploy
                timeline_data.append({
                    'Technology': node['label'][:25] + ('...' if len(node['label']) > 25 else ''),
                    'Deployment Year': deployment_year,
                    'Success Probability': success_prob,
                    'Category': node.get('category', 'Unknown'),
                    'TRL': node.get('trl_current', 'Unknown')
                })
        except:
            continue
    
    if timeline_data:
        df_timeline = pd.DataFrame(timeline_data)
        
        # Create timeline chart
        fig = px.scatter(df_timeline, 
                        x='Deployment Year', 
                        y='Technology',
                        size='Success Probability',
                        color='Category',
                        hover_data=['TRL', 'Success Probability'],
                        title='Nuclear Technology Deployment Timeline')
        
        fig.update_layout(
            height=max(400, len(timeline_data) * 30),
            yaxis={'categoryorder':'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("📊 Portfolio Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_deployment = df_timeline['Deployment Year'].mean()
            st.metric("Average Deployment Year", f"{avg_deployment:.0f}")
        
        with col2:
            avg_success = df_timeline['Success Probability'].mean()
            st.metric("Average Success Probability", f"{avg_success:.1%}")
        
        with col3:
            earliest_deployment = df_timeline['Deployment Year'].min()
            st.metric("Earliest Deployment", f"{earliest_deployment:.0f}")
        
        with col4:
            high_prob_count = len(df_timeline[df_timeline['Success Probability'] > 0.7])
            st.metric("High Confidence Technologies", high_prob_count)
    
    else:
        st.warning("Unable to generate timeline data. Please check the technology dependencies.")

if __name__ == "__main__":
    main()