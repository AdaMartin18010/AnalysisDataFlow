/**
 * AnalysisDataFlow Website - Main JavaScript
 * Features: Theme toggle, Sidebar, Search, D3.js Graph
 */

// ============================================
// Theme Management
// ============================================
const ThemeManager = {
    init() {
        const themeToggle = document.getElementById('themeToggle');
        if (!themeToggle) return;
        
        // Load saved theme or default to dark
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
        this.updateIcon(savedTheme);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            this.updateIcon(newTheme);
        });
    },
    
    updateIcon(theme) {
        const themeToggle = document.getElementById('themeToggle');
        if (!themeToggle) return;
        
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }
};

// ============================================
// Sidebar Management
// ============================================
const SidebarManager = {
    init() {
        const menuToggle = document.getElementById('menuToggle');
        const sidebarClose = document.getElementById('sidebarClose');
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('overlay');
        
        if (!menuToggle || !sidebar) return;
        
        menuToggle.addEventListener('click', () => {
            sidebar.classList.add('open');
            overlay.classList.add('show');
            document.body.style.overflow = 'hidden';
        });
        
        const closeSidebar = () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('show');
            document.body.style.overflow = '';
        };
        
        if (sidebarClose) {
            sidebarClose.addEventListener('click', closeSidebar);
        }
        
        if (overlay) {
            overlay.addEventListener('click', closeSidebar);
        }
        
        // Close sidebar when clicking on nav links (mobile)
        const navLinks = sidebar.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    closeSidebar();
                }
            });
        });
    }
};

