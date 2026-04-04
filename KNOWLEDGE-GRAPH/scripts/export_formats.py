#!/usr/bin/env python3
"""
AnalysisDataFlow Knowledge Graph Export Utilities
Supports: JSON, GraphML, Cypher (Neo4j), GEXF
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


class GraphExporter:
    """Export knowledge graphs to various formats"""
    
    def __init__(self, graph_data: Dict[str, Any]):
        self.graph = graph_data
        self.nodes = graph_data.get("nodes", [])
        self.edges = graph_data.get("edges", [])
    
    def to_json(self, pretty: bool = True) -> str:
        """Export to JSON format"""
        if pretty:
            return json.dumps(self.graph, indent=2, ensure_ascii=False)
        return json.dumps(self.graph, ensure_ascii=False)
    
    def to_graphml(self) -> str:
        """Export to GraphML format"""
        # Create root element
        root = ET.Element("graphml")
        root.set("xmlns", "http://graphml.graphdrawing.org/xmlns")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", 
                 "http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd")
        
        # Add keys for node attributes
        keys = {
            "label": {"id": "d0", "for": "node", "attr.name": "label", "attr.type": "string"},
            "type": {"id": "d1", "for": "node", "attr.name": "type", "attr.type": "string"},
            "category": {"id": "d2", "for": "node", "attr.name": "category", "attr.type": "string"},
            "description": {"id": "d3", "for": "node", "attr.name": "description", "attr.type": "string"},
            "level": {"id": "d4", "for": "node", "attr.name": "level", "attr.type": "int"},
            "relation": {"id": "d5", "for": "edge", "attr.name": "relation", "attr.type": "string"},
            "weight": {"id": "d6", "for": "edge", "attr.name": "weight", "attr.type": "double"},
        }
        
        for key_id, key_attrs in keys.items():
            key_elem = ET.SubElement(root, "key")
            for attr_name, attr_value in key_attrs.items():
                key_elem.set(attr_name, str(attr_value))
        
        # Create graph element
        graph_elem = ET.SubElement(root, "graph")
        graph_elem.set("id", self.graph.get("name", "G").replace(" ", "_"))
        graph_elem.set("edgedefault", "directed")
        
        # Add nodes
        for node in self.nodes:
            node_elem = ET.SubElement(graph_elem, "node")
            node_elem.set("id", str(node.get("id", "")))
            
            # Add node data
            for key_id, attr_name in [("d0", "label"), ("d1", "type"), 
                                       ("d2", "category"), ("d3", "description"),
                                       ("d4", "level")]:
                if attr_name in node and node[attr_name] is not None:
                    data_elem = ET.SubElement(node_elem, "data")
                    data_elem.set("key", key_id)
                    data_elem.text = str(node[attr_name])
        
        # Add edges
        for i, edge in enumerate(self.edges):
            edge_elem = ET.SubElement(graph_elem, "edge")
            edge_elem.set("id", f"e{i}")
            edge_elem.set("source", str(edge.get("source", "")))
            edge_elem.set("target", str(edge.get("target", "")))
            
            # Add edge data
            if "type" in edge:
                data_elem = ET.SubElement(edge_elem, "data")
                data_elem.set("key", "d5")
                data_elem.text = str(edge["type"])
            
            if "weight" in edge:
                data_elem = ET.SubElement(edge_elem, "data")
                data_elem.set("key", "d6")
                data_elem.text = str(edge["weight"])
        
        # Pretty print
        xml_str = ET.tostring(root, encoding="unicode")
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")
    
    def to_cypher(self) -> str:
        """Export to Neo4j Cypher format"""
        lines = [
            "// AnalysisDataFlow Knowledge Graph",
            f"// Graph: {self.graph.get('name', 'Unknown')}",
            f"// Generated: {datetime.now().isoformat()}",
            "",
            "// Create constraints",
            "CREATE CONSTRAINT concept_id IF NOT EXISTS FOR (c:Concept) REQUIRE c.id IS UNIQUE;",
            "",
            "// Create nodes",
        ]
        
        # Create nodes
        for node in self.nodes:
            node_id = node.get("id", "").replace('"', '\\"')
            label = node.get("label", "").replace('"', '\\"')
            node_type = (node.get("type") or node.get("category", "Unknown")).replace('"', '\\"')
            description = node.get("description", "").replace('"', '\\"')
            
            props = [
                f'id: "{node_id}"',
                f'label: "{label}"',
                f'type: "{node_type}"',
            ]
            
            if description:
                props.append(f'description: "{description}"')
            
            if "level" in node:
                props.append(f'level: {node["level"]}')
            
            if "layer" in node:
                props.append(f'layer: {node["layer"]}')
            
            if "stage" in node:
                props.append(f'stage: {node["stage"]}')
            
            if "score" in node:
                props.append(f'score: {node["score"]}')
            
            props_str = ", ".join(props)
            lines.append(f'CREATE (:Concept {{ {props_str} }});')
        
        lines.append("")
        lines.append("// Create relationships")
        
        # Create relationships
        rel_types = set()
        for edge in self.edges:
            rel_type = edge.get("type", "RELATED_TO").upper().replace("-", "_")
            rel_types.add(rel_type)
            source = str(edge.get("source", "")).replace('"', '\\"')
            target = str(edge.get("target", "")).replace('"', '\\"')
            edge_label = edge.get("label", "").replace('"', '\\"')
            
            rel_props = ""
            if edge_label:
                rel_props = f' {{ label: "{edge_label}" }}'
            
            lines.append(
                f'MATCH (a:Concept {{ id: "{source}" }}), '
                f'(b:Concept {{ id: "{target}" }}) '
                f'CREATE (a)-[:{rel_type}{rel_props}]->(b);'
            )
        
        lines.append("")
        lines.append("// Create indexes for relationship types")
        for rel_type in rel_types:
            lines.append(f"CREATE INDEX {rel_type.lower()}_idx IF NOT EXISTS FOR ()-[r:{rel_type}]-() ON r.label;")
        
        return "\n".join(lines)
    
    def to_gexf(self) -> str:
        """Export to GEXF format (for Gephi)"""
        root = ET.Element("gexf")
        root.set("xmlns", "http://www.gexf.net/1.3")
        root.set("version", "1.3")
        
        # Add meta
        meta = ET.SubElement(root, "meta")
        meta.set("lastmodifieddate", datetime.now().strftime("%Y-%m-%d"))
        creator = ET.SubElement(meta, "creator")
        creator.text = "AnalysisDataFlow Knowledge Graph"
        description = ET.SubElement(meta, "description")
        description.text = self.graph.get("description", "")
        
        # Add graph
        graph_elem = ET.SubElement(root, "graph")
        graph_elem.set("mode", "static")
        graph_elem.set("defaultedgetype", "directed")
        
        # Add attributes
        attrs_elem = ET.SubElement(graph_elem, "attributes")
        attrs_elem.set("class", "node")
        
        attr_defs = [
            {"id": "0", "title": "type", "type": "string"},
            {"id": "1", "title": "category", "type": "string"},
            {"id": "2", "title": "description", "type": "string"},
            {"id": "3", "title": "level", "type": "integer"},
        ]
        
        for attr_def in attr_defs:
            attr_elem = ET.SubElement(attrs_elem, "attribute")
            for k, v in attr_def.items():
                attr_elem.set(k, v)
        
        # Add nodes
        nodes_elem = ET.SubElement(graph_elem, "nodes")
        for node in self.nodes:
            node_elem = ET.SubElement(nodes_elem, "node")
            node_elem.set("id", str(node.get("id", "")))
            node_elem.set("label", str(node.get("label", "")))
            
            # Add viz:color
            color = node.get("color", "#7F8C8D")
            if color.startswith("#"):
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                viz_color = ET.SubElement(node_elem, "{http://www.gexf.net/1.3/viz}color")
                viz_color.set("r", str(r))
                viz_color.set("g", str(g))
                viz_color.set("b", str(b))
            
            # Add attributes
            attvalues = ET.SubElement(node_elem, "attvalues")
            for attr_id, attr_name in [("0", "type"), ("1", "category"), 
                                        ("2", "description"), ("3", "level")]:
                if attr_name in node and node[attr_name] is not None:
                    attvalue = ET.SubElement(attvalues, "attvalue")
                    attvalue.set("for", attr_id)
                    attvalue.set("value", str(node[attr_name]))
        
        # Add edges
        edges_elem = ET.SubElement(graph_elem, "edges")
        for i, edge in enumerate(self.edges):
            edge_elem = ET.SubElement(edges_elem, "edge")
            edge_elem.set("id", f"e{i}")
            edge_elem.set("source", str(edge.get("source", "")))
            edge_elem.set("target", str(edge.get("target", "")))
            edge_elem.set("label", str(edge.get("type", "")))
            
            if "weight" in edge:
                edge_elem.set("weight", str(edge["weight"]))
        
        # Pretty print
        xml_str = ET.tostring(root, encoding="unicode")
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent="  ")
    
    def to_dot(self) -> str:
        """Export to Graphviz DOT format"""
        lines = [
            f"// {self.graph.get('name', 'Knowledge Graph')}",
            f"// {self.graph.get('description', '')}",
            "digraph G {",
            '  rankdir="TB";',
            '  node [style=filled, fillcolor="#f0f0f0", fontname="Arial"];',
            '  edge [fontname="Arial", fontsize=10];',
            "",
        ]
        
        # Add nodes
        for node in self.nodes:
            node_id = str(node.get("id", "")).replace("-", "_").replace(".", "_")
            label = node.get("label", "").replace('"', '\\"')
            color = node.get("color", "#7F8C8D")
            
            lines.append(f'  {node_id} [label="{label}", fillcolor="{color}"];')
        
        lines.append("")
        
        # Add edges
        for edge in self.edges:
            source = str(edge.get("source", "")).replace("-", "_").replace(".", "_")
            target = str(edge.get("target", "")).replace("-", "_").replace(".", "_")
            label = edge.get("label", edge.get("type", "")).replace('"', '\\"')
            
            edge_attrs = f'[label="{label}"]'
            lines.append(f'  {source} -> {target} {edge_attrs};')
        
        lines.append("}")
        return "\n".join(lines)
    
    def export_all(self, output_dir: Path) -> Dict[str, Path]:
        """Export to all formats"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        base_name = self.graph.get("name", "graph").replace(" ", "_").lower()
        
        exports = {}
        
        # JSON
        json_path = output_dir / f"{base_name}.json"
        json_path.write_text(self.to_json(), encoding="utf-8")
        exports["json"] = json_path
        
        # GraphML
        graphml_path = output_dir / f"{base_name}.graphml"
        graphml_path.write_text(self.to_graphml(), encoding="utf-8")
        exports["graphml"] = graphml_path
        
        # Cypher
        cypher_path = output_dir / f"{base_name}.cypher"
        cypher_path.write_text(self.to_cypher(), encoding="utf-8")
        exports["cypher"] = cypher_path
        
        # GEXF
        gexf_path = output_dir / f"{base_name}.gexf"
        gexf_path.write_text(self.to_gexf(), encoding="utf-8")
        exports["gexf"] = gexf_path
        
        # DOT
        dot_path = output_dir / f"{base_name}.dot"
        dot_path.write_text(self.to_dot(), encoding="utf-8")
        exports["dot"] = dot_path
        
        return exports


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Export knowledge graphs to various formats")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("-o", "--output", help="Output directory", default="./exports")
    parser.add_argument("-f", "--format", choices=["json", "graphml", "cypher", "gexf", "dot", "all"],
                       default="all", help="Export format")
    parser.add_argument("--stdout", action="store_true", help="Output to stdout")
    
    args = parser.parse_args()
    
    # Load graph
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    graph_data = json.loads(input_path.read_text(encoding="utf-8"))
    exporter = GraphExporter(graph_data)
    
    if args.stdout:
        if args.format == "json":
            print(exporter.to_json())
        elif args.format == "graphml":
            print(exporter.to_graphml())
        elif args.format == "cypher":
            print(exporter.to_cypher())
        elif args.format == "gexf":
            print(exporter.to_gexf())
        elif args.format == "dot":
            print(exporter.to_dot())
    else:
        output_dir = Path(args.output)
        
        if args.format == "all":
            exports = exporter.export_all(output_dir)
            print(f"Exported to:")
            for fmt, path in exports.items():
                print(f"  {fmt}: {path}")
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
            base_name = graph_data.get("name", "graph").replace(" ", "_").lower()
            
            format_methods = {
                "json": ("json", exporter.to_json),
                "graphml": ("graphml", exporter.to_graphml),
                "cypher": ("cypher", exporter.to_cypher),
                "gexf": ("gexf", exporter.to_gexf),
                "dot": ("dot", exporter.to_dot),
            }
            
            ext, method = format_methods[args.format]
            output_path = output_dir / f"{base_name}.{ext}"
            output_path.write_text(method(), encoding="utf-8")
            print(f"Exported to: {output_path}")
    
    return 0


if __name__ == "__main__":
    exit(main())
