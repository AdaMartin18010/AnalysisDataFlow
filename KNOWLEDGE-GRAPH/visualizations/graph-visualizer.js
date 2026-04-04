/**
 * AnalysisDataFlow Knowledge Graph Visualizer
 * Interactive D3.js-based graph visualization
 */

class GraphVisualizer {
    constructor() {
        this.svg = d3.select("#graph");
        this.container = this.svg.append("g");
        this.width = 0;
        this.height = 0;
        this.zoom = d3.zoom();
        this.simulation = null;
        
        this.currentGraph = null;
        this.currentData = { nodes: [], edges: [] };
        this.selectedNode = null;
        this.visibleTypes = new Set();
        
        this.graphFiles = {
            "streaming-theory": "../data/streaming-theory-graph.json",
            "flink-technology": "../data/flink-technology-graph.json",
            "design-patterns": "../data/design-patterns-graph.json",
            "concept-dependency": "../data/concept-dependency-graph.json",
            "tech-decision": "../data/tech-decision-graph.json",
            "learning-path": "../data/learning-path-graph.json"
        };
        
        this.init();
    }
    
    init() {
        this.setupSVG();
        this.setupZoom();
        this.setupEventListeners();
        this.loadGraph("streaming-theory");
    }
    
    setupSVG() {
        const container = document.getElementById("graph-container");
        this.width = container.clientWidth;
        this.height = container.clientHeight;
        
        this.svg
            .attr("width", this.width)
            .attr("height", this.height)
            .attr("viewBox", [0, 0, this.width, this.height]);
    }
    
    setupZoom() {
        this.zoom
            .scaleExtent([0.1, 4])
            .on("zoom", (event) => {
                this.container.attr("transform", event.transform);
            });
        
        this.svg.call(this.zoom);
    }
    
    setupEventListeners() {
        // Graph selector
        document.getElementById("graph-selector").addEventListener("change", (e) => {
            this.loadGraph(e.target.value);
        });
        
        // Layout selector
        document.getElementById("layout-selector").addEventListener("change", (e) => {
            this.applyLayout(e.target.value);
        });
        
        // Search
        const searchInput = document.getElementById("search-input");
        searchInput.addEventListener("input", (e) => {
            this.handleSearch(e.target.value);
        });
        
        // Toolbar buttons
        document.getElementById("btn-zoom-in").addEventListener("click", () => {
            this.svg.transition().call(this.zoom.scaleBy, 1.3);
        });
        
        document.getElementById("btn-zoom-out").addEventListener("click", () => {
            this.svg.transition().call(this.zoom.scaleBy, 0.7);
        });
        
        document.getElementById("btn-fit").addEventListener("click", () => {
            this.fitToScreen();
        });
        
        document.getElementById("btn-reset").addEventListener("click", () => {
            this.resetView();
        });

        // Export panel
        const exportBtn = document.getElementById("btn-export");
        const exportPanel = document.getElementById("export-panel");
        exportBtn.addEventListener("click", () => {
            exportPanel.classList.toggle("visible");
        });

        // Export buttons
        document.querySelectorAll(".export-btn").forEach(btn => {
            btn.addEventListener("click", (e) => {
                const format = e.target.dataset.format;
                this.exportGraph(format);
                exportPanel.classList.remove("visible");
            });
        });

        // Close export panel on outside click
        document.addEventListener("click", (e) => {
            if (!exportBtn.contains(e.target) && !exportPanel.contains(e.target)) {
                exportPanel.classList.remove("visible");
            }
        });
        
        // Window resize
        window.addEventListener("resize", () => {
            this.setupSVG();
            if (this.simulation) {
                this.simulation.force("center", d3.forceCenter(this.width / 2, this.height / 2));
                this.simulation.alpha(0.3).restart();
            }
        });
    }
    
    async loadGraph(graphName) {
        document.getElementById("loading").style.display = "block";
        
        try {
            const response = await fetch(this.graphFiles[graphName]);
            this.currentGraph = await response.json();
            
            this.processData();
            this.updateTypeFilters();
            this.updateLegend();
            this.render();
            this.updateStats();
        } catch (error) {
            console.error("Failed to load graph:", error);
            alert("加载图谱失败，请检查数据文件");
        } finally {
            document.getElementById("loading").style.display = "none";
        }
    }
    
