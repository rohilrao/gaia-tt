"""
LangGraph workflow for handling nuclear simulation requests and questions.
This workflow can either run simulations or answer questions about existing results.
"""

import json
from typing import Dict, Any, List, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import google.genai as genai
from google.genai import types

from utils.nuclear_scheduler import NuclearScheduler
from utils.tech_tree_data import tech_tree


class SimulationState(TypedDict):
    """State for the simulation workflow."""
    messages: Annotated[List[Dict[str, str]], add_messages]
    user_query: str
    simulation_request: Optional[Dict[str, Any]]
    simulation_results: Optional[Dict[str, Any]]
    context_summary: str
    response: str


class NuclearSimulationWorkflow:
    """LangGraph workflow for nuclear simulation and analysis."""
    
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
            
            # Update context
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
            state["context_summary"] = f"Error running simulation: {str(e)}"
        
        return state
    
    def _answer_question(self, state: SimulationState) -> SimulationState:
        """Answer questions about existing simulation data."""
        user_query = state["user_query"]
        context = state.get("context_summary", "No simulation data available.")
        
        qa_prompt = f"""
        You are an expert assistant helping users understand nuclear technology 
        acceleration simulation results. Answer the user's question based on the 
        current simulation context.
        
        Current simulation context: {context}
        
        User question: "{user_query}"
        
        Provide a helpful, detailed answer. If you need more specific data to answer 
        the question properly, suggest that the user run a new simulation or ask 
        for specific details.
        """
        
        try:
            chat_config = types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=800,
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
        if state["simulation_request"]["intent"] == "simulation":
            if state["simulation_results"]:
                years = state["simulation_results"]["years_simulated"]
                stats = state["simulation_results"]["summary_stats"]
                
                response = f"""
## Simulation Complete! 

I've successfully run a **{years}-year simulation** of nuclear technology acceleration impacts.

### Key Results:
- **{stats['total_techs']}** technologies analyzed
- **{stats['active_techs']}** technologies with positive impact potential
- **{stats['max_impact']:.1f} TWh** maximum single-year impact
- **{stats['current_opportunities']}** investment opportunities available in 2025

The dashboard above has been updated with these new results. You can now explore the heatmap and analyze the data in detail.

### What you can explore:
- Use the heatmap to identify high-impact technologies by year
- Adjust the minimum impact threshold in the sidebar
- Select specific years to see detailed investment opportunities
- Ask me follow-up questions about the results!

*Would you like me to highlight any specific insights from this simulation?*
                """.strip()
            else:
                response = "Sorry, there was an error running the simulation. Please try again or contact support if the issue persists."
        else:
            # For questions, the response is already in state["response"]
            response = state.get("response", "Sorry, I couldn't process your question.")
        
        state["response"] = response
        return state
    
    def process_user_input(self, user_query: str, current_context: str = "") -> Dict[str, Any]:
        """Process user input through the workflow."""
        initial_state = {
            "messages": [],
            "user_query": user_query,
            "simulation_request": None,
            "simulation_results": None,
            "context_summary": current_context,
            "response": ""
        }
        
        # Run the workflow
        result = self.graph.invoke(initial_state)
        
        return {
            "response": result["response"],
            "simulation_results": result.get("simulation_results"),
            "intent": result["simulation_request"]["intent"],
            "context_summary": result["context_summary"]
        }