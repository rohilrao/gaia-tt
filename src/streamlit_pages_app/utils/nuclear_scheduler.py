# utils/nuclear_scheduler.py
import json
import copy
from datetime import datetime
import sys
from functools import reduce
import operator

sys.setrecursionlimit(2000)

# --- Model Configuration & Assumptions ---
DISCOUNT_RATE = 0.05
YEARS_OF_OPERATION = 60
AVG_PLANT_CAPACITY_MW = 1000
CAPACITY_FACTOR = 0.90
CURRENT_YEAR = datetime.now().year
TRL_PROBABILITY_MAP = {
    "1": 0.10, "2": 0.20, "2-3": 0.25, "3": 0.30, "3-4": 0.40,
    "4": 0.50, "4-5": 0.60, "5": 0.70, "5-6": 0.75, "6": 0.80,
    "6-7": 0.85, "7": 0.90, "7-8": 0.95, "8": 0.98, "9": 1.0,
    "default": 0.6
}
MWH_TO_TWH = 1_000_000

class NuclearScheduler:
    """
    A dynamic scheduler that simulates year-by-year progress and allocates
    acceleration resources to the highest-impact milestones.
    This version correctly models that R&D work reduces both time and risk,
    and correctly calculates impact based on affected pathways only.
    """
    def __init__(self, graph_data):
        self.nodes = {node['id']: node for node in graph_data['graph']['nodes']}
        self.edges = graph_data['graph']['edges']
        self.dependencies = self._build_dependency_map()
        self.successors = self._build_successor_map()
        self.memoization_cache = {}
        self.recursion_stack = set()

    def _build_dependency_map(self):
        deps = {node_id: [] for node_id in self.nodes}
        for edge in self.edges:
            source_id = edge['source']
            targets = edge.get('targets', [edge.get('target')])
            for target_id in targets:
                if target_id and target_id in deps:
                    deps[target_id].append(source_id)
        return deps

    def _build_successor_map(self):
        succ = {node_id: [] for node_id in self.nodes}
        for edge in self.edges:
            source_id = edge['source']
            targets = edge.get('targets', [edge.get('target')])
            for target_id in targets:
                 if source_id and source_id in succ:
                    succ[source_id].append(target_id)
        return succ

    def _get_downstream_concepts(self, start_node_id):
        """Find all final reactor concepts that depend on a given start node."""
        concepts = set()
        q = [start_node_id]
        visited = set()
        while q:
            curr_id = q.pop(0)
            if curr_id in visited:
                continue
            visited.add(curr_id)

            node = self.nodes.get(curr_id)
            if node and node.get('type') == 'ReactorConcept':
                concepts.add(curr_id)

            for succ_id in self.successors.get(curr_id, []):
                if succ_id not in visited:
                    q.append(succ_id)
        return list(concepts)

    def _get_initial_prob(self, node):
        trl_str = node.get('trl_current', 'default')
        if ' ' in trl_str: trl_str = trl_str.split(' ')[0]
        if ';' in trl_str: trl_str = trl_str.split(';')[0].strip()
        return TRL_PROBABILITY_MAP.get(trl_str, TRL_PROBABILITY_MAP['default'])

    def _find_critical_path(self, node_id, current_nodes):
        if node_id in self.recursion_stack: return (float('inf'), 0.0)
        if node_id in self.memoization_cache: return self.memoization_cache[node_id]

        node = current_nodes.get(node_id)
        if not node: return 0, 1.0

        self.recursion_stack.add(node_id)

        time_for_this_node = node.get('time_remaining', 0)
        prob_of_this_node = node.get('prob_of_success', 1.0)

        prereq_ids = self.dependencies.get(node_id, [])
        if not prereq_ids:
            self.recursion_stack.remove(node_id)
            return time_for_this_node, prob_of_this_node

        prereq_times = []
        prereq_probs = []
        for prereq_id in prereq_ids:
            prereq_time, prereq_prob = self._find_critical_path(prereq_id, current_nodes)
            prereq_times.append(prereq_time)
            prereq_probs.append(prereq_prob)

        max_prereq_time = max(prereq_times) if prereq_times else 0.0
        combined_prereq_prob = reduce(operator.mul, prereq_probs, 1)

        total_time = time_for_this_node + max_prereq_time
        total_prob = prob_of_this_node * combined_prereq_prob

        self.recursion_stack.remove(node_id)
        self.memoization_cache[node_id] = (total_time, total_prob)
        return total_time, total_prob

    def _calculate_discounted_mwh(self, deployment_year):
        if deployment_year == float('inf'): return 0
        annual_mwh = AVG_PLANT_CAPACITY_MW * CAPACITY_FACTOR * 24 * 365
        total_discounted_mwh = sum(
            annual_mwh / ((1 + DISCOUNT_RATE) ** (deployment_year + i - CURRENT_YEAR))
            for i in range(YEARS_OF_OPERATION) if deployment_year + i > CURRENT_YEAR
        )
        return total_discounted_mwh

    def _calculate_pathway_mwh(self, nodes_to_sim, concept_ids):
        """Calculates the total expected MWh for a specific list of concepts."""
        self.memoization_cache.clear()
        total_expected_mwh = 0
        for concept_id in concept_ids:
            time_to_deploy, prob_of_success = self._find_critical_path(concept_id, nodes_to_sim)
            deployment_year = CURRENT_YEAR + time_to_deploy
            potential_mwh = self._calculate_discounted_mwh(deployment_year)
            total_expected_mwh += potential_mwh * prob_of_success
        return total_expected_mwh

    def run_simulation(self, years_to_simulate=20):
        sim_nodes = copy.deepcopy(self.nodes)
        for node_id, node in sim_nodes.items():
            initial_time = 0

            if 'trl_projected_5_10_years' in node: initial_time = 7.5
            else:
                try:
                    trl_val = float(node.get('trl_current', '1').split('-')[0].split(' ')[0])
                    initial_time = (9 - trl_val) * 2.5
                except (ValueError, IndexError):
                    initial_time = 5.0

            node['initial_time'] = initial_time if initial_time > 0 else 0.1 # Avoid division by zero
            node['time_remaining'] = initial_time
            node['prob_of_success'] = self._get_initial_prob(node)
            node['is_complete'] = True if initial_time <= 0 else False

        impact_table = {node['label']: {} for node in self.nodes.values() if node.get('type') in ['Milestone', 'EnablingTechnology']}
        status_table = {node['label']: {} for node in self.nodes.values() if node.get('type') in ['Milestone', 'EnablingTechnology']}

        for year in range(CURRENT_YEAR, CURRENT_YEAR + years_to_simulate):
            for node_id, node in sim_nodes.items():
                if node.get('type') not in ['Milestone', 'EnablingTechnology']: continue

                prereqs = self.dependencies.get(node_id, [])
                is_active = all(sim_nodes[pid]['is_complete'] for pid in prereqs)

                if node['is_complete']:
                    status_table[node['label']][year] = "Completed"
                    continue

                if is_active:
                    status_table[node['label']][year] = "Active"
                    if node['time_remaining'] > 0:
                        node['time_remaining'] -= 1
                        risk_reduction_per_year = (1 - self._get_initial_prob(node)) / node['initial_time']
                        node['prob_of_success'] += risk_reduction_per_year
                    if node['time_remaining'] <= 0:
                        node['is_complete'] = True
                        node['prob_of_success'] = 1.0
                else:
                    status_table[node['label']][year] = "Pending"

            for node_id, node in sim_nodes.items():
                if node.get('type') not in ['Milestone', 'EnablingTechnology']: continue
                if node['is_complete']: continue
                if status_table[node['label']].get(year) == "Active":
                    # Find all final concepts affected by this node
                    affected_concepts = self._get_downstream_concepts(node_id)
                    if not affected_concepts: continue

                    # Calculate baseline MWh for only the affected concepts
                    baseline_mwh = self._calculate_pathway_mwh(sim_nodes, affected_concepts)

                    temp_nodes = copy.deepcopy(sim_nodes)

                    # Apply acceleration (time and risk reduction)
                    temp_nodes[node_id]['time_remaining'] -= 1
                    risk_reduction_per_year = (1 - self._get_initial_prob(temp_nodes[node_id])) / temp_nodes[node_id]['initial_time']
                    temp_nodes[node_id]['prob_of_success'] += risk_reduction_per_year

                    # Calculate accelerated MWh for only the affected concepts
                    accelerated_mwh = self._calculate_pathway_mwh(temp_nodes, affected_concepts)

                    impact_twh = (accelerated_mwh - baseline_mwh) / MWH_TO_TWH
                    if impact_twh > 0.001:
                        impact_table[node['label']][year] = impact_twh

        return impact_table, status_table


