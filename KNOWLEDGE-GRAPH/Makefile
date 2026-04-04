# AnalysisDataFlow Knowledge Graph Makefile
# Quick commands for common operations

.PHONY: help serve export extract update clean all

# Default target
help:
	@echo "AnalysisDataFlow Knowledge Graph Commands"
	@echo "========================================="
	@echo ""
	@echo "  make serve       - Start development server"
	@echo "  make export      - Export all graphs to all formats"
	@echo "  make extract     - Extract entities from documents"
	@echo "  make update      - Run auto-update"
	@echo "  make watch       - Watch for changes and auto-update"
	@echo "  make validate    - Validate graph data files"
	@echo "  make stats       - Show graph statistics"
	@echo "  make clean       - Clean generated files"
	@echo "  make all         - Run export, extract, and update"

# Start development server
serve:
	@echo "Starting server at http://localhost:8080"
	@cd visualizations && python -m http.server 8080

# Export all graphs
export:
	@echo "Exporting graphs..."
	@mkdir -p exports
	@python scripts/export_formats.py data/streaming-theory-graph.json -o exports
	@python scripts/export_formats.py data/flink-technology-graph.json -o exports
	@python scripts/export_formats.py data/design-patterns-graph.json -o exports
	@python scripts/export_formats.py data/concept-dependency-graph.json -o exports
	@python scripts/export_formats.py data/tech-decision-graph.json -o exports
	@python scripts/export_formats.py data/learning-path-graph.json -o exports
	@echo "Export complete!"

# Extract entities
extract:
	@echo "Extracting entities..."
	@python scripts/extract_entities.py --base-dir .. --output extracted-entities.json Struct Knowledge Flink
	@echo "Extraction complete!"

# Build dependency graph
build-deps:
	@echo "Building dependency graph..."
	@python scripts/extract_entities.py --build-deps --output data/auto-dependency-graph.json ..
	@echo "Dependency graph built!"

# Run auto-update once
update:
	@echo "Running auto-update..."
	@python scripts/auto_update.py --once

# Watch for changes
watch:
	@echo "Watching for changes (Ctrl+C to stop)..."
	@python scripts/auto_update.py --watch --interval 60

# Validate graph files
validate:
	@echo "Validating graph files..."
	@python -c "
import json
import sys
from pathlib import Path

graphs = [
    'data/streaming-theory-graph.json',
    'data/flink-technology-graph.json',
    'data/design-patterns-graph.json',
    'data/concept-dependency-graph.json',
    'data/tech-decision-graph.json',
    'data/learning-path-graph.json'
]

errors = 0
for graph_file in graphs:
    try:
        with open(graph_file) as f:
            data = json.load(f)
        required = ['name', 'nodes', 'edges']
        for field in required:
            if field not in data:
                print(f'❌ {graph_file}: Missing {field}')
                errors += 1
                continue
        print(f'✅ {graph_file}: {len(data[\"nodes\"])} nodes, {len(data[\"edges\"])} edges')
    except Exception as e:
        print(f'❌ {graph_file}: {e}')
        errors += 1

sys.exit(1 if errors > 0 else 0)
"

# Show statistics
stats:
	@echo "Graph Statistics"
	@echo "==============="
	@python -c "
import json
from pathlib import Path

graphs = list(Path('data').glob('*-graph.json'))
total_nodes = 0
total_edges = 0

for graph_file in graphs:
    with open(graph_file) as f:
        data = json.load(f)
    nodes = len(data.get('nodes', []))
    edges = len(data.get('edges', []))
    total_nodes += nodes
    total_edges += edges
    print(f'{graph_file.stem:30} | Nodes: {nodes:3} | Edges: {edges:3}')

print('-' * 50)
print(f'{'TOTAL':30} | Nodes: {total_nodes:3} | Edges: {total_edges:3}')
"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -rf exports
	@rm -f extracted-entities.json
	@rm -f .graph-state.json
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

# Run everything
all: export extract update
	@echo "All tasks completed!"

# Create new graph template
template:
	@read -p "Enter graph name: " name; \
	cat > data/$$name-graph.json << 'EOF'
{
  "name": "New Knowledge Graph",
  "description": "Description of the knowledge graph",
  "version": "1.0",
  "lastUpdated": "2026-04-04",
  "nodes": [],
  "edges": [],
  "categories": {},
  "relationTypes": {}
}
EOF
	@echo "Created data/$$name-graph.json"
