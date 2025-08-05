# pages/3_Technology_Comparison.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
from utils.nuclear_scheduler import NuclearScheduler
from utils.tech_tree_data import tech_tree

st.set_page_config(
    page_title="Technology Comparison - Nuclear Investment Analyzer",
    page_icon="📈",
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
    .comparison-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    .pathway-box {
        background-color: #ffffff;
        border: 2px solid #1f77b4;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .tech-category {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    .risk-low { background-color: #d4edda; border-left: 4px solid #28a745; }
    .risk-medium { background-color: #fff3cd; border-left: 4px solid #ffc107; }
    .risk-high { background-color: #f8d7da; border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">Technology Pathway Comparison</div>', 
            unsafe_allow_html=True)

st.markdown("""
Compare different nuclear technology pathways and their deployment timelines, 
success probabilities, and energy production potential.
""")

# Sidebar configuration
with st.sidebar:
    st.header("Analysis Options")
    
    pathway_filter = st.selectbox(
        "Focus on Technology Type",
        ["All Technologies", "Fusion Only", "Fission Only", "Enabling Technologies Only"]
    )
    
    timeline_range = st.slider("Timeline Range (Years from 2025)", 5, 30, (5, 20))
    
    min_success_prob = st.slider(
        "Minimum Success Probability",
        0.0, 1.0, 0.3, 0.1,
        help="Filter technologies by minimum success probability"
    )
    
    st.subheader("Display Options")
    
    show_trl_info = st.checkbox("Show TRL Information", value=True)
    show_dependencies = st.checkbox("Show Technology Dependencies", value=False)
    group_by_category = st.checkbox("Group by Technology Category", value=True)
    show_detailed_metrics = st.checkbox("Show Detailed Metrics", value=False)

# Initialize scheduler
scheduler = NuclearScheduler(tech_tree)

# Get technology information
fusion_concepts = []
fission_concepts = []
enabling_techs = []
milestones = []

for node_id, node in scheduler.nodes.items():
    if node.get('type') == 'ReactorConcept':
        if 'Fusion' in node.get('category', ''):
            fusion_concepts.append((node_id, node))
        elif 'Fission' in node.get('category', ''):
            fission_concepts.append((node_id, node))
    elif node.get('type') == 'EnablingTechnology':
        enabling_techs.append((node_id, node))
    elif node.get('type') == 'Milestone':
        milestones.append((node_id, node))

# Filter based on selection
if pathway_filter == "Fusion Only":
    concepts_to_show = fusion_concepts
    title_suffix = " (Fusion Technologies)"
elif pathway_filter == "Fission Only":
    concepts_to_show = fission_concepts
    title_suffix = " (Fission Technologies)"
elif pathway_filter == "Enabling Technologies Only":
    concepts_to_show = enabling_techs
    title_suffix = " (Enabling Technologies)"
else:
    concepts_to_show = fusion_concepts + fission_concepts
    title_suffix = ""

# Technology pathway analysis
st.markdown(f'<div class="section-header">Technology Deployment Pathways{title_suffix}</div>', 
            unsafe_allow_html=True)

if pathway_filter != "Enabling Technologies Only":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="pathway-box">', unsafe_allow_html=True)
        st.markdown("**Fusion Pathways**")
        if fusion_concepts and (pathway_filter in ["All Technologies", "Fusion Only"]):
            fusion_data = []
            for node_id, node in fusion_concepts:
                try:
                    time_to_deploy, success_prob = scheduler._find_critical_path(node_id, scheduler.nodes)
                    if success_prob >= min_success_prob:
                        deployment_year = 2025 + time_to_deploy
                        
                        row_data = {
                            'Technology': node['label'],
                            'Current TRL': node.get('trl_current', 'Unknown'),
                            'Deployment Year': f"{deployment_year:.0f}" if deployment_year != float('inf') else "TBD",
                            'Success Probability': f"{success_prob:.1%}",
                            'Time to Deploy': f"{time_to_deploy:.1f} years" if time_to_deploy != float('inf') else "TBD"
                        }
                        
                        if show_detailed_metrics:
                            # Calculate potential energy output
                            annual_twh = 7.9  # Approximate TWh per year for 1GW plant at 90% capacity
                            lifetime_twh = annual_twh * 60 * success_prob  # 60-year lifetime
                            row_data['Potential Output (TWh)'] = f"{lifetime_twh:.0f}"
                            
                        fusion_data.append(row_data)
                except:
                    continue
            
            if fusion_data:
                df_fusion = pd.DataFrame(fusion_data)
                st.dataframe(df_fusion, hide_index=True, use_container_width=True)
                
                # Summary metrics for fusion
                if show_detailed_metrics and len(fusion_data) > 0:
                    avg_prob = df_fusion['Success Probability'].str.rstrip('%').astype(float).mean() / 100
                    st.caption(f"Average Success Probability: {avg_prob:.1%}")
            else:
                st.info("No fusion technologies meet the criteria")
        else:
            st.info("No fusion concepts to display")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="pathway-box">', unsafe_allow_html=True)
        st.markdown("**Fission Pathways**")
        if fission_concepts and (pathway_filter in ["All Technologies", "Fission Only"]):
            fission_data = []
            for node_id, node in fission_concepts:
                try:
                    time_to_deploy, success_prob = scheduler._find_critical_path(node_id, scheduler.nodes)
                    if success_prob >= min_success_prob:
                        deployment_year = 2025 + time_to_deploy
                        
                        row_data = {
                            'Technology': node['label'],
                            'Current TRL': node.get('trl_current', 'Unknown'),
                            'Deployment Year': f"{deployment_year:.0f}" if deployment_year != float('inf') else "TBD",
                            'Success Probability': f"{success_prob:.1%}",
                            'Time to Deploy': f"{time_to_deploy:.1f} years" if time_to_deploy != float('inf') else "TBD"
                        }
                        
                        if show_detailed_metrics:
                            annual_twh = 7.9  # Same assumption
                            lifetime_twh = annual_twh * 60 * success_prob
                            row_data['Potential Output (TWh)'] = f"{lifetime_twh:.0f}"
                            
                        fission_data.append(row_data)
                except:
                    continue
            
            if fission_data:
                df_fission = pd.DataFrame(fission_data)
                st.dataframe(df_fission, hide_index=True, use_container_width=True)
                
                # Summary metrics for fission
                if show_detailed_metrics and len(fission_data) > 0:
                    avg_prob = df_fission['Success Probability'].str.rstrip('%').astype(float).mean() / 100
                    st.caption(f"Average Success Probability: {avg_prob:.1%}")
            else:
                st.info("No fission technologies meet the criteria")
        else:
            st.info("No fission concepts to display")
        st.markdown('</div>', unsafe_allow_html=True)

# Enabling technologies section
if pathway_filter in ["All Technologies", "Enabling Technologies Only"]:
    st.markdown('<div class="section-header">Enabling Technologies Analysis</div>', 
                unsafe_allow_html=True)
    
    enabling_data = []
    for node_id, node in enabling_techs:
        try:
            # For enabling technologies, calculate their readiness rather than deployment
            trl_current = node.get('trl_current', 'Unknown')
            
            # Estimate completion time based on TRL
            if 'trl_projected_5_10_years' in node:
                completion_time = 7.5
            else:
                try:
                    trl_val = float(str(trl_current).split('-')[0].split(' ')[0])
                    completion_time = max(1, (9 - trl_val) * 1.5)  # Faster for enabling techs
                except:
                    completion_time = 5.0
            
            # Calculate success probability
            success_prob = scheduler._get_initial_prob(node)
            
            if success_prob >= min_success_prob:
                # Determine priority based on success probability and completion time
                if success_prob > 0.7 and completion_time < 5:
                    priority = 'High'
                elif success_prob > 0.5 and completion_time < 8:
                    priority = 'Medium'
                else:
                    priority = 'Low'
                
                row_data = {
                    'Technology': node['label'],
                    'Current TRL': trl_current,
                    'Completion Year': f"{2025 + completion_time:.0f}",
                    'Success Probability': f"{success_prob:.1%}",
                    'Time to Complete': f"{completion_time:.1f} years",
                    'Priority': priority
                }
                
                if show_detailed_metrics:
                    # Count how many reactor concepts this enables
                    enabled_concepts = len(scheduler._get_downstream_concepts(node_id))
                    row_data['Enables Concepts'] = enabled_concepts
                    
                enabling_data.append(row_data)
        except:
            continue
    
    if enabling_data:
        df_enabling = pd.DataFrame(enabling_data)
        
        # Display with priority-based styling
        st.dataframe(df_enabling, hide_index=True, use_container_width=True)
        
        # Priority breakdown
        if len(enabling_data) > 0:
            priority_counts = df_enabling['Priority'].value_counts()
            col1, col2, col3 = st.columns(3)
            
            with col1:
                high_count = priority_counts.get('High', 0)
                st.metric("High Priority", high_count, help="High success probability, near-term completion")
            
            with col2:
                medium_count = priority_counts.get('Medium', 0)
                st.metric("Medium Priority", medium_count, help="Moderate success probability and timeline")
            
            with col3:
                low_count = priority_counts.get('Low', 0)
                st.metric("Low Priority", low_count, help="Lower success probability or longer timeline")
    else:
        st.info("No enabling technologies meet the criteria")

# Timeline visualization
st.markdown('<div class="section-header">Technology Deployment Timeline</div>', 
            unsafe_allow_html=True)

# Prepare timeline data
timeline_data = []
all_concepts = fusion_concepts + fission_concepts

for node_id, node in all_concepts:
    try:
        time_to_deploy, success_prob = scheduler._find_critical_path(node_id, scheduler.nodes)
        if (time_to_deploy != float('inf') and 
            success_prob >= min_success_prob and
            timeline_range[0] <= time_to_deploy <= timeline_range[1]):
            
            deployment_year = 2025 + time_to_deploy
            timeline_data.append({
                'Technology': node['label'][:30] + ('...' if len(node['label']) > 30 else ''),
                'Full_Name': node['label'],
                'Deployment Year': deployment_year,
                'Success Probability': success_prob,
                'Category': node.get('category', 'Unknown'),
                'TRL': node.get('trl_current', 'Unknown'),
                'Time to Deploy': time_to_deploy,
                'Node_ID': node_id
            })
    except:
        continue

if timeline_data:
    df_timeline = pd.DataFrame(timeline_data)
    
    # Create timeline chart
    if group_by_category:
        fig = px.scatter(df_timeline, 
                        x='Deployment Year', 
                        y='Technology',
                        size='Success Probability',
                        color='Category',
                        hover_data=['TRL', 'Success Probability', 'Full_Name'],
                        title='Nuclear Technology Deployment Timeline by Category',
                        size_max=20)
    else:
        fig = px.scatter(df_timeline, 
                        x='Deployment Year', 
                        y='Technology',
                        size='Success Probability',
                        color='Success Probability',
                        color_continuous_scale='Viridis',
                        hover_data=['TRL', 'Category', 'Full_Name'],
                        title='Nuclear Technology Deployment Timeline by Success Probability',
                        size_max=20)
    
    fig.update_layout(
        height=max(500, len(timeline_data) * 25),
        yaxis={'categoryorder':'category ascending' if group_by_category else 'total ascending'},
        xaxis_title='Deployment Year',
        yaxis_title='Technology'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Technology readiness vs time analysis
    st.subheader("Technology Readiness vs Deployment Time Analysis")
    
    # Extract numeric TRL values for analysis
    df_timeline['TRL_Numeric'] = df_timeline['TRL'].apply(lambda x: 
        float(str(x).split('-')[0].split(' ')[0]) if str(x).replace('-', '').replace('.', '').replace(' ', '').isdigit() else 5.0)
    
    fig_readiness = px.scatter(df_timeline,
                              x='Time to Deploy',
                              y='TRL_Numeric',
                              size='Success Probability',
                              color='Category',
                              hover_name='Full_Name',
                              title='Technology Readiness Level vs Time to Deploy',
                              labels={'TRL_Numeric': 'Technology Readiness Level'},
                              size_max=20)
    
    # Add trend line
    fig_readiness.add_trace(
        go.Scatter(
            x=[df_timeline['Time to Deploy'].min(), df_timeline['Time to Deploy'].max()],
            y=[9, 2],  # Higher TRL should correlate with shorter time
            mode='lines',
            name='Expected Trend',
            line=dict(dash='dash', color='red', width=2),
            showlegend=True
        )
    )
    
    fig_readiness.update_layout(height=500)
    st.plotly_chart(fig_readiness, use_container_width=True)
    
    # Summary statistics
    st.markdown('<div class="section-header">Portfolio Summary</div>', 
                unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_deployment = df_timeline['Deployment Year'].mean()
        st.metric("Average Deployment Year", f"{avg_deployment:.0f}")
    
    with col2:
        avg_success = df_timeline['Success Probability'].mean()
        st.metric("Average Success Probability", f"{avg_success:.1%}")
    
    with col3:
        earliest_deployment = df_timeline['Deployment Year'].min()
        earliest_tech = df_timeline.loc[df_timeline['Deployment Year'].idxmin(), 'Full_Name']
        st.metric("Earliest Deployment", f"{earliest_deployment:.0f}")
        st.caption(f"{earliest_tech[:30]}...")
    
    with col4:
        high_prob_count = len(df_timeline[df_timeline['Success Probability'] > 0.7])
        st.metric("High Confidence Technologies", high_prob_count)
    
    # Risk-return analysis
    st.subheader("Risk-Return Analysis")
    
    # Calculate risk-adjusted metrics
    df_timeline['Risk_Score'] = 1 - df_timeline['Success Probability']
    df_timeline['Time_Score'] = df_timeline['Time to Deploy'] / df_timeline['Time to Deploy'].max()
    df_timeline['Overall_Risk'] = (df_timeline['Risk_Score'] + df_timeline['Time_Score']) / 2
    
    # Risk categories
    risk_categories = []
    risk_colors = []
    for _, row in df_timeline.iterrows():
        if row['Overall_Risk'] < 0.3:
            risk_categories.append('Low Risk')
            risk_colors.append('#28a745')
        elif row['Overall_Risk'] < 0.6:
            risk_categories.append('Medium Risk')
            risk_colors.append('#ffc107')
        else:
            risk_categories.append('High Risk')
            risk_colors.append('#dc3545')
    
    df_timeline['Risk_Category'] = risk_categories
    df_timeline['Risk_Color'] = risk_colors
    
    # Risk distribution
    risk_summary = df_timeline['Risk_Category'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_risk = px.pie(values=risk_summary.values, 
                         names=risk_summary.index,
                         title='Technology Portfolio by Risk Category',
                         color_discrete_map={
                             'Low Risk': '#28a745',
                             'Medium Risk': '#ffc107', 
                             'High Risk': '#dc3545'
                         })
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # Timeline by risk category
        fig_risk_timeline = px.box(df_timeline,
                                  x='Risk_Category',
                                  y='Deployment Year',
                                  title='Deployment Timeline by Risk Category',
                                  color='Risk_Category',
                                  color_discrete_map={
                                      'Low Risk': '#28a745',
                                      'Medium Risk': '#ffc107',
                                      'High Risk': '#dc3545'
                                  })
        st.plotly_chart(fig_risk_timeline, use_container_width=True)
    
    # Risk-adjusted recommendations
    st.subheader("Risk-Adjusted Investment Recommendations")
    
    # Create investment recommendations based on risk-return profile
    low_risk_high_return = df_timeline[
        (df_timeline['Risk_Category'] == 'Low Risk') & 
        (df_timeline['Success Probability'] > 0.7)
    ].sort_values('Deployment Year').head(3)
    
    balanced_options = df_timeline[
        (df_timeline['Risk_Category'] == 'Medium Risk') & 
        (df_timeline['Success Probability'] > 0.5) &
        (df_timeline['Time to Deploy'] < 15)
    ].sort_values('Success Probability', ascending=False).head(3)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="tech-category risk-low">', unsafe_allow_html=True)
        st.markdown("**Conservative Portfolio (Low Risk)**")
        if len(low_risk_high_return) > 0:
            for _, tech in low_risk_high_return.iterrows():
                st.write(f"• {tech['Full_Name'][:40]}")
                st.caption(f"   Deploy: {tech['Deployment Year']:.0f}, Success: {tech['Success Probability']:.1%}")
        else:
            st.write("No low-risk, high-return options available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="tech-category risk-medium">', unsafe_allow_html=True)
        st.markdown("**Balanced Portfolio (Medium Risk)**")
        if len(balanced_options) > 0:
            for _, tech in balanced_options.iterrows():
                st.write(f"• {tech['Full_Name'][:40]}")
                st.caption(f"   Deploy: {tech['Deployment Year']:.0f}, Success: {tech['Success Probability']:.1%}")
        else:
            st.write("No balanced options available")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("No technologies meet the selected criteria. Try adjusting the filters.")

# Dependency analysis (if enabled)
if show_dependencies and timeline_data:
    st.markdown('<div class="section-header">Technology Dependencies</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    **Key Technology Dependencies:**
    
    Understanding which technologies depend on others is crucial for investment prioritization.
    """)
    
    # Create dependency network visualization
    try:
        # Build dependency graph
        G = nx.DiGraph()
        
        # Add nodes
        for node_id, node in scheduler.nodes.items():
            if node.get('type') in ['ReactorConcept', 'Milestone', 'EnablingTechnology']:
                G.add_node(node_id, 
                          label=node['label'][:20] + ('...' if len(node['label']) > 20 else ''),
                          type=node.get('type'),
                          category=node.get('category', 'Other'))
        
        # Add edges
        for edge in scheduler.edges:
            source = edge['source']
            targets = edge.get('targets', [edge.get('target')])
            for target in targets:
                if target and source in G.nodes and target in G.nodes:
                    G.add_edge(source, target)
        
        # Calculate network metrics
        if len(G.nodes) > 0:
            # Most connected technologies
            in_degrees = dict(G.in_degree())
            out_degrees = dict(G.out_degree())
            
            # Find critical technologies (high out-degree - enables many others)
            critical_techs = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Find bottleneck technologies (high in-degree - many depend on them)
            bottleneck_techs = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Critical Enabling Technologies** (Enable Many Others):")
                for node_id, out_degree in critical_techs:
                    if out_degree > 0:
                        tech_name = scheduler.nodes[node_id]['label']
                        st.write(f"• **{tech_name}** → Enables {out_degree} technologies")
            
            with col2:
                st.markdown("**Bottleneck Technologies** (Many Depend On):")
                for node_id, in_degree in bottleneck_techs:
                    if in_degree > 0:
                        tech_name = scheduler.nodes[node_id]['label']
                        st.write(f"• **{tech_name}** ← {in_degree} technologies depend on this")
            
            # Dependency insights
            st.markdown("**Strategic Insights:**")
            st.markdown("""
            - **Critical Enabling Technologies** should be prioritized as they unlock multiple pathways
            - **Bottleneck Technologies** represent single points of failure in development chains
            - Consider parallel development paths to reduce dependency risks
            - Balance investments across independent technology clusters
            """)
        
    except Exception as e:
        st.write("Dependency analysis encountered an error. Complex dependencies require specialized visualization.")

# Key insights and recommendations
st.markdown('<div class="section-header">Key Insights and Recommendations</div>', 
            unsafe_allow_html=True)

if timeline_data:
    # Calculate insights based on the data
    df_insights = pd.DataFrame(timeline_data)
    
    fusion_count = len(df_insights[df_insights['Category'] == 'Fusion'])
    fission_count = len(df_insights[df_insights['Category'] == 'Fission'])
    near_term_count = len(df_insights[df_insights['Deployment Year'] <= 2030])
    high_confidence_count = len(df_insights[df_insights['Success Probability'] > 0.8])
    avg_time = df_insights['Time to Deploy'].mean()
    
    st.markdown(f"""
    **Portfolio Analysis Results:**
    
    1. **Technology Mix**: Your filtered portfolio contains {fusion_count} fusion and {fission_count} fission technologies.
    
    2. **Timeline Analysis**: Average time to deployment is {avg_time:.1f} years, with {near_term_count} technologies deployable by 2030.
    
    3. **Risk Assessment**: {high_confidence_count} technologies have >80% success probability, representing lower-risk investments.
    
    4. **Strategic Recommendations**:
       - **Diversification**: Balance investments across fusion and fission to manage technological risk
       - **Timeline Management**: Mix near-term and long-term bets for steady progress and sustained impact
       - **Risk Management**: Prioritize high-confidence technologies for reliable returns while including breakthrough bets
       - **Enabling Technologies**: Invest in technologies that enable multiple downstream pathways
    
    5. **Investment Portfolio Strategy**:
       - **30% Conservative**: High TRL, high success probability technologies for near-term deployment
       - **50% Balanced**: Medium risk technologies with reasonable timelines and good potential
       - **20% Breakthrough**: High-risk, high-reward technologies that could transform the industry
    
    6. **Technology Pathway Priorities**:
       - **Fusion Focus**: Emphasize technologies with demonstrated physics feasibility
       - **Fission Focus**: Leverage existing supply chains and regulatory frameworks
       - **Cross-cutting**: Prioritize enabling technologies that benefit multiple pathways
    """)
    
    # Create a simple portfolio recommendation
    if len(df_insights) >= 6:
        conservative = df_insights[df_insights['Risk_Category'] == 'Low Risk'].head(2)
        balanced = df_insights[df_insights['Risk_Category'] == 'Medium Risk'].head(3)
        breakthrough = df_insights[df_insights['Risk_Category'] == 'High Risk'].head(1)
        
        st.subheader("Recommended Investment Portfolio")
        
        portfolio_data = []
        
        for _, tech in conservative.iterrows():
            portfolio_data.append({
                'Technology': tech['Full_Name'][:40],
                'Category': 'Conservative',
                'Deployment Year': f"{tech['Deployment Year']:.0f}",
                'Success Probability': f"{tech['Success Probability']:.1%}",
                'Risk Level': tech['Risk_Category']
            })
        
        for _, tech in balanced.iterrows():
            portfolio_data.append({
                'Technology': tech['Full_Name'][:40],
                'Category': 'Balanced',
                'Deployment Year': f"{tech['Deployment Year']:.0f}",
                'Success Probability': f"{tech['Success Probability']:.1%}",
                'Risk Level': tech['Risk_Category']
            })
        
        for _, tech in breakthrough.iterrows():
            portfolio_data.append({
                'Technology': tech['Full_Name'][:40],
                'Category': 'Breakthrough',
                'Deployment Year': f"{tech['Deployment Year']:.0f}",
                'Success Probability': f"{tech['Success Probability']:.1%}",
                'Risk Level': tech['Risk_Category']
            })
        
        if portfolio_data:
            df_portfolio = pd.DataFrame(portfolio_data)
            st.dataframe(df_portfolio, hide_index=True, use_container_width=True)
            
            st.caption("""
            **Portfolio Rationale**: This balanced approach provides steady near-term progress (Conservative), 
            substantial medium-term impact (Balanced), and potential breakthrough opportunities (Breakthrough) 
            while managing overall portfolio risk.
            """)

else:
    st.markdown("""
    **Adjust the filters above to see technology comparison results and strategic insights.**
    
    **Recommended Settings:**
    - **Timeline Range**: 5-20 years for near to medium-term focus
    - **Minimum Success Probability**: 0.3 to include promising early-stage technologies
    - **Technology Type**: "All Technologies" for comprehensive analysis
    - **Show Dependencies**: Enable to understand technology interdependencies
    
    **Analysis Tips:**
    - Lower the success probability threshold to see more experimental technologies
    - Expand the timeline range to include long-term breakthrough opportunities
    - Enable detailed metrics to see potential energy output calculations
    - Use dependency analysis to identify critical enabling technologies
    """)