// ============================================
// Search Functionality
// ============================================
const SearchManager = {
    data: [],
    fuse: null,
    
    async init() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) return;
        
        // Load search data
        try {
            const response = await fetch('data/search-index.json');
            this.data = await response.json();
            
            // Initialize Fuse.js
            this.fuse = new Fuse(this.data, {
                keys: ['id', 'name', 'description'],
                threshold: 0.3,
                includeScore: true,
                includeMatches: true
            });
            
            this.setupEventListeners();
        } catch (error) {
            console.error('Failed to load search data:', error);
        }
    },
    
    setupEventListeners() {
        const searchInput = document.getElementById('searchInput');
        const resultsContainer = document.getElementById('searchResults');
        
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                this.performSearch(e.target.value);
            }, 200);
        });
        
        // Filter buttons
        const filterBtns = document.querySelectorAll('.filter-btn');
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.performSearch(searchInput.value, btn.dataset.filter);
            });
        });
    },
    
    performSearch(query, filter = 'all') {
        const resultsContainer = document.getElementById('searchResults');
        
        if (!query.trim()) {
            resultsContainer.innerHTML = '';
            return;
        }
        
        let results = this.fuse.search(query);
        
        // Apply filter
        if (filter !== 'all') {
            results = results.filter(r => r.item.type === filter);
        }
        
        this.renderResults(results);
    },
    
    renderResults(results) {
        const resultsContainer = document.getElementById('searchResults');
        
        if (results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="no-results">
                    <i class="fas fa-search"></i>
                    <p>未找到匹配的结果</p>
                </div>
            `;
            return;
        }
        
        resultsContainer.innerHTML = results.map(result => {
            const item = result.item;
            const typeClass = item.type.toLowerCase();
            
            return `
                <div class="result-item" onclick="window.open('${item.path}', '_blank')">
                    <div class="result-header">
                        <span class="result-type ${typeClass}">${item.type}</span>
                        <span class="result-id">${item.id}</span>
                    </div>
                    <div class="result-title">${item.name}</div>
                    <div class="result-location">
                        <i class="fas fa-folder"></i> ${item.location}
                    </div>
                </div>
            `;
        }).join('');
    }
};

// ============================================
// D3.js Graph Visualization
// ============================================
const GraphVisualization = {
    svg: null,
    simulation: null,
    g: null,
    zoom: null,
    
    async init() {
        const container = document.getElementById('graphCanvas');
        if (!container || typeof d3 === 'undefined') return;
        
        try {
            const response = await fetch('data/graph-data.json');
            const data = await response.json();
            this.renderGraph(container, data);
        } catch (error) {
            console.error('Failed to load graph data:', error);
            container.innerHTML = '<div class="no-results"><p>加载图谱数据失败</p></div>';
        }
    },
    
    renderGraph(container, data) {
        const width = container.clientWidth;
        const height = container.clientHeight;
        
        // Create SVG
        this.svg = d3.select('#graphCanvas')
            .append('svg')
            .attr('width', width)
            .attr('height', height)
            .attr('viewBox', [0, 0, width, height]);
        
        // Add zoom behavior
        this.zoom = d3.zoom()
            .scaleExtent([0.1, 4])
            .on('zoom', (event) => {
                this.g.attr('transform', event.transform);
            });
        
        this.svg.call(this.zoom);
        
        // Create main group
        this.g = this.svg.append('g');
        
        // Define arrow marker
        this.svg.append('defs').selectAll('marker')
            .data(['end'])
            .enter().append('marker')
            .attr('id', 'arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 25)
            .attr('refY', 0)
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#58a6ff');
        
        // Color scale
        const colorScale = d3.scaleOrdinal()
            .domain(['struct', 'knowledge', 'flink'])
            .range(['#4A90D9', '#5CB85C', '#F0AD4E']);
        
        // Create force simulation
        this.simulation = d3.forceSimulation(data.nodes)
            .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(40));
        
        // Create links
        const link = this.g.append('g')
            .attr('class', 'links')
            .selectAll('line')
            .data(data.links)
            .enter().append('line')
            .attr('stroke', '#58a6ff')
            .attr('stroke-width', 1.5)
            .attr('marker-end', 'url(#arrow)');
        
        // Create nodes
        const node = this.g.append('g')
            .attr('class', 'nodes')
            .selectAll('g')
            .data(data.nodes)
            .enter().append('g')
            .attr('class', 'node')
            .call(d3.drag()
                .on('start', (event, d) => this.dragstarted(event, d))
                .on('drag', (event, d) => this.dragged(event, d))
                .on('end', (event, d) => this.dragended(event, d)));
        
        // Add circles to nodes
        node.append('circle')
            .attr('r', d => d.size || 20)
            .attr('fill', d => colorScale(d.group))
            .attr('stroke', '#fff')
            .attr('stroke-width', 2)
            .style('cursor', 'pointer');
        
        // Add labels
        node.append('text')
            .text(d => d.label || d.id)
            .attr('x', 25)
            .attr('y', 5)
            .attr('font-size', '12px')
            .attr('fill', 'var(--text-primary)')
            .style('pointer-events', 'none');
        
        // Add tooltips
        node.append('title')
            .text(d => `${d.id}: ${d.name}`);
        
        // Update positions on tick
        this.simulation.on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);
            
            node.attr('transform', d => `translate(${d.x},${d.y})`);
        });
        
        // Node click event
        node.on('click', (event, d) => {
            if (d.path) {
                window.open(d.path, '_blank');
            }
        });
        
        // Setup toolbar buttons
        this.setupToolbar();
    },
    
    dragstarted(event, d) {
        if (!event.active) this.simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    },
    
    dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    },
    
    dragended(event, d) {
        if (!event.active) this.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    },
    
    setupToolbar() {
        const zoomIn = document.getElementById('zoomIn');
        const zoomOut = document.getElementById('zoomOut');
        const resetView = document.getElementById('resetView');
        
        if (zoomIn) {
            zoomIn.addEventListener('click', () => {
                this.svg.transition().call(this.zoom.scaleBy, 1.3);
            });
        }
        
        if (zoomOut) {
            zoomOut.addEventListener('click', () => {
                this.svg.transition().call(this.zoom.scaleBy, 1 / 1.3);
            });
        }
        
        if (resetView) {
            resetView.addEventListener('click', () => {
                this.svg.transition().call(this.zoom.transform, d3.zoomIdentity);
            });
        }
    }
};

// ============================================
// Utility Functions
// ============================================
const Utils = {
    // Format number with commas
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Copy to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            console.error('Failed to copy:', err);
            return false;
        }
    }
};

// ============================================
// Initialize on DOM Ready
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    SidebarManager.init();
    SearchManager.init();
    GraphVisualization.init();
});

// Export for external use
window.AnalysisDataFlow = {
    ThemeManager,
    SidebarManager,
    SearchManager,
    GraphVisualization,
    Utils
};