    processData() {
        const nodes = this.currentGraph.nodes.map(n => ({
            ...n,
            radius: this.getNodeRadius(n),
            color: this.getNodeColor(n)
        }));
        
        const edges = this.currentGraph.edges.map(e => ({
            ...e,
            source: e.source,
            target: e.target,
            color: this.getEdgeColor(e),
            width: this.getEdgeWidth(e)
        }));
        
        this.currentData = { nodes, edges };
        
        // Initialize visible types
        const types = new Set(nodes.map(n => n.type || n.category));
        this.visibleTypes = types;
    }
    
    getNodeRadius(node) {
        if (node.importance) return 5 + node.importance * 2;
        if (node.level) return 5 + node.level * 2;
        if (node.score) return 5 + node.score / 10;
        return 8;
    }
    
    getNodeColor(node) {
        const categories = this.currentGraph.categories || {};
        const cat = categories[node.category] || categories[node.type];
        if (cat) return cat.color;
        
        // Default colors based on node properties
        const colorMap = {
            "foundation": "#3498DB",
            "concept": "#2ECC71",
            "theorem": "#E74C3C",
            "model": "#9B59B6",
            "pattern": "#F39C12",
            "mechanism": "#1ABC9C",
            "decision-root": "#2C3E50",
            "decision": "#E67E22",
            "technology": "#D9534F",
            "choice": "#5BC0DE",
            "milestone": "#27AE60",
            "module": "#3498DB",
            "topic": "#9B59B6"
        };
        
        return colorMap[node.type] || colorMap[node.category] || "#7F8C8D";
    }
    
    getEdgeColor(edge) {
        const relationTypes = this.currentGraph.relationTypes || {};
        const rt = relationTypes[edge.type];
        if (rt) return rt.color;
        return "#666";
    }
    
    getEdgeWidth(edge) {
        return edge.weight || 1;
    }
    
    updateTypeFilters() {
        const container = document.getElementById("type-filters");
        container.innerHTML = "";
        
        const types = new Map();
        this.currentData.nodes.forEach(n => {
            const type = n.type || n.category;
            if (!types.has(type)) {
                types.set(type, { count: 0, color: n.color });
            }
            types.get(type).count++;
        });
        
        types.forEach((info, type) => {
            const item = document.createElement("label");
            item.className = "checkbox-item";
            item.innerHTML = `
                <input type="checkbox" checked data-type="${type}">
                <span class="color-dot" style="background: ${info.color}"></span>
                <span>${type} (${info.count})</span>
            `;
            container.appendChild(item);
        });
        
        // Add event listeners
        container.querySelectorAll("input[type='checkbox']").forEach(cb => {
            cb.addEventListener("change", (e) => {
                const type = e.target.dataset.type;
                if (e.target.checked) {
                    this.visibleTypes.add(type);
                } else {
                    this.visibleTypes.delete(type);
                }
                this.filterNodes();
            });
        });
    }
    
    updateLegend() {
        const container = document.getElementById("legend-content");
        container.innerHTML = "";
        
        // Node types
        if (this.currentGraph.categories) {
            const section = document.createElement("div");
            section.style.marginBottom = "12px";
            Object.entries(this.currentGraph.categories).forEach(([key, info]) => {
                const item = document.createElement("div");
                item.className = "legend-item";
                item.innerHTML = `
                    <span class="legend-symbol" style="background: ${info.color}"></span>
                    <span>${info.label}</span>
                `;
                section.appendChild(item);
            });
            container.appendChild(section);
        }
        
        // Edge types
        if (this.currentGraph.relationTypes) {
            const title = document.createElement("div");
            title.className = "control-label";
            title.textContent = "关系类型";
            title.style.marginTop = "12px";
            container.appendChild(title);
            
            Object.entries(this.currentGraph.relationTypes).forEach(([key, info]) => {
                const item = document.createElement("div");
                item.className = "legend-item";
                item.innerHTML = `
                    <span class="legend-line" style="background: ${info.color}"></span>
                    <span>${info.label}</span>
                `;
                container.appendChild(item);
            });
        }
    }
    
