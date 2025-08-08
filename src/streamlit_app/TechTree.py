# app.py - Main Streamlit application (Home page)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from utils.nuclear_scheduler import NuclearScheduler, StrategicNuclearScheduler
from utils.tech_tree_data import tech_tree
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Tech Tree Investment Analyzer for Nuclear Tech",
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
        padding: 0.8rem;
        margin: 0.5rem 0;
        text-align: center;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .navigation-card h3 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .navigation-card p {
        font-size: 0.85rem;
        margin-bottom: 0.8rem;
        line-height: 1.3;
    }
    .navigation-card .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: 500;
        width: 100%;
        margin-top: 0.5rem;
    }
    .navigation-card .stButton > button:hover {
        background-color: #1565c0;
        color: white;
    }
    .metric-highlight {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .page-link-button {
        background-color: #1f77b4;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 5px;
        border: none;
        cursor: pointer;
    }
    .page-link-button:hover {
        background-color: #1565c0;
        color: white;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)

def create_tech_tree_html():
    """Create the D3.js tech tree visualization HTML"""
    # Convert your tech_tree data to JavaScript format
    tech_tree_js = f"""
    const tech_tree = {tech_tree};
    """
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dynamic Tech Tree</title>
    <style>
        body {{
            font-family: "Inter", sans-serif;
            background-color: #ffffff;
            margin: 0;
            padding: 10px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 12px;
            padding: 10px;
            width: 100%;
            max-width: 100%;
            margin-bottom: 10px;
            overflow: hidden;
        }}
        .graph-container {{
            width: 100%;
            height: 600px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            background-color: #ffffff;
            position: relative;
            overflow: hidden;
        }}
        svg {{
            width: 100%;
            height: 100%;
            display: block;
        }}
        .links line {{
            stroke: #999;
            stroke-opacity: 0.6;
            stroke-width: 2px;
            marker-end: url(#arrowhead);
        }}
        .links line.highlight-path {{
            stroke: #ff7f0e; /* A vibrant color for highlighted links */
            stroke-width: 4px;
            stroke-opacity: 1;
            marker-end: url(#arrowhead-highlight);
        }}
        .nodes circle {{
            stroke: #fff;
            stroke-width: 1.5px;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
        }}
        .nodes circle:hover {{
            transform: scale(1.1);
            stroke-width: 3px;
        }}
        .nodes circle.highlight-node {{
            stroke: #ff7f0e; /* A vibrant border for highlighted nodes */
            stroke-width: 3px;
            transform: scale(1.2); /* Make highlighted nodes slightly larger */
        }}
        .nodes text {{
            font-size: 9px;
            fill: #333;
            pointer-events: none;
            user-select: none;
            font-weight: 500;
        }}
        .nodes text.highlight-node {{
            font-weight: bold;
            fill: #ff7f0e;
        }}
        .node-info {{
            position: absolute;
            background-color: rgba(0, 0, 0, 0.85);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
            max-width: 250px;
            word-wrap: break-word;
            z-index: 100;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            font-size: 12px;
        }}
        .node-info.active {{
            opacity: 1;
        }}
        .legend {{
            margin-bottom: 15px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            padding: 12px;
            background-color: #f8fafc;
            border-radius: 8px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            font-size: 12px;
            color: #4a5568;
        }}
        .legend-color-box {{
            width: 16px;
            height: 16px;
            border-radius: 3px;
            margin-right: 6px;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }}
        .nav-controls {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .nav-button {{
            background-color: #1f77b4;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 500;
        }}
        .nav-button:hover {{
            background-color: #1565c0;
        }}
        .nav-button:active {{
            background-color: #0d47a1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color-box" style="background-color: #636efa;"></div>
                <span>Reactor Concept</span>
            </div>
            <div class="legend-item">
                <div class="legend-color-box" style="background-color: #00cc96;"></div>
                <span>Milestone</span>
            </div>
            <div class="legend-item">
                <div class="legend-color-box" style="background-color: #FFA15A;"></div>
                <span>Enabling Technology</span>
            </div>
        </div>
        <div class="nav-controls">
            <button class="nav-button" onclick="zoomIn()">🔍 Zoom In</button>
            <button class="nav-button" onclick="zoomOut()">🔍 Zoom Out</button>
            <button class="nav-button" onclick="resetView()">🏠 Reset View</button>
            <button class="nav-button" onclick="fitToScreen()">📐 Fit to Screen</button>
            <button class="nav-button" onclick="clearHighlight()">❌ Clear Highlight</button>
        </div>
        <div class="graph-container" id="graph-container">
            <div id="node-info" class="node-info"></div>
        </div>
    </div>

    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        {tech_tree_js}

        // Get the container dimensions
        const container = document.getElementById('graph-container');
        const nodeInfo = document.getElementById('node-info');
        let width = container.clientWidth;
        let height = container.clientHeight;

        // Function to update dimensions on resize
        const updateDimensions = () => {{
            width = container.clientWidth;
            height = container.clientHeight;
            if (svg) {{
                svg.attr("width", width).attr("height", height);
                simulation.force("center", d3.forceCenter(width / 2, height / 2));
                simulation.alpha(0.3).restart();
            }}
        }};

        // Create SVG element with zoom and pan
        const svg = d3.select(container).append("svg")
            .attr("viewBox", `0 0 ${{width}} ${{height}}`)
            .attr("preserveAspectRatio", "xMidYMid meet");

        // Create a group for zoomable content
        const g = svg.append("g");

        // Define zoom behavior
        const zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on("zoom", function(event) {{
                g.attr("transform", event.transform);
            }});

        // Apply zoom behavior to SVG
        svg.call(zoom);

        // Define arrowhead marker
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "-0 -5 10 10")
            .attr("refX", 13)
            .attr("refY", 0)
            .attr("orient", "auto")
            .attr("markerWidth", 8)
            .attr("markerHeight", 8)
            .attr("xoverflow", "visible")
            .append("svg:path")
            .attr("d", "M 0,-5 L 10,0 L 0,5")
            .attr("fill", "#999")
            .style("stroke", "none");

        // Define highlighted arrowhead marker
        svg.append("defs").append("marker")
            .attr("id", "arrowhead-highlight")
            .attr("viewBox", "-0 -5 10 10")
            .attr("refX", 13)
            .attr("refY", 0)
            .attr("orient", "auto")
            .attr("markerWidth", 8)
            .attr("markerHeight", 8)
            .attr("xoverflow", "visible")
            .append("svg:path")
            .attr("d", "M 0,-5 L 10,0 L 0,5")
            .attr("fill", "#ff7f0e")
            .style("stroke", "none");

        // Prepare data for D3
        const nodesData = tech_tree.graph.nodes;
        const linksData = [];
        const nodeMap = new Map();
        nodesData.forEach(node => nodeMap.set(node.id, node));

        tech_tree.graph.edges.forEach(edge => {{
            if (Array.isArray(edge.targets)) {{
                edge.targets.forEach(target => {{
                    linksData.push({{ source: edge.source, target: target }});
                }});
            }} else if (edge.target) {{
                linksData.push({{ source: edge.source, target: edge.target }});
            }}
        }});
        
        // Create a force simulation
        const simulation = d3.forceSimulation(nodesData)
            .force("link", d3.forceLink(linksData).id(d => d.id).distance(120))
            .force("charge", d3.forceManyBody().strength(-500))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("collide", d3.forceCollide(25));

        // Create links
        const link = g.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(linksData)
            .enter().append("line");

        // Create nodes
        const node = g.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(nodesData)
            .enter().append("g")
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended))
            .on("click", clickNode);

        node.append("circle")
            .attr("r", 8)
            .attr("fill", d => {{
                if (d.type === "ReactorConcept") return "#636efa";
                if (d.type === "Milestone") return "#00cc96";
                if (d.type === "EnablingTechnology") return "#FFA15A";
                return "#999";
            }});

        node.append("text")
            .attr("dx", 10)
            .attr("dy", ".35em")
            .text(d => d.label.length > 30 ? d.label.substring(0, 30) + "..." : d.label);

        // Tooltip / Node Info
        node.on("mouseover", function(event, d) {{
            let infoHtml = `<strong>${{d.label}}</strong><br>`;
            for (const key in d) {{
                if (key !== "id" && key !== "label" && key !== "x" && key !== "y" && key !== "vx" && key !== "vy") {{
                    infoHtml += `<strong>${{key.replace(/_/g, ' ').replace(/\\b\\w/g, c => c.toUpperCase())}}:</strong> ${{d[key]}}<br>`;
                }}
            }}
            nodeInfo.innerHTML = infoHtml;
            nodeInfo.classList.add('active');

            const mouseX = event.clientX;
            const mouseY = event.clientY;
            const containerRect = container.getBoundingClientRect();

            let tooltipX = mouseX - containerRect.left + 10;
            let tooltipY = mouseY - containerRect.top + 10;

            if (tooltipX + nodeInfo.offsetWidth > width) {{
                tooltipX = width - nodeInfo.offsetWidth - 10;
            }}
            if (tooltipY + nodeInfo.offsetHeight > height) {{
                tooltipY = height - nodeInfo.offsetHeight - 10;
            }}

            nodeInfo.style.left = `${{tooltipX}}px`;
            nodeInfo.style.top = `${{tooltipY}}px`;
        }})
        .on("mouseout", function() {{
            nodeInfo.classList.remove('active');
        }});

        // Update positions on each tick
        simulation.on("tick", () => {{
            link
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            node
                .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
        }});

        // --- NEW PATH HIGHLIGHTING LOGIC ---
        function findPath(startNodeId) {{
            const pathNodes = new Set();
            const pathLinks = new Set();

            // Find dependencies (ancestors)
            function findAncestors(nodeId) {{
                pathNodes.add(nodeId);
                linksData.forEach(link => {{
                    if (link.target.id === nodeId) {{
                        pathLinks.add(link);
                        findAncestors(link.source.id);
                    }}
                }});
            }}

            // Find technologies enabled by (descendants)
            function findDescendants(nodeId) {{
                pathNodes.add(nodeId);
                linksData.forEach(link => {{
                    if (link.source.id === nodeId) {{
                        pathLinks.add(link);
                        findDescendants(link.target.id);
                    }}
                }});
            }}

            // Start traversal from the clicked node
            findAncestors(startNodeId);
            findDescendants(startNodeId);

            return {{nodes: Array.from(pathNodes), links: Array.from(pathLinks)}};
        }}
        
        // Handles the node click event
        function clickNode(event, d) {{
            // Clear any previous highlights
            clearHighlight();

            // Find all nodes and links in the dependency path
            const path = findPath(d.id);

            // Highlight the nodes
            g.selectAll('.nodes g')
                .filter(nodeData => path.nodes.includes(nodeData.id))
                .select('circle')
                .classed('highlight-node', true);
            
            g.selectAll('.nodes g')
                .filter(nodeData => path.nodes.includes(nodeData.id))
                .select('text')
                .classed('highlight-node', true);

            // Highlight the links
            g.selectAll('.links line')
                .filter(linkData => path.links.includes(linkData))
                .classed('highlight-path', true);
        }}
        
        window.clearHighlight = function() {{
            g.selectAll('.nodes circle').classed('highlight-node', false);
            g.selectAll('.nodes text').classed('highlight-node', false);
            g.selectAll('.links line').classed('highlight-path', false);
        }};

        // Drag functions
        function dragstarted(event, d) {{
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }}

        function dragged(event, d) {{
            d.fx = event.x;
            d.fy = event.y;
        }}

        function dragended(event, d) {{
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }}

        // Handle window resize
        window.addEventListener('resize', updateDimensions);
        updateDimensions();

        // Navigation functions
        window.zoomIn = function() {{
            svg.transition().duration(300).call(
                zoom.scaleBy, 1.5
            );
        }};

        window.zoomOut = function() {{
            svg.transition().duration(300).call(
                zoom.scaleBy, 1 / 1.5
            );
        }};

        window.resetView = function() {{
            svg.transition().duration(500).call(
                zoom.transform,
                d3.zoomIdentity
            );
        }};

        window.fitToScreen = function() {{
            const bounds = g.node().getBBox();
            const fullWidth = width;
            const fullHeight = height;
            const widthScale = fullWidth / bounds.width;
            const heightScale = fullHeight / bounds.height;
            const scale = Math.min(widthScale, heightScale) * 0.9;
            const translate = [
                fullWidth / 2 - scale * (bounds.x + bounds.width / 2),
                fullHeight / 2 - scale * (bounds.y + bounds.height / 2)
            ];
            
            svg.transition().duration(750).call(
                zoom.transform,
                d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
            );
        }};
    </script>
</body>
</html>
    """
    return html_template

def main():
    # Title
    st.markdown('<div class="main-header">Investment Analyzer for Nuclear Tech</div>', 
                unsafe_allow_html=True)
    
    # Introduction
    # st.markdown("""
    # **A comprehensive analysis platform for nuclear technology R&D investment decisions combining short-term impact analysis with long-term strategic planning.**
    # """)
    
    # Tech Tree Visualization
    st.markdown('<div class="section-header">Interactive Tech Dependency Graph</div>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Explore the nuclear technology landscape below. Hover over nodes to see detailed information about each technology, milestone, or enabling capability. The arrows show key dependencies between technologies.
    """)
    
    # Display the D3.js tech tree
    components.html(create_tech_tree_html(), height=750, scrolling=True)
    
    # Navigation cards with working links
    st.markdown('<div class="section-header">Analysis Modules</div>', 
                unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown('''
            <div class="navigation-card">
                <h3>🔬 Impact Simulation</h3>
                <p><strong>See which technologies offer the best investment opportunities by year</strong></p>
            ''', unsafe_allow_html=True)
            
            # Working navigation button inside the card
            if st.button("Open Analysis", key="yearly_btn", help="Year-by-year impact assessment with interactive heatmaps"):
                st.switch_page("pages/1_Impact_Simulation.py")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="height: 160px;"></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="height: 160px;"></div>', unsafe_allow_html=True)

    # Technology Portfolio Overview as expandable section
    with st.expander("📊 Technology Portfolio Overview", expanded=False):
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
    
    # Key features as expandable section
    with st.expander("🔧 Key Features", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-box">
            
            ### Technology Modeling
            - **Impact Assessment**: Measures additional clean energy (TWh) from technology acceleration
            - **TRL-based Analysis**: Technology readiness levels inform deployment timelines
            - **Dependency Mapping**: Models technology interdependencies
            
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-box">
            
            ### Interactive Visualization
            - **Dynamic Heatmaps**: Year-by-year impact visualization
            - **Configurable Filters**: Focus on specific technology types or impact thresholds
            - **Chat Assistant**: AI-powered insights and questions about simulation results
            
            </div>
            """, unsafe_allow_html=True)
    
    # Methodology overview as expandable section
    with st.expander("📋 Methodology", expanded=False):
        st.markdown("""
        <div class="info-card">
        
        ### Analysis Framework
        
        **Impact Simulation**
        - Models accelerating each technology by one year
        - Calculates additional clean energy generation (TWh) over plant lifetime
        - Uses technology readiness levels and deployment timelines
        - Accounts for technology dependencies and prerequisites
        
        </div>
        """, unsafe_allow_html=True)
    
    # Configuration tips
    with st.expander("⚙️ Configuration Tips", expanded=False):
        st.markdown("""
        ### How to Use This Platform
        
        **Navigation**: Click "Open Analysis" above to access the Impact Simulation
        
        **Customization**: 
        - Adjust minimum impact threshold in the sidebar
        - Choose different color schemes for visualization
        - Filter technologies by impact levels
        - Use the chat assistant for insights about results
        """)
    
    # Data sources and assumptions
    with st.expander("Data Sources and Assumptions"):
        st.markdown("""
        ### Key Assumptions
        - **Average Plant Capacity**: 1,000 MW
        - **Capacity Factor**: 90%
        - **Plant Lifetime**: 60 years
        - **Simulation Period**: 30 years
        
        ### Model Focus
        - Technology acceleration impact measurement
        - Clean energy generation potential
        - Year-by-year investment opportunity analysis
        """)

if __name__ == "__main__":
    main()