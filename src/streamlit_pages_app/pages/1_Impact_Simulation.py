"""
This Streamlit application provides an interactive dashboard for exploring the
impact of accelerating nuclear technologies. It visualises simulation results
via a heatmap and summary metrics and includes a Gemini‑powered chat
assistant that can answer follow‑up questions. 
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Import the scheduler and technology data
from utils.nuclear_scheduler import NuclearScheduler
from utils.tech_tree_data import tech_tree

# Import Google Gen AI SDK.  This SDK exposes a `client.chats` API for
# multi‑turn conversations. 
import google.genai as genai
from google.genai import types


def main() -> None:
    """Entry point for the Technology Simulation Streamlit page."""

    # Page configuration
    st.set_page_config(
        page_title="Technology Simulation - Nuclear Investment Analyzer",
        page_icon="🔬",
        layout="wide",
    )

    # Apply custom CSS styling for headers and containers
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
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="main-header">Technology Acceleration Impact Simulation</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        This simulation models the **immediate impact** of accelerating each technology by one year
        in each specific year. The impact is measured in additional clean energy (TWh)
        generated over the technology's lifetime.
        """
    )

    # Sidebar for simulation parameters
    with st.sidebar:
        st.header("Simulation Parameters")

        simulation_years: int = st.slider(
            "Simulation Years",
            min_value=10,
            max_value=50,
            value=30,
            help="Number of years to simulate forward",
        )

        discount_rate: float = st.slider(
            "Discount Rate",
            min_value=0.01,
            max_value=0.10,
            value=0.05,
            step=0.01,
            format="%.2f",
            help="Annual discount rate for future energy benefits",
        )

        st.subheader("Model Assumptions")
        capacity_factor: float = st.slider(
            "Plant Capacity Factor",
            min_value=0.70,
            max_value=0.95,
            value=0.90,
            step=0.01,
            help="Average capacity factor for nuclear plants",
        )

        avg_plant_size: int = st.slider(
            "Average Plant Size (MW)",
            min_value=300,
            max_value=1500,
            value=1000,
            step=50,
            help="Average capacity of deployed nuclear plants",
        )

        st.subheader("Display Filters")
        min_impact: float = st.slider(
            "Minimum Impact to Display (TWh)",
            min_value=0.0,
            max_value=5.0,
            value=0.1,
            step=0.1,
            help="Filter out technologies with impact below this threshold",
        )

        show_all_techs: bool = st.checkbox(
            "Show All Technologies",
            value=False,
            help="Show all technologies or limit to top 15 by maximum impact",
        )

    # Initialize scheduler and run the simulation
    scheduler = NuclearScheduler(tech_tree)
    with st.spinner("Running technology acceleration simulation..."):
        impact_data, status_data = scheduler.run_simulation(years_to_simulate=simulation_years)

    # Display metrics in four columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_techs = len(impact_data.keys())
        st.metric("Technologies Analyzed", total_techs)
    with col2:
        active_techs = sum(
            1
            for tech_data in impact_data.values()
            if any(impact > 0 for impact in tech_data.values())
        )
        st.metric("Technologies with Positive Impact", active_techs)
    with col3:
        max_impact = max(
            (
                max(yearly_impacts.values())
                for yearly_impacts in impact_data.values()
                if yearly_impacts
            ),
            default=0,
        )
        st.metric("Maximum Single-Year Impact", f"{max_impact:.1f} TWh")
    with col4:
        current_year = 2025
        current_opportunities = sum(
            1
            for tech_data in impact_data.values()
            if tech_data.get(current_year, 0) > 0
        )
        st.metric(f"Investment Opportunities in {current_year}", current_opportunities)

    # Prepare heatmap data for Plotly
    heatmap_data: list[list] = []
    for tech, yearly_impact in impact_data.items():
        for year, impact in yearly_impact.items():
            heatmap_data.append([tech, int(year), impact])

    # If we have simulation data, build the heatmap and allow filtering
    if heatmap_data:
        df = pd.DataFrame(heatmap_data, columns=["Technology", "Year", "Impact (TWh)"])
        filtered_df = df[df["Impact (TWh)"] >= min_impact]
        if not show_all_techs and len(filtered_df) > 0:
            tech_max_impacts = (
                filtered_df.groupby("Technology")["Impact (TWh)"].max().sort_values(ascending=False)
            )
            top_techs = tech_max_impacts.head(15).index.tolist()
            filtered_df = filtered_df[filtered_df["Technology"].isin(top_techs)]

        if len(filtered_df) > 0:
            pivot_df = filtered_df.pivot_table(
                index="Technology",
                columns="Year",
                values="Impact (TWh)",
                fill_value=0,
            )
            fig = go.Figure(
                data=go.Heatmap(
                    z=pivot_df.values,
                    x=pivot_df.columns,
                    y=pivot_df.index,
                    colorscale="Viridis",
                    colorbar=dict(title="Impact (TWh)"),
                    hoverongaps=False,
                    hovertemplate="Year: %{x}<br>Technology: %{y}<br>Impact: %{z:.2f} TWh<extra></extra>",
                )
            )
            fig.update_layout(
                title="Technology Acceleration Impact by Year",
                xaxis_title="Year",
                yaxis_title="Technology",
                height=max(400, len(pivot_df.index) * 25),
                yaxis=dict(autorange="reversed"),
                font=dict(size=10),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Summary table of investment opportunities by year
            st.markdown(
                '<div class="section-header">Investment Opportunities by Year</div>',
                unsafe_allow_html=True,
            )
            available_years = sorted(df["Year"].unique())
            selected_year = st.selectbox(
                "Select Year for Detailed Analysis",
                available_years,
                index=0 if available_years else 0,
            )
            if selected_year:
                year_data = (
                    df[df["Year"] == selected_year]
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
            st.warning(
                "No technologies meet the minimum impact threshold. Try lowering the minimum impact filter in the sidebar."
            )
    else:
        st.error("No simulation data generated. Please check the configuration.")

    
    # --- Gemini Chat Assistant ---
    # Remove the previous static insights and replace it with an interactive chat.
    st.markdown(
        '<div class="section-header">Interactive Simulation Chat</div>',
        unsafe_allow_html=True,
    )

    # Build a detailed context string summarising the simulation for the system instruction.
    context_lines = []
    context_lines.append(
        f"Simulation parameters: simulation_years={simulation_years}, discount_rate={discount_rate:.2f}, "
        f"capacity_factor={capacity_factor:.2f}, avg_plant_size={avg_plant_size} MW."
    )
    context_lines.append(
        f"Total technologies analysed: {total_techs}. Positive impact technologies: {active_techs}. "
        f"Maximum single‑year impact: {max_impact:.1f} TWh. Investment opportunities in {current_year}: {current_opportunities}."
    )
    # Identify up to five top technologies by maximum impact, if available
    try:
        tech_max = df.groupby("Technology")["Impact (TWh)"].max().sort_values(ascending=False)
        top_list = tech_max.head(5).index.tolist()
        if top_list:
            context_lines.append(
                "Top technologies with highest potential impact: " + ", ".join(top_list) + "."
            )
    except Exception:
        # if df isn't defined due to no data
        pass
    # Combine context lines into a single instruction
    # Build the system instruction by concatenating strings.  Do not place a raw
    # newline outside of quotes – instead include it inside the string or use
    # explicit concatenation.  This avoids syntax errors when Python parses
    # backslash‑escaped line breaks.
    system_instruction: str = (
        "You are an expert assistant helping users understand a nuclear technology "
        "acceleration simulation. The simulation models the impact of accelerating "
        "each technology by one year and measures additional clean energy (TWh) "
        "generated over its lifetime. Use the following context when answering questions:\n"
        + "\n".join(context_lines)
        + "\n\n"
        + "Your first response should provide a concise overview summarising the "
        "key findings of the simulation in one or two sentences. Provide more "
        "detail only when the user asks follow‑up questions. If the question is "
        "unrelated to the simulation, politely decline to answer and remind the "
        "user to ask about the simulation."
    )

    # Initialise the chat session on first load.  The Gen AI SDK caches chat
    # history in the Chat object, so repeated send_message calls will build
    # Streamlit's session_state to persist across reruns.
    import os
    if "simulation_chat" not in st.session_state:
        client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))  # use API key from environment or config
        chat_config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            max_output_tokens=1024,
        )
        st.session_state.simulation_chat = client.chats.create(
            model="gemini-2.0-flash-001",  # choose a fast, cost‑effective model
            config=chat_config,
        )
        # Issue an initial prompt requesting a brief summary
        init_prompt = (
            "Provide a concise summary of the simulation results. "
            "Do not go into detail unless asked later."
        )
        initial_text = ""
        for chunk in st.session_state.simulation_chat.send_message_stream(init_prompt):
            # accumulate chunk.text from streaming responses
            initial_text += chunk.text
        # Save assistant's first message in history
        st.session_state.messages = [
            {"role": "assistant", "content": initial_text},
        ]

    # Display chat history
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for user
    user_input = st.chat_input("Ask about the simulation…")
    if user_input:
        # Append user's message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        # Send message to Gemini and stream response
        response_text = ""
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            for chunk in st.session_state.simulation_chat.send_message_stream(user_input):
                response_text += chunk.text
                # progressively update the message display
                response_placeholder.markdown(response_text)
        # Append assistant's response to history
        st.session_state.messages.append({"role": "assistant", "content": response_text})


if __name__ == "__main__":
    main()