    render() {
        this.container.selectAll("*").remove();
        
        // Create arrow marker
        this.svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#666");
        
        // Draw edges
        const links = this.container.append("g")
            .attr("class", "links")
            .selectAll("line")
            .data(this.currentData.edges)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr("stroke", d => d.color)
            .attr("stroke-width", d => d.width)
            .attr("marker-end", "url(#arrowhead)");
        
        // Draw nodes
        const nodes = this.container.append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(this.currentData.nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(d3.drag()
                .on("start", (e, d) => this.dragstarted(e, d))
                .on("drag", (e, d) => this.dragged(e, d))
                .on("end", (e, d) => this.dragended(e, d)));
        
        nodes.append("circle")
            .attr("r", d => d.radius)
            .attr("fill", d => d.color)
            .attr("stroke", "#fff")
            .attr("stroke-width", 1.5);
        
        // Add labels for larger nodes or all nodes if count is low
        const nodeCount = this.currentData.nodes.length;
        if (nodeCount < 100) {
            nodes.append("text")
                .attr("class", "node-label")
                .attr("dy", d => d.radius + 12)
                .attr("text-anchor", "middle")
                .text(d => d.label.length > 15 ? d.label.substring(0, 12) + "..." : d.label);
        }
        
        // Add interaction
        nodes.on("click", (e, d) => {
            e.stopPropagation();
            this.selectNode(d);
        });
        
        nodes.on("mouseenter", (e, d) => {
            this.showTooltip(e, d);
        });
        
        nodes.on("mouseleave", () => {
            this.hideTooltip();
        });
        
        // Click background to deselect
        this.svg.on("click", () => {
            this.deselectNode();
        });
        
        // Setup simulation
        this.setupSimulation();
    }
    
    setupSimulation() {
        this.simulation = d3.forceSimulation(this.currentData.nodes)
            .force("link", d3.forceLink(this.currentData.edges)
                .id(d => d.id)
                .distance(100))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(this.width / 2, this.height / 2))
            .force("collision", d3.forceCollide().radius(d => d.radius + 10));
        
        this.simulation.on("tick", () => {
            this.container.selectAll(".link")
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
            
            this.container.selectAll(".node")
                .attr("transform", d => `translate(${d.x},${d.y})`);
        });
    }
    
    applyLayout(layoutType) {
        if (!this.simulation) return;
        
        switch (layoutType) {
            case "hierarchical":
                this.simulation.force("y", d3.forceY(d => {
                    const layers = this.currentGraph.layers || this.currentGraph.stages || {};
                    const layer = d.layer || d.stage || 0;
                    return (layer + 1) * (this.height / (Object.keys(layers).length + 2));
                }).strength(0.5));
                break;
                
            case "circular":
                const radius = Math.min(this.width, this.height) / 3;
                const angleStep = (2 * Math.PI) / this.currentData.nodes.length;
                this.currentData.nodes.forEach((d, i) => {
                    d.fx = this.width / 2 + radius * Math.cos(i * angleStep);
                    d.fy = this.height / 2 + radius * Math.sin(i * angleStep);
                });
                setTimeout(() => {
                    this.currentData.nodes.forEach(d => {
                        d.fx = null;
                        d.fy = null;
                    });
                }, 1000);
                break;
                
            case "grid":
                const cols = Math.ceil(Math.sqrt(this.currentData.nodes.length));
                const cellWidth = this.width / (cols + 1);
                const cellHeight = this.height / (cols + 1);
                this.currentData.nodes.forEach((d, i) => {
                    const col = i % cols;
                    const row = Math.floor(i / cols);
                    d.fx = (col + 1) * cellWidth;
                    d.fy = (row + 1) * cellHeight;
                });
                setTimeout(() => {
                    this.currentData.nodes.forEach(d => {
                        d.fx = null;
                        d.fy = null;
                    });
                }, 1000);
                break;
                
            default: // force
                this.simulation.force("y", null);
                break;
        }
        
        this.simulation.alpha(1).restart();
    }
    
    filterNodes() {
        this.container.selectAll(".node")
            .classed("dimmed", d => !this.visibleTypes.has(d.type || d.category));
        
        this.container.selectAll(".link")
            .classed("dimmed", d => {
                const sourceType = d.source.type || d.source.category;
                const targetType = d.target.type || d.target.category;
                return !this.visibleTypes.has(sourceType) || !this.visibleTypes.has(targetType);
            });
    }
    
