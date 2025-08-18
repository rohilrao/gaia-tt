"""
Enhanced LangGraph workflow for handling nuclear simulation requests and questions.
This workflow provides complete data context including raw simulation data, tech tree data,
and dashboard plotting data to enable accurate question answering.
"""

import json
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import google.genai as genai
from google.genai import types
import pandas as pd

from utils.nuclear_scheduler import NuclearScheduler
from utils.tech_tree_data import tech_tree


class SimulationState(TypedDict):
    """State for the simulation workflow."""
    messages: Annotated[List[Dict[str, str]], add_messages]
    user_query: str
    simulation_request: Optional[Dict[str, Any]]
    simulation_results: Optional[Dict[str, Any]]
    context_summary: str
    complete_data_context: str  # New: Complete raw data context
    response: str


class NuclearSimulationWorkflow:
    """Enhanced LangGraph workflow for nuclear simulation and analysis."""
    
    def __init__(self, genai_client):
        self.client = genai_client
        self.scheduler = NuclearScheduler(tech_tree)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(SimulationState)
        
        # Add nodes
        workflow.add_node("classify_intent", self._classify_intent)
        workflow.add_node("run_simulation", self._run_simulation)
        workflow.add_node("answer_question", self._answer_question)
        workflow.add_node("format_response", self._format_response)
        
        # Add edges
        workflow.set_entry_point("classify_intent")
        workflow.add_conditional_edges(
            "classify_intent",
            self._route_based_on_intent,
            {
                "simulation": "run_simulation",
                "question": "answer_question"
            }
        )
        workflow.add_edge("run_simulation", "format_response")
        workflow.add_edge("answer_question", "format_response")
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    def _create_complete_data_context(self, impact_data: Dict, status_data: Dict, years_simulated: int) -> str:
        """Create comprehensive data context including all raw data for accurate question answering."""
        if not impact_data:
            return "No simulation data available."
        
        # 1. Tech Tree Information
        tech_tree_context = "TECHNOLOGY TREE INFORMATION:\n"
        for tech_name, tech_info in tech_tree.items():
            tech_tree_context += f"- {tech_name}:\n"
            tech_tree_context += f"  * Description: {tech_info.get('description', 'N/A')}\n"
            tech_tree_context += f"  * Category: {tech_info.get('category', 'N/A')}\n"
            tech_tree_context += f"  * Readiness Level: {tech_info.get('readiness_level', 'N/A')}\n"
            tech_tree_context += f"  * Impact Potential: {tech_info.get('impact_potential', 'N/A')}\n"
            tech_tree_context += f"  * Dependencies: {tech_info.get('dependencies', [])}\n"
            tech_tree_context += f"  * Investment Required: ${tech_info.get('investment_required', 0):,}M\n"
            tech_tree_context += f"  * Development Time: {tech_info.get('development_time', 'N/A')} years\n\n"
        
        # 2. Complete Impact Data (year-by-year for all technologies)
        impact_context = "COMPLETE IMPACT DATA (TWh by year for all technologies):\n"
        
        # Get all years in the simulation
        all_years = set()
        for tech_data in impact_data.values():
            all_years.update(tech_data.keys())
        all_years = sorted(all_years)
        
        for tech_name, yearly_impacts in impact_data.items():
            impact_context += f"\n{tech_name}:\n"
            for year in all_years:
                impact_value = yearly_impacts.get(year, 0)
                if impact_value > 0:  # Only show years with positive impact
                    impact_context += f"  {year}: {impact_value:.3f} TWh\n"
        
        # 3. Technology Status Data
        status_context = "\nTECHNOLOGY STATUS DATA:\n"
        for tech_name, status_info in status_data.items():
            status_context += f"\n{tech_name}:\n"
            status_context += f"  * Current Status: {status_info.get('status', 'Unknown')}\n"
            status_context += f"  * Development Progress: {status_info.get('development_progress', 0):.1f}%\n"
            status_context += f"  * Years in Development: {status_info.get('years_in_development', 0)}\n"
            status_context += f"  * Total Investment: ${status_info.get('total_investment', 0):,}M\n"
            status_context += f"  * Dependencies Met: {status_info.get('dependencies_met', [])}\n"
            status_context += f"  * Dependencies Pending: {status_info.get('dependencies_pending', [])}\n"
        
        # 4. Dashboard/Plotting Data Context
        dashboard_context = "\nDASHBOARD DATA CONTEXT:\n"
        
        # Technology rankings by total impact
        tech_total_impacts = {}
        for tech, yearly_data in impact_data.items():
            tech_total_impacts[tech] = sum(yearly_data.values()) if yearly_data else 0
        
        top_techs_by_total = sorted(tech_total_impacts.items(), key=lambda x: x[1], reverse=True)
        dashboard_context += "Technologies ranked by total impact over simulation period:\n"
        for i, (tech, total_impact) in enumerate(top_techs_by_total[:20], 1):
            dashboard_context += f"  {i}. {tech}: {total_impact:.2f} TWh (total)\n"
        
        # Technology rankings by peak impact
        tech_peak_impacts = {}
        for tech, yearly_data in impact_data.items():
            tech_peak_impacts[tech] = max(yearly_data.values()) if yearly_data else 0
        
        top_techs_by_peak = sorted(tech_peak_impacts.items(), key=lambda x: x[1], reverse=True)
        dashboard_context += "\nTechnologies ranked by peak single-year impact:\n"
        for i, (tech, peak_impact) in enumerate(top_techs_by_peak[:20], 1):
            dashboard_context += f"  {i}. {tech}: {peak_impact:.2f} TWh (peak)\n"
        
        # Year-by-year opportunity analysis
        dashboard_context += "\nYear-by-year investment opportunities (technologies with positive impact):\n"
        for year in all_years:
            year_opportunities = []
            for tech, yearly_data in impact_data.items():
                impact = yearly_data.get(year, 0)
                if impact > 0:
                    year_opportunities.append((tech, impact))
            
            year_opportunities.sort(key=lambda x: x[1], reverse=True)
            dashboard_context += f"\n{year} ({len(year_opportunities)} opportunities):\n"
            for tech, impact in year_opportunities[:10]:  # Top 10 per year
                dashboard_context += f"  - {tech}: {impact:.3f} TWh\n"
        
        # 5. Simulation Metadata
        metadata_context = f"\nSIMULATION METADATA:\n"
        metadata_context += f"- Simulation Period: 2025 to {2025 + years_simulated - 1} ({years_simulated} years)\n"
        metadata_context += f"- Total Technologies: {len(impact_data)}\n"
        metadata_context += f"- Technologies with Impact: {len([t for t in impact_data.values() if any(v > 0 for v in t.values())])}\n"
        metadata_context += f"- Total Impact Across All Technologies: {sum(sum(yearly_data.values()) for yearly_data in impact_data.values()):.2f} TWh\n"
        metadata_context += f"- Peak Single Year Impact: {max((max(yearly_data.values()) for yearly_data in impact_data.values() if yearly_data), default=0):.2f} TWh\n"
        
        # Combine all contexts
        complete_context = f"""
{tech_tree_context}

{impact_context}

{status_context}

{dashboard_context}

{metadata_context}

IMPORTANT NOTES FOR ANALYSIS:
- All impact values are in TWh (Terawatt-hours)
- Investment values are in millions of dollars
- Development progress is percentage complete
- The heatmap visualization shows this impact data with technologies on Y-axis and years on X-axis
- Technologies with zero impact in all years are not shown in visualizations
- The dashboard allows filtering by minimum impact threshold
- Users can select specific years to see detailed investment opportunities for that year
"""
        
        return complete_context.strip()
    
    def _classify_intent(self, state: SimulationState) -> SimulationState:
        """Classify whether the user wants to run a simulation or ask a question."""
        user_query = state["user_query"]
        
        classification_prompt = f"""
        Analyze this user query and determine if they want to:
        1. Run a simulation (keywords: "run", "simulate", "simulation", mentions of years like "30 years", "25 years")
        2. Ask a question about existing data/dashboard
        
        User query: "{user_query}"
        
        Respond with JSON in this format:
        {{
            "intent": "simulation" or "question",
            "years": number (if simulation request, extract the number of years),
            "confidence": float between 0 and 1
        }}
        
        Examples:
        - "Run a simulation for 30 years" -> {{"intent": "simulation", "years": 30, "confidence": 0.95}}
        - "What are the top technologies?" -> {{"intent": "question", "years": null, "confidence": 0.9}}
        - "Simulate for 25 years" -> {{"intent": "simulation", "years": 25, "confidence": 0.9}}
        """
        
        try:
            chat_config = types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=200,
            )
            chat = self.client.chats.create(
                model="gemini-2.0-flash-001",
                config=chat_config,
            )
            
            response_text = ""
            for chunk in chat.send_message_stream(classification_prompt):
                response_text += chunk.text
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                classification = json.loads(json_match.group())
            else:
                # Fallback classification
                classification = {
                    "intent": "simulation" if any(word in user_query.lower() for word in ["run", "simulate", "simulation"]) else "question",
                    "years": None,
                    "confidence": 0.5
                }
            
            # Extract years if it's a simulation request
            if classification["intent"] == "simulation" and not classification.get("years"):
                # Try to extract years from the query
                year_patterns = [r'(\d+)\s*years?', r'for\s*(\d+)', r'(\d+)\s*year']
                for pattern in year_patterns:
                    match = re.search(pattern, user_query.lower())
                    if match:
                        classification["years"] = int(match.group(1))
                        break
                
                # Default to 30 years if no years specified
                if not classification.get("years"):
                    classification["years"] = 30
            
            state["simulation_request"] = classification
            
        except Exception as e:
            print(f"Error in classification: {e}")
            # Fallback classification
            state["simulation_request"] = {
                "intent": "question",
                "years": None,
                "confidence": 0.5
            }
        
        return state
    
    def _route_based_on_intent(self, state: SimulationState) -> str:
        """Route to appropriate handler based on classified intent."""
        intent = state["simulation_request"]["intent"]
        return intent
    
    def _run_simulation(self, state: SimulationState) -> SimulationState:
        """Run the nuclear technology simulation."""
        years = state["simulation_request"].get("years", 30)
        
        try:
            print(f"Running simulation for {years} years...")
            impact_data, status_data = self.scheduler.run_simulation(years_to_simulate=years)
            
            # Calculate summary statistics
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
            
            # Store results
            state["simulation_results"] = {
                "impact_data": impact_data,
                "status_data": status_data,
                "years_simulated": years,
                "summary_stats": {
                    "total_techs": total_techs,
                    "active_techs": active_techs,
                    "max_impact": max_impact,
                    "current_opportunities": current_opportunities
                }
            }
            
            # Create complete data context
            state["complete_data_context"] = self._create_complete_data_context(
                impact_data, status_data, years
            )
            
            # Update basic context summary
            state["context_summary"] = (
                f"Simulation completed for {years} years. "
                f"Total technologies: {total_techs}, "
                f"Technologies with positive impact: {active_techs}, "
                f"Maximum single-year impact: {max_impact:.1f} TWh, "
                f"Investment opportunities in {current_year}: {current_opportunities}."
            )
            
        except Exception as e:
            print(f"Error running simulation: {e}")
            state["simulation_results"] = None
            state["complete_data_context"] = ""
            state["context_summary"] = f"Error running simulation: {str(e)}"
        
        return state
    
    def _answer_question(self, state: SimulationState) -> SimulationState:
        """Answer questions about existing simulation data using complete data context."""
        user_query = state["user_query"]
        context = state.get("context_summary", "No simulation data available.")
        complete_context = state.get("complete_data_context", "")
        
        # Use the complete data context for much more accurate answers
        qa_prompt = f"""
        You are an expert assistant helping users understand nuclear technology 
        acceleration simulation results. You have access to complete simulation data
        including raw impact values, technology information, and dashboard data.
        
        Answer the user's question based on the comprehensive data provided below.
        Be specific and accurate, using exact values from the data when possible.
        
        COMPLETE SIMULATION DATA AND CONTEXT:
        {complete_context}
        
        BASIC SIMULATION SUMMARY:
        {context}
        
        USER QUESTION: "{user_query}"
        
        INSTRUCTIONS:
        - Use specific technology names, years, and impact values from the data above
        - When discussing rankings or comparisons, use the actual data provided
        - If asked about specific years, refer to the year-by-year data
        - If asked about technology details, use the tech tree information
        - If asked about development status, use the technology status data
        - Be conversational but precise with numbers and facts
        - If the question requires data not available in the context, clearly state what additional information would be needed
        
        Provide a helpful, detailed answer using the specific data above.
        """
        
        try:
            chat_config = types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1000,
            )
            chat = self.client.chats.create(
                model="gemini-2.0-flash-001",
                config=chat_config,
            )
            
            response_text = ""
            for chunk in chat.send_message_stream(qa_prompt):
                response_text += chunk.text
                
            state["response"] = response_text
            
        except Exception as e:
            print(f"Error answering question: {e}")
            state["response"] = f"Sorry, I encountered an error while processing your question: {str(e)}"
        
        return state
    
    def _format_response(self, state: SimulationState) -> SimulationState:
        """Format the final response based on the action taken."""
        current_intent = state["simulation_request"]["intent"]
        
        if current_intent == "simulation":
            if state["simulation_results"]:
                years = state["simulation_results"]["years_simulated"]
                stats = state["simulation_results"]["summary_stats"]
                
                response = f"""
## Simulation Complete

I've successfully run a {years}-year simulation of nuclear technology acceleration impacts.

### Key Results:
- {stats['active_techs']} technologies with positive impact potential
- {stats['max_impact']:.1f} TWh maximum single-year impact
- {stats['current_opportunities']} investment opportunities available in 2025

### What's Next:
- Explore the heatmap to identify high-impact technologies by year
- Adjust filters in the sidebar to focus on specific impact thresholds

### Follow-up Questions You Can Ask:
- "What are the top 5 technologies by total impact?"
- "Which technology shows the most growth potential?"

The dashboard is now updated with your new simulation data spanning {2025} to {2025 + years - 1}. 
I have complete access to all the raw data, so feel free to ask detailed questions!
                """.strip()
            else:
                response = "❌ Sorry, there was an error running the simulation. Please try again or contact support if the issue persists."
        else:
            # For questions, use the response from _answer_question
            response = state.get("response", "Sorry, I couldn't process your question.")
        
        state["response"] = response
        return state
    
    def process_user_input(self, user_query: str, current_context: str = "", current_complete_context: str = "") -> Dict[str, Any]:
        """Process user input through the workflow."""
        initial_state = {
            "messages": [],
            "user_query": user_query,
            "simulation_request": None,
            "simulation_results": None,
            "context_summary": current_context,
            "complete_data_context": current_complete_context,
            "response": ""
        }
        
        # Run the workflow
        result = self.graph.invoke(initial_state)
        
        return {
            "response": result["response"],
            "simulation_results": result.get("simulation_results"),
            "intent": result["simulation_request"]["intent"],
            "context_summary": result["context_summary"],
            "complete_data_context": result.get("complete_data_context", current_complete_context)
        }