/**
 * Proof Tree Visualization - Phase 2 Task 4-2
 * Interactive visualization of theorem dependency trees
 * 
 * Technology: D3.js v7
 * Features:
 * - Hierarchical tree layout
 * - Collapsible nodes
 * - Zoom and pan
 * - Node details on click
 * - Export to SVG/PNG
 */

class ProofTreeVisualization {
    constructor(containerId, data) {
        this.container = d3.select(`#${containerId}`);
        this.data = data;
        this.width = 1200;
        this.height = 800;
        this.margin = { top: 20, right: 90, bottom: 30, left: 90 };
        this.duration = 750;
        
        this.init();
    }
    
    init() {
        // Clear container
        this.container.selectAll("*").remove();
        
        // Create SVG
        this.svg = this.container.append("svg")
            .attr("width", this.width)
            .attr("height", this.height)
            .call(d3.zoom().on("zoom", (event) => {
                this.g.attr("transform", event.transform);
            }));
        
        this.g = this.svg.append("g")
            .attr("transform", `translate(${this.margin.left},${this.margin.top})`);
        
        // Create tree layout
        this.tree = d3.tree()
            .size([this.height - this.margin.top - this.margin.bottom, 
                   this.width - this.margin.left - this.margin.right]);
        
        // Process data
        this.root = d3.hierarchy(this.data, d => d.children);
        this.root.x0 = (this.height - this.margin.top - this.margin.bottom) / 2;
        this.root.y0 = 0;
        
        // Collapse after second level
        this.root.children.forEach(this.collapse);
        
        this.update(this.root);
    }
    
    collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }
    
    update(source) {
        // Assigns the x and y position for the nodes
        const treeData = this.tree(this.root);
        
        // Compute the new tree layout
        const nodes = treeData.descendants();
        const links = treeData.links();
        
        // Normalize for fixed-depth
        nodes.forEach(d => { d.y = d.depth * 180; });
        
        // ****************** Nodes section ******************
        
        // Update the nodes...
        const node = this.g.selectAll('g.node')
            .data(nodes, d => d.id || (d.id = ++this.i));
        
        // Enter any new modes at the parent's previous position
        const nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr("transform", d => `translate(${source.y0},${source.x0})`)
            .on('click', (event, d) => this.click(d));
        
        // Add Circle for the nodes
        nodeEnter.append('circle')
            .attr('class', 'node')
            .attr('r', 1e-6)
            .style("fill", d => this.getNodeColor(d));
        
        // Add labels for the nodes
        nodeEnter.append('text')
            .attr("dy", ".35em")
            .attr("x", d => d.children || d._children ? -13 : 13)
            .attr("text-anchor", d => d.children || d._children ? "end" : "start")
            .text(d => d.data.name)
            .style("fill-opacity", 1e-6);
        
        // UPDATE
        const nodeUpdate = node.merge(nodeEnter);
        
        // Transition to the proper position for the node
        nodeUpdate.transition()
            .duration(this.duration)
            .attr("transform", d => `translate(${d.y},${d.x})`);
        
        // Update the node attributes and style
        nodeUpdate.select('circle.node')
            .attr('r', 10)
            .style("fill", d => this.getNodeColor(d))
            .attr('cursor', 'pointer');
        
        nodeUpdate.select('text')
            .style("fill-opacity", 1);
        
        // Remove any exiting nodes
        const nodeExit = node.exit().transition()
            .duration(this.duration)
            .attr("transform", d => `translate(${source.y},${source.x})`)
            .remove();
        
        nodeExit.select('circle')
            .attr('r', 1e-6);
        
        nodeExit.select('text')
            .style("fill-opacity", 1e-6);
        
        // ****************** Links section ******************
        
        // Update the links...
        const link = this.g.selectAll('path.link')
            .data(links, d => d.target.id);
        
        // Enter any new links at the parent's previous position
        const linkEnter = link.enter().insert('path', "g")
            .attr("class", "link")
            .attr('d', d => {
                const o = {x: source.x0, y: source.y0};
                return this.diagonal(o, o);
            });
        
        // UPDATE
        const linkUpdate = link.merge(linkEnter);
        
        // Transition back to the parent element position
        linkUpdate.transition()
            .duration(this.duration)
            .attr('d', d => this.diagonal(d.source, d.target));
        
        // Remove any exiting links
        const linkExit = link.exit().transition()
            .duration(this.duration)
            .attr('d', d => {
                const o = {x: source.x, y: source.y};
                return this.diagonal(o, o);
            })
            .remove();
        
        // Store the old positions for transition
        nodes.forEach(d => {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }
    
    diagonal(s, d) {
        return `M ${s.y} ${s.x}
                C ${(s.y + d.y) / 2} ${s.x},
                  ${(s.y + d.y) / 2} ${d.x},
                  ${d.y} ${d.x}`;
    }
    
    click(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        this.update(d);
        
        // Show details
        this.showNodeDetails(d);
    }
    
    getNodeColor(d) {
        const colors = {
            'theorem': '#4CAF50',
            'lemma': '#2196F3',
            'definition': '#FF9800',
            'axiom': '#9C27B0',
            'proof': '#F44336'
        };
        return colors[d.data.type] || '#999';
    }
    
    showNodeDetails(d) {
        const detailsPanel = d3.select('#details-panel');
        detailsPanel.html(`
            <h3>${d.data.name}</h3>
            <p><strong>Type:</strong> ${d.data.type}</p>
            <p><strong>Description:</strong> ${d.data.description || 'N/A'}</p>
            <p><strong>Status:</strong> ${d.data.proven ? '✅ Proven' : '⏳ In Progress'}</p>
            ${d.data.file ? `<p><strong>File:</strong> ${d.data.file}</p>` : ''}
            ${d.data.line ? `<p><strong>Line:</strong> ${d.data.line}</p>` : ''}
        `);
    }
    
    expandAll() {
        this.expand(this.root);
        this.update(this.root);
    }
    
    expand(d) {
        if (d._children) {
            d.children = d._children;
            d._children = null;
        }
        if (d.children) {
            d.children.forEach(child => this.expand(child));
        }
    }
    
    collapseAll() {
        if (this.root.children) {
            this.root.children.forEach(child => this.collapse(child));
        }
        this.update(this.root);
    }
    
    exportSVG() {
        const svgData = this.svg.node().outerHTML;
        const blob = new Blob([svgData], {type: 'image/svg+xml'});
        const url = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.href = url;
        link.download = 'proof-tree.svg';
        link.click();
    }
}

// Example data structure
const exampleData = {
    name: "ExactlyOnceSemantics",
    type: "theorem",
    description: "End-to-end exactly-once semantics guarantee",
    proven: true,
    children: [
        {
            name: "ReplayableSource",
            type: "lemma",
            description: "Source can replay events",
            proven: true,
            children: [
                { name: "SourceOrdering", type: "axiom", proven: true }
            ]
        },
        {
            name: "ConsistentCheckpoint",
            type: "lemma",
            description: "Checkpoint mechanism is consistent",
            proven: true,
            children: [
                { name: "ChandyLamport", type: "theorem", proven: true }
            ]
        },
        {
            name: "AtomicSink",
            type: "lemma",
            description: "Sink commit is atomic",
            proven: true
        }
    ]
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const visualization = new ProofTreeVisualization('proof-tree-container', exampleData);
    
    // Expose for debugging
    window.proofTree = visualization;
});