    selectNode(node) {
        this.selectedNode = node;
        
        // Update visual state
        this.container.selectAll(".node")
            .classed("selected", d => d.id === node.id)
            .classed("dimmed", d => d.id !== node.id);
        
        // Highlight connected edges and nodes
        const connectedNodeIds = new Set();
        this.currentData.edges.forEach(e => {
            if (e.source.id === node.id) connectedNodeIds.add(e.target.id);
            if (e.target.id === node.id) connectedNodeIds.add(e.source.id);
        });
        
        this.container.selectAll(".node")
            .classed("highlighted", d => connectedNodeIds.has(d.id) || d.id === node.id)
            .classed("dimmed", d => !connectedNodeIds.has(d.id) && d.id !== node.id);
        
        this.container.selectAll(".link")
            .classed("highlighted", d => d.source.id === node.id || d.target.id === node.id)
            .classed("dimmed", d => d.source.id !== node.id && d.target.id !== node.id);
        
        // Update details panel
        this.updateNodeDetails(node, connectedNodeIds);
        
        // Update stats
        document.getElementById("stat-selected").textContent = node.label;
    }
    
    deselectNode() {
        this.selectedNode = null;
        
        this.container.selectAll(".node")
            .classed("selected", false)
            .classed("dimmed", false)
            .classed("highlighted", false);
        
        this.container.selectAll(".link")
            .classed("highlighted", false)
            .classed("dimmed", false);
        
        document.getElementById("node-details").innerHTML = `
            <div class="detail-empty">点击节点查看详情</div>
        `;
        
        document.getElementById("stat-selected").textContent = "-";
    }
    
    updateNodeDetails(node, connectedIds) {
        const container = document.getElementById("node-details");
        
        // Get connected nodes info
        const incoming = this.currentData.edges
            .filter(e => e.target.id === node.id)
            .map(e => ({ node: e.source, relation: e.type, label: e.label }));
        
        const outgoing = this.currentData.edges
            .filter(e => e.source.id === node.id)
            .map(e => ({ node: e.target, relation: e.type, label: e.label }));
        
        let html = `
            <div class="detail-card">
                <div class="detail-title">${node.label}</div>
                <div class="detail-row">
                    <span class="detail-label">ID</span>
                    <span class="detail-value">${node.id}</span>
                </div>
                <div class="detail-row">
                    <span class="detail-label">类型</span>
                    <span class="detail-value">${node.type || node.category || "-"}</span>
                </div>
        `;
        
        if (node.description) {
            html += `<div class="detail-description">${node.description}</div>`;
        }
        
        if (node.level) {
            html += `
                <div class="detail-row">
                    <span class="detail-label">级别</span>
                    <span class="detail-value">${node.level}</span>
                </div>
            `;
        }
        
        if (node.duration) {
            html += `
                <div class="detail-row">
                    <span class="detail-label">预计时长</span>
                    <span class="detail-value">${node.duration}</span>
                </div>
            `;
        }
        
        if (node.score) {
            html += `
                <div class="detail-row">
                    <span class="detail-label">评分</span>
                    <span class="detail-value">${node.score}/100</span>
                </div>
            `;
        }
        
        if (node.pros) {
            html += `
                <div class="detail-row" style="flex-direction: column; align-items: flex-start;">
                    <span class="detail-label">优点</span>
                    <span class="detail-value" style="max-width: 100%; margin-top: 4px;">${node.pros.join(", ")}</span>
                </div>
            `;
        }
        
        if (node.cons) {
            html += `
                <div class="detail-row" style="flex-direction: column; align-items: flex-start;">
                    <span class="detail-label">缺点</span>
                    <span class="detail-value" style="max-width: 100%; margin-top: 4px;">${node.cons.join(", ")}</span>
                </div>
            `;
        }
        
        html += `</div>`;
        
        // Incoming relations
        if (incoming.length > 0) {
            html += `
                <div class="detail-card">
                    <div class="detail-title">入边关系 (${incoming.length})</div>
                    <div class="related-nodes">
            `;
            incoming.forEach(({ node: n, relation, label }) => {
                html += `<span class="related-node" data-id="${n.id}">${label || relation}: ${n.label}</span>`;
            });
            html += `</div></div>`;
        }
        
        // Outgoing relations
        if (outgoing.length > 0) {
            html += `
                <div class="detail-card">
                    <div class="detail-title">出边关系 (${outgoing.length})</div>
                    <div class="related-nodes">
            `;
            outgoing.forEach(({ node: n, relation, label }) => {
                html += `<span class="related-node" data-id="${n.id}">${label || relation}: ${n.label}</span>`;
            });
            html += `</div></div>`;
        }
        
        // Prerequisites for learning path
        if (node.prerequisites && node.prerequisites.length > 0) {
            html += `
                <div class="detail-card">
                    <div class="detail-title">前置要求</div>
                    <div class="related-nodes">
            `;
            node.prerequisites.forEach(prereq => {
                const prereqNode = this.currentData.nodes.find(n => n.id === prereq);
                if (prereqNode) {
                    html += `<span class="related-node" data-id="${prereq}">${prereqNode.label}</span>`;
                }
            });
            html += `</div></div>`;
        }
        
        container.innerHTML = html;
        
        // Add click handlers for related nodes
        container.querySelectorAll(".related-node").forEach(el => {
            el.addEventListener("click", () => {
                const nodeId = el.dataset.id;
                const relatedNode = this.currentData.nodes.find(n => n.id === nodeId);
                if (relatedNode) {
                    this.selectNode(relatedNode);
                    // Center view on node
                    this.svg.transition().duration(750).call(
                        this.zoom.transform,
                        d3.zoomIdentity
                            .translate(this.width / 2, this.height / 2)
                            .scale(1.5)
                            .translate(-relatedNode.x, -relatedNode.y)
                    );
                }
            });
        });
    }
    