class StrategicNuclearScheduler(NuclearScheduler):
    """
    Extended scheduler that calculates long-term cumulative impact of investments
    rather than just immediate year-over-year effects.
    """
    
    def __init__(self, graph_data):
        super().__init__(graph_data)
        self.simulation_horizon = 30  # years to look ahead
        
    def calculate_cumulative_impact(self, investment_tech_id, investment_year, 
                                  years_ahead=20, discount_rate=0.05):
        """
        Calculate the cumulative impact of investing in a specific technology
        in a specific year, looking years_ahead into the future.
        
        Args:
            investment_tech_id: ID of technology to accelerate
            investment_year: Year to make the investment
            years_ahead: How many years to simulate forward
            discount_rate: Discount rate for future benefits
            
        Returns:
            dict with baseline_twh, accelerated_twh, cumulative_impact_twh
        """
        
        # Run baseline simulation (no acceleration)
        baseline_results = self._run_forward_simulation(
            start_year=investment_year, 
            years_to_simulate=years_ahead,
            accelerated_tech=None
        )
        
        # Run accelerated simulation (with investment)
        accelerated_results = self._run_forward_simulation(
            start_year=investment_year,
            years_to_simulate=years_ahead, 
            accelerated_tech=investment_tech_id
        )
        
        # Calculate cumulative discounted energy production
        baseline_cumulative = self._calculate_discounted_cumulative_energy(
            baseline_results, investment_year, discount_rate
        )
        
        accelerated_cumulative = self._calculate_discounted_cumulative_energy(
            accelerated_results, investment_year, discount_rate
        )
        
        return {
            'investment_tech': investment_tech_id,
            'investment_year': investment_year,
            'baseline_twh': baseline_cumulative,
            'accelerated_twh': accelerated_cumulative,
            'cumulative_impact_twh': accelerated_cumulative - baseline_cumulative,
            'roi_multiple': accelerated_cumulative / baseline_cumulative if baseline_cumulative > 0 else float('inf')
        }
    
    def _run_forward_simulation(self, start_year, years_to_simulate, accelerated_tech=None):
        """
        Run a forward simulation starting from start_year.
        If accelerated_tech is specified, accelerate that technology in year 1.
        
        Returns:
            dict with yearly deployment data for each reactor concept
        """
        # Initialize simulation state
        sim_nodes = copy.deepcopy(self.nodes)
        
        # Set up initial conditions
        for node_id, node in sim_nodes.items():
            initial_time = self._get_initial_time_estimate(node)
            node['initial_time'] = initial_time
            node['time_remaining'] = initial_time
            node['prob_of_success'] = self._get_initial_prob(node)
            node['is_complete'] = initial_time <= 0
            node['deployment_year'] = None
            node['deployed_capacity_mw'] = 0
        
        # Track results
        yearly_results = {}
        
        # Run year-by-year simulation
        for year_offset in range(years_to_simulate):
            current_year = start_year + year_offset
            yearly_results[current_year] = {}
            
            # Apply acceleration in first year if specified
            if year_offset == 0 and accelerated_tech and accelerated_tech in sim_nodes:
                self._apply_acceleration(sim_nodes[accelerated_tech])
            
            # Update all technologies
            self._advance_technologies_one_year(sim_nodes)
            
            # Check for new deployments
            newly_deployed = self._check_for_deployments(sim_nodes, current_year)
            
            # Calculate energy production from all deployed concepts
            total_energy_twh = self._calculate_yearly_energy_production(sim_nodes, current_year)
            
            yearly_results[current_year] = {
                'total_energy_twh': total_energy_twh,
                'newly_deployed': newly_deployed,
                'deployed_concepts': {node_id: node for node_id, node in sim_nodes.items() 
                                    if node.get('deployment_year') and node['deployment_year'] <= current_year}
            }
            
        return yearly_results
    
    def _apply_acceleration(self, node):
        """Apply 1-year acceleration and risk reduction to a technology node."""
        if node['time_remaining'] > 0:
            node['time_remaining'] = max(0, node['time_remaining'] - 1)
            
            # Risk reduction
            if node['initial_time'] > 0:
                risk_reduction = (1 - self._get_initial_prob(node)) / node['initial_time']
                node['prob_of_success'] = min(1.0, node['prob_of_success'] + risk_reduction)
    
    def _advance_technologies_one_year(self, sim_nodes):
        """Advance all active technologies by one year."""
        for node_id, node in sim_nodes.items():
            if node.get('type') not in ['Milestone', 'EnablingTechnology']:
                continue
                
            if node['is_complete']:
                continue
                
            # Check if prerequisites are met
            prereqs = self.dependencies.get(node_id, [])
            is_active = all(sim_nodes[pid]['is_complete'] for pid in prereqs)
            
            if is_active and node['time_remaining'] > 0:
                node['time_remaining'] -= 1
                
                # Natural risk reduction over time
                if node['initial_time'] > 0:
                    risk_reduction = (1 - self._get_initial_prob(node)) / node['initial_time']
                    node['prob_of_success'] = min(1.0, node['prob_of_success'] + risk_reduction)
                
                # Mark as complete if time is up
                if node['time_remaining'] <= 0:
                    node['is_complete'] = True
                    node['prob_of_success'] = 1.0
    
    def _check_for_deployments(self, sim_nodes, current_year):
        """Check if any reactor concepts can be deployed this year."""
        newly_deployed = []
        
        for node_id, node in sim_nodes.items():
            if node.get('type') != 'ReactorConcept':
                continue
                
            if node.get('deployment_year'):  # Already deployed
                continue
            
            # Check if all dependencies are complete
            prereqs = self.dependencies.get(node_id, [])
            all_prereqs_complete = all(sim_nodes[pid]['is_complete'] for pid in prereqs)
            
            if all_prereqs_complete:
                # Calculate deployment probability based on critical path
                _, deployment_prob = self._find_critical_path(node_id, sim_nodes)
                
                # For simulation purposes, deploy if probability > threshold
                # In reality, you might want to model stochastic deployment
                if deployment_prob > 0.7:  # 70% threshold for commercial deployment
                    node['deployment_year'] = current_year
                    node['deployed_capacity_mw'] = AVG_PLANT_CAPACITY_MW
                    newly_deployed.append(node_id)
        
        return newly_deployed
    
    def _calculate_yearly_energy_production(self, sim_nodes, current_year):
        """Calculate total energy production in TWh for the current year."""
        total_energy_mwh = 0
        
        for node_id, node in sim_nodes.items():
            if node.get('type') != 'ReactorConcept':
                continue
                
            deployment_year = node.get('deployment_year')
            if deployment_year and deployment_year <= current_year:
                # Years of operation
                years_operating = current_year - deployment_year + 1
                
                # Energy production (with ramp-up in first year)
                if years_operating == 1:
                    # Assume 50% capacity in first year
                    annual_energy = node['deployed_capacity_mw'] * CAPACITY_FACTOR * 24 * 365 * 0.5
                else:
                    annual_energy = node['deployed_capacity_mw'] * CAPACITY_FACTOR * 24 * 365
                
                total_energy_mwh += annual_energy
        
        return total_energy_mwh / MWH_TO_TWH
    
    def _calculate_discounted_cumulative_energy(self, yearly_results, start_year, discount_rate):
        """Calculate net present value of all energy production."""
        cumulative_discounted_twh = 0
        
        for year, results in yearly_results.items():
            years_from_start = year - start_year
            discount_factor = 1 / ((1 + discount_rate) ** years_from_start)
            discounted_energy = results['total_energy_twh'] * discount_factor
            cumulative_discounted_twh += discounted_energy
            
        return cumulative_discounted_twh
    
    def _get_initial_time_estimate(self, node):
        """Get initial time estimate for a technology node."""
        if 'trl_projected_5_10_years' in node:
            return 7.5
        else:
            try:
                trl_val = float(node.get('trl_current', '1').split('-')[0].split(' ')[0])
                return max(0.1, (9 - trl_val) * 2.5)
            except (ValueError, IndexError):
                return 5.0
    
    def find_optimal_long_term_investment(self, current_year, years_ahead=20, 
                                        candidate_techs=None):
        """
        Find the technology that would have the highest cumulative impact
        if accelerated in the current year.
        
        Args:
            current_year: Year to make investment decision
            years_ahead: How many years to simulate forward
            candidate_techs: List of tech IDs to consider (None = all active techs)
            
        Returns:
            List of investment options sorted by cumulative impact
        """
        if candidate_techs is None:
            # Get only truly active technologies that can be accelerated
            candidate_techs = self._get_truly_active_technologies(current_year)
        
        investment_options = []
        
        for tech_id in candidate_techs:
            try:
                impact_analysis = self.calculate_cumulative_impact(
                    investment_tech_id=tech_id,
                    investment_year=current_year,
                    years_ahead=years_ahead
                )
                investment_options.append(impact_analysis)
            except Exception as e:
                print(f"Error analyzing {tech_id}: {e}")
                continue
        
        # Sort by cumulative impact (descending), then filter out zero-impact options
        investment_options.sort(key=lambda x: x['cumulative_impact_twh'], reverse=True)
        
        # Separate options with positive impact from zero-impact options
        positive_impact = [opt for opt in investment_options if opt['cumulative_impact_twh'] > 0.001]
        zero_impact = [opt for opt in investment_options if opt['cumulative_impact_twh'] <= 0.001]
        
        # Return positive impact options first, then zero impact ones (for debugging)
        return positive_impact + zero_impact
    
    def _get_truly_active_technologies(self, current_year):
        """
        Get list of technologies that are actually active and ready for acceleration.
        This is more sophisticated than just returning all techs.
        """
        # For now, we'll use the original simulation to determine what's actually active
        impact_data, status_data = self.run_simulation(years_to_simulate=1)
        
        active_techs = []
        for tech_name, yearly_data in impact_data.items():
            if current_year in yearly_data and yearly_data[current_year] > 0.001:
                # Find the node ID that matches this tech name
                for node_id, node in self.nodes.items():
                    if node['label'] == tech_name:
                        active_techs.append(node_id)
                        break
        
        return active_techs
    
    def _get_active_technologies(self, current_year):
        """Get list of technologies that could be accelerated in the current year."""
        # For this example, return all milestone and enabling tech IDs
        # In practice, you'd run a partial simulation to see what's active
        active_techs = []
        for node_id, node in self.nodes.items():
            if node.get('type') in ['Milestone', 'EnablingTechnology']:
                active_techs.append(node_id)
        return active_techs