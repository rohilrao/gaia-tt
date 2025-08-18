"""
Enhanced Run Simulations page for the Nuclear Investment Analyzer.
This page provides complete data context to the AI chat for accurate question answering.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import time

# Import the scheduler and technology data
from utils.nuclear_scheduler import NuclearScheduler
from utils.tech_tree_data import tech_tree
from utils.langgraph_workflow import NuclearSimulationWorkflow

# Import Google Gen AI SDK
import google.genai as genai
from google.genai import types


def initialize_workflow():
    """Initialize the LangGraph workflow with Gemini."""
    try:
        client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
        workflow = NuclearSimulationWorkflow(client)
        return workflow, client
    except Exception as e:
        st.error(f"Failed to initialize AI workflow: {str(e)}")
        return None, None


def create_heatmap(impact_data, min_impact=0.1, show_all_techs=False, color_scheme="plasma"):
    """Create the impact heatmap visualization."""
    if not impact_data:
        return None
    
    # Prepare heatmap data
    heatmap_data = []
    for tech, yearly_impact in impact_data.items():
        for year, impact in yearly_impact.items():
            heatmap_data.append([tech, int(year), impact])
    
    if not heatmap_data:
        return None
    
    df = pd.DataFrame(heatmap_data, columns=["Technology", "Year", "Impact (TWh)"])
    filtered_df = df[df["Impact (TWh)"] >= min_impact]
    
    if not show_all_techs and len(filtered_df) > 0:
        tech_max_impacts = (
            filtered_df.groupby("Technology")["Impact (TWh)"].max().sort_values(ascending=False)
        )
        top_techs = tech_max_impacts.head(15).index.tolist()
        filtered_df = filtered_df[filtered_df["Technology"].isin(top_techs)]
    
    if len(filtered_df) == 0:
        return None
    
    pivot_df = filtered_df.pivot_table(
        index="Technology",
        columns="Year",
        values="Impact (TWh)",
        fill_value=0,
    )
    
    # Get actual year range from the data
    min_year, max_year = pivot_df.columns.min(), pivot_df.columns.max()
    
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale=color_scheme,
            colorbar=dict(
                title="Impact (TWh)",
                thickness=15,
                len=0.7
            ),
            hoverongaps=False,
            hovertemplate="<b>%{y}</b><br>Year: %{x}<br>Impact: %{z:.2f} TWh<extra></extra>",
        )
    )
    fig.update_layout(
        title={
            'text': f"Technology Acceleration Impact by Year",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2c3e50'}
        },
        xaxis_title="Year",
        yaxis_title="Technology",
        height=max(500, len(pivot_df.index) * 30),
        yaxis=dict(autorange="reversed"),
        xaxis=dict(
            dtick=max(1, (max_year - min_year) // 10),  # Smart tick spacing
            tickangle=45 if max_year - min_year > 20 else 0
        ),
        font=dict(size=11),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig, filtered_df


def calculate_summary_stats(impact_data):
    """Calculate summary statistics from impact data."""
    if not impact_data:
        return {
            "total_techs": 0,
            "active_techs": 0,
            "max_impact": 0,
            "current_opportunities": 0
        }
    
    total_techs = len(impact_data.keys())
    active_techs = sum(
        1 for tech_data in impact_data.values()
        if any(impact > 0 for impact in tech_data.values())
    )
    max_impact = max(
        (max(yearly_impacts.values()) for yearly_impacts in impact_data.values() if yearly_impacts),
        default=0,
    )
    current_year = 2025
    current_opportunities = sum(
        1 for tech_data in impact_data.values()
        if tech_data.get(current_year, 0) > 0
    )
    
    return {
        "total_techs": total_techs,
        "active_techs": active_techs,
        "max_impact": max_impact,
        "current_opportunities": current_opportunities
    }


def main():
    """Entry point for the Run Simulations Streamlit page."""
    
    # Page configuration
    st.set_page_config(
        page_title="Run Simulations - Nuclear Investment Analyzer",
        page_icon="⚛️",
        layout="wide",
    )
    
    # Apply custom CSS styling
    st.markdown(
        """
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
            .chat-instructions {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;
            }
            .instruction-item {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 0.75rem;
                margin: 0.5rem 0;
                border-left: 3px solid rgba(255, 255, 255, 0.3);
            }
            .simulation-status {
                background-color: #e8f5e8;
                border: 1px solid #4caf50;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            }
            .success-notification {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
                border-left: 4px solid #28a745;
            }
            .data-context-info {
                background-color: #e1f5fe;
                border: 1px solid #0288d1;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
                border-left: 4px solid #0288d1;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown(
        '<div class="main-header">Interactive Nuclear Technology Simulation</div>',
        unsafe_allow_html=True,
    )
    
    st.markdown(
        """
        This page provides an **interactive simulation environment** where you can run custom 
        nuclear technology simulations and get real-time analysis through AI-powered chat with 
        **complete access to all simulation data**.
        """
    )
    
    # Initialize session state for simulation data
    if "current_simulation_data" not in st.session_state:
        st.session_state.current_simulation_data = None
    if "current_context" not in st.session_state:
        st.session_state.current_context = "No simulation has been run yet. Ask me to run a simulation!"
    if "complete_data_context" not in st.session_state:
        st.session_state.complete_data_context = ""
    if "simulation_messages" not in st.session_state:
        st.session_state.simulation_messages = []
    if "dashboard_update_needed" not in st.session_state:
        st.session_state.dashboard_update_needed = False
    
    # Initialize workflow
    workflow, genai_client = initialize_workflow()
    
    if not workflow:
        st.error("AI-powered simulation is not available. Please check your API configuration.")
        st.stop()
    
    # Sidebar for display controls
    with st.sidebar:
        st.header("Display Filters")
        min_impact = st.slider(
            "Minimum Impact to Display (TWh)",
            min_value=0.0,
            max_value=5.0,
            value=0.1,
            step=0.1,
            help="Filter out technologies with impact below this threshold",
        )
        
        show_all_techs = st.checkbox(
            "Show All Technologies",
            value=False,
            help="Show all technologies or limit to top 15 by maximum impact",
        )
        
        # Color scheme selection
        st.subheader("Visualization Options")
        color_scheme = st.selectbox(
            "Heatmap Color Scheme",
            options=[
                "plasma",
                "turbo", 
                "inferno",
                "magma",
                "cividis",
                "blues",
                "oranges",
                "greens",
                "reds",
                "rdylgn",
                "spectral"
            ],
            index=0,
            help="Choose the color scheme for the heatmap visualization"
        )
        
        # Quick simulation buttons
        st.subheader("Quick Simulations")
        if st.button("Run 30-Year Simulation", use_container_width=True):
            st.session_state.quick_simulation_request = "Run a simulation for 30 years"
        
        if st.button("Run 20-Year Simulation", use_container_width=True):
            st.session_state.quick_simulation_request = "Run a simulation for 20 years"
        
        if st.button("Run 40-Year Simulation", use_container_width=True):
            st.session_state.quick_simulation_request = "Run a simulation for 40 years"
        
        # Data context indicator
        if st.session_state.complete_data_context:
            st.markdown(
                """
                <div class="data-context-info">
                    <strong>🔍 Complete Data Access</strong><br>
                    The AI has access to all raw simulation data, tech tree details, 
                    and dashboard plotting data for accurate question answering.
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Handle quick simulation requests
    if "quick_simulation_request" in st.session_state:
        user_input = st.session_state.quick_simulation_request
        del st.session_state.quick_simulation_request
        
        # Add user message to history
        st.session_state.simulation_messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Running simulation..."):
            result = workflow.process_user_input(
                user_input, 
                st.session_state.current_context,
                st.session_state.complete_data_context
            )
            
            # Update session state and context
            st.session_state.current_context = result["context_summary"]
            st.session_state.complete_data_context = result["complete_data_context"]
            
            # Add assistant response to history
            st.session_state.simulation_messages.append({"role": "assistant", "content": result["response"]})
            
            # Update simulation data if available
            if result["simulation_results"]:
                st.session_state.current_simulation_data = result["simulation_results"]
                st.session_state.dashboard_update_needed = True
                # Show success notification
                st.success("Simulation completed! Dashboard has been updated with new results.")
                st.rerun()
    
    # Display current simulation results
    if st.session_state.current_simulation_data:
        impact_data = st.session_state.current_simulation_data["impact_data"]
        summary_stats = st.session_state.current_simulation_data["summary_stats"]
        years_simulated = st.session_state.current_simulation_data["years_simulated"]
        
        # Show update notification if dashboard was just updated
        if st.session_state.dashboard_update_needed:
            st.markdown(
                """
                <div class="success-notification">
                    <strong>Dashboard Updated!</strong> New simulation results are now displayed below. 
                    The AI chat now has complete access to all raw data for detailed question answering.
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.session_state.dashboard_update_needed = False
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Technologies Analyzed", summary_stats["total_techs"])
        with col2:
            st.metric("Technologies with Positive Impact", summary_stats["active_techs"])
        with col3:
            st.metric("Maximum Single-Year Impact", f"{summary_stats['max_impact']:.1f} TWh")
        with col4:
            st.metric("Years Simulated", years_simulated)
        
        # Create and display heatmap
        heatmap_result = create_heatmap(impact_data, min_impact, show_all_techs, color_scheme)
        
        if heatmap_result:
            fig, filtered_df = heatmap_result
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary table
            st.markdown(
                '<div class="section-header">Investment Opportunities by Year</div>',
                unsafe_allow_html=True,
            )
            available_years = sorted(filtered_df["Year"].unique())
            if available_years:
                selected_year = st.selectbox(
                    "Select Year for Detailed Analysis",
                    available_years,
                    index=0,
                )
                
                year_data = (
                    filtered_df[filtered_df["Year"] == selected_year]
                    .sort_values("Impact (TWh)", ascending=False)
                )
                year_data = year_data[year_data["Impact (TWh)"] > 0].head(10)
                
                if len(year_data) > 0:
                    st.dataframe(
                        year_data.reset_index(drop=True),
                        column_config={
                            "Technology": st.column_config.TextColumn("Technology", width="large"),
                            "Impact (TWh)": st.column_config.NumberColumn(
                                "Impact (TWh)", format="%.2f"
                            ),
                        },
                        hide_index=True,
                        use_container_width=True,
                    )
                else:
                    st.info(f"No investment opportunities with positive impact in {selected_year}")
        else:
            st.warning("No technologies meet the minimum impact threshold. Try lowering the filter or running a different simulation.")
    
    else:
        # Show placeholder when no simulation has been run
        st.markdown(
            """
            <div class="simulation-status">
                <h3>Ready to Run Simulations</h3>
                <p>No simulation data available yet. Use the chat below or quick buttons in the sidebar to run your first simulation!</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Interactive Chat Section
    st.markdown(
        '<div class="section-header">AI-Powered Simulation Chat</div>',
        unsafe_allow_html=True,
    )
    
    # Enhanced chat instructions
    if st.session_state.complete_data_context:
        st.markdown(
            """
            <div class="chat-instructions">
                <h4>🤖 Enhanced AI Assistant with Complete Data Access</h4>
                <p>The AI now has access to:</p>
                <div class="instruction-item">
                    <strong>📊 Complete Raw Data:</strong> All impact values by technology and year
                </div>
                <div class="instruction-item">
                    <strong>🔬 Technology Details:</strong> Full tech tree with descriptions, categories, dependencies, investment requirements
                </div>
                <div class="instruction-item">
                    <strong>📈 Development Status:</strong> Progress percentages, development timelines, investment tracking
                </div>
                <div class="instruction-item">
                    <strong>🎯 Dashboard Data:</strong> Exact data used in visualizations and rankings
                </div>
                <p><strong>Try asking:</strong> "What's the exact impact of Thorium MSRs in 2035?" or "Which technology requires the least investment but has high impact?"</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="chat-instructions">
                <h4>🤖 AI-Powered Simulation Assistant</h4>
                <p>Ask me to run simulations or get help with the interface:</p>
                <div class="instruction-item">
                    <strong>🔬 Run Simulations:</strong> "Run a 30-year simulation" or "Simulate for 25 years"
                </div>
                <div class="instruction-item">
                    <strong>❓ Ask Questions:</strong> After running a simulation, I'll have complete data access
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Display chat history
    for message in st.session_state.simulation_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if st.session_state.complete_data_context:
        placeholder_text = "Ask detailed questions about the simulation data, technologies, or request new simulations..."
    else:
        placeholder_text = "Ask me to run a simulation or answer questions about the results..."
    
    user_input = st.chat_input(placeholder_text)
    
    if user_input:
        # Add user message to history
        st.session_state.simulation_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Process through workflow
        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                result = workflow.process_user_input(
                    user_input, 
                    st.session_state.current_context,
                    st.session_state.complete_data_context
                )
                
                # Always update context
                st.session_state.current_context = result["context_summary"]
                st.session_state.complete_data_context = result["complete_data_context"]
                
                # Display response first
                st.markdown(result["response"])
                
                # Add assistant response to history
                st.session_state.simulation_messages.append({"role": "assistant", "content": result["response"]})
                
                # Update session state if simulation was run
                if result["simulation_results"]:
                    st.session_state.current_simulation_data = result["simulation_results"]
                    st.session_state.dashboard_update_needed = True
                    
                    # Trigger rerun to update dashboard
                    st.rerun()


if __name__ == "__main__":
    main()