    handleSearch(query) {
        const resultsContainer = document.getElementById("search-results");
        
        if (!query.trim()) {
            resultsContainer.classList.remove("visible");
            return;
        }
        
        const matches = this.currentData.nodes.filter(n => 
            n.label.toLowerCase().includes(query.toLowerCase()) ||
            n.id.toLowerCase().includes(query.toLowerCase())
        );
        
        if (matches.length === 0) {
            resultsContainer.classList.remove("visible");
            return;
        }
        
        resultsContainer.innerHTML = matches.slice(0, 10).map(n => `
            <div class="search-result-item" data-id="${n.id}">
                <div>${n.label}</div>
                <div class="search-result-type">${n.type || n.category || "unknown"}</div>
            </div>
        `).join("");
        
        resultsContainer.classList.add("visible");
        
        // Add click handlers
        resultsContainer.querySelectorAll(".search-result-item").forEach(el => {
            el.addEventListener("click", () => {
                const nodeId = el.dataset.id;
                const node = this.currentData.nodes.find(n => n.id === nodeId);
                if (node) {
                    this.selectNode(node);
                    resultsContainer.classList.remove("visible");
                    document.getElementById("search-input").value = "";
                    
                    // Center view
                    this.svg.transition().duration(750).call(
                        this.zoom.transform,
                        d3.zoomIdentity
                            .translate(this.width / 2, this.height / 2)
                            .scale(1.5)
                            .translate(-node.x, -node.y)
                    );
                }
            });
        });
    }
    
    showTooltip(event, node) {
        const tooltip = document.getElementById("tooltip");
        tooltip.innerHTML = `
            <strong>${node.label}</strong><br>
            <span style="color: #9ca3af;">${node.type || node.category || ""}</span>
            ${node.description ? `<br><span style="font-size: 11px;">${node.description.substring(0, 100)}${node.description.length > 100 ? "..." : ""}</span>` : ""}
        `;
        tooltip.style.left = (event.pageX + 10) + "px";
        tooltip.style.top = (event.pageY + 10) + "px";
        tooltip.classList.add("visible");
    }
    
    hideTooltip() {
        document.getElementById("tooltip").classList.remove("visible");
    }
    
    updateStats() {
        document.getElementById("stat-nodes").textContent = this.currentData.nodes.length;
        document.getElementById("stat-edges").textContent = this.currentData.edges.length;
        document.getElementById("stat-categories").textContent = 
            Object.keys(this.currentGraph.categories || {}).length;
        document.getElementById("stat-selected").textContent = "-";
    }
    
    fitToScreen() {
        if (this.currentData.nodes.length === 0) return;
        
        const bounds = this.container.node().getBBox();
        const fullWidth = this.width;
        const fullHeight = this.height;
        const width = bounds.width;
        const height = bounds.height;
        const midX = bounds.x + width / 2;
        const midY = bounds.y + height / 2;
        
        if (width === 0 || height === 0) return;
        
        const scale = 0.8 / Math.max(width / fullWidth, height / fullHeight);
        const translate = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];
        
        this.svg.transition().duration(750).call(
            this.zoom.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
        );
    }
    
    resetView() {
        this.svg.transition().duration(750).call(
            this.zoom.transform,
            d3.zoomIdentity
        );
        this.deselectNode();
    }
    
    dragstarted(event, d) {
        if (!event.active) this.simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    
    dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }
    
    dragended(event, d) {
        if (!event.active) this.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    // Export functions
    exportGraph(format) {
        switch (format) {
            case "json":
                this.exportJSON();
                break;
            case "graphml":
                this.exportGraphML();
                break;
            case "cypher":
                this.exportCypher();
                break;
            case "png":
                this.exportPNG();
                break;
        }
    }

    exportJSON() {
        const dataStr = JSON.stringify(this.currentGraph, null, 2);
        this.downloadFile(dataStr, `knowledge-graph-${this.currentGraph.name}.json`, "application/json");
    }

    exportGraphML() {
        let xml = `<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns">
  <key id="label" for="node" attr.name="label" attr.type="string"/>
  <key id="type" for="node" attr.name="type" attr.type="string"/>
  <key id="category" for="node" attr.name="category" attr.type="string"/>
  <key id="description" for="node" attr.name="description" attr.type="string"/>
  <key id="relation" for="edge" attr.name="relation" attr.type="string"/>
  <graph id="${this.currentGraph.name}" edgedefault="directed">
`;
        
        this.currentData.nodes.forEach(node => {
            xml += `    <node id="${node.id}">
      <data key="label">${this.escapeXml(node.label)}</data>
      <data key="type">${node.type || ""}</data>
      <data key="category">${node.category || ""}</data>
      <data key="description">${this.escapeXml(node.description || "")}</data>
    </node>
`;
        });
        
        this.currentData.edges.forEach((edge, i) => {
            xml += `    <edge id="e${i}" source="${edge.source.id || edge.source}" target="${edge.target.id || edge.target}">
      <data key="relation">${edge.type}</data>
    </edge>
`;
        });
        
        xml += `  </graph>
</graphml>`;
        
        this.downloadFile(xml, `knowledge-graph-${this.currentGraph.name}.graphml`, "application/xml");
    }

    exportCypher() {
        let cypher = "// Knowledge Graph Cypher Export\n";
        cypher += `// Graph: ${this.currentGraph.name}\n`;
        cypher += `// Generated: ${new Date().toISOString()}\n\n`;
        
        // Create nodes
        cypher += "// Create nodes\n";
        this.currentData.nodes.forEach(node => {
            const props = {
                id: node.id,
                label: node.label,
                type: node.type || node.category || "unknown",
                description: node.description || ""
            };
            const propStr = Object.entries(props)
                .map(([k, v]) => `${k}: "${this.escapeCypher(v)}"`)
                .join(", ");
            cypher += `CREATE (:Concept {${propStr}})\n`;
        });
        
        cypher += "\n// Create relationships\n";
        this.currentData.edges.forEach(edge => {
            const sourceId = edge.source.id || edge.source;
            const targetId = edge.target.id || edge.target;
            cypher += `MATCH (a:Concept {id: "${sourceId}"}), (b:Concept {id: "${targetId}"})\n`;
            cypher += `CREATE (a)-[:${edge.type.toUpperCase().replace(/-/g, "_")} {label: "${edge.label || ""}"}]->(b)\n`;
        });
        
        this.downloadFile(cypher, `knowledge-graph-${this.currentGraph.name}.cypher`, "text/plain");
    }

    exportPNG() {
        const svgElement = this.svg.node();
        const svgData = new XMLSerializer().serializeToString(svgElement);
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const img = new Image();
        
        canvas.width = this.width;
        canvas.height = this.height;
        
        // Fill background
        ctx.fillStyle = "#0a0e17";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        img.onload = () => {
            ctx.drawImage(img, 0, 0);
            const pngUrl = canvas.toDataURL("image/png");
            this.downloadDataUrl(pngUrl, `knowledge-graph-${this.currentGraph.name}.png`);
        };
        
        img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData)));
    }

    downloadFile(content, filename, mimeType) {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        this.downloadDataUrl(url, filename);
        URL.revokeObjectURL(url);
    }

    downloadDataUrl(url, filename) {
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    escapeXml(str) {
        if (!str) return "";
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&apos;");
    }

    escapeCypher(str) {
        if (!str) return "";
        return str.replace(/"/g, '\\"').replace(/\\/g, "\\\\");
    }
}

// Initialize on load
document.addEventListener("DOMContentLoaded", () => {
    new GraphVisualizer();
});
