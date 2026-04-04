#!/usr/bin/env python3
"""
AnalysisDataFlow Knowledge Graph Auto-Update Script
Automatically updates knowledge graphs when documents change
"""

import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, List
import subprocess
import sys

from extract_entities import MarkdownEntityExtractor, Entity, Relation
from export_formats import GraphExporter


class GraphAutoUpdater:
    """Automatically update knowledge graphs"""
    
    def __init__(self, base_dir: Path, state_file: Path = None):
        self.base_dir = Path(base_dir)
        self.state_file = state_file or Path(base_dir) / ".graph-state.json"
        self.state = self._load_state()
        
        # Graph data directory
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def _load_state(self) -> Dict:
        """Load state from file"""
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        return {
            "last_update": None,
            "file_hashes": {},
            "generated_files": []
        }
    
    def _save_state(self):
        """Save state to file"""
        self.state_file.write_text(
            json.dumps(self.state, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    
    def _get_file_hash(self, file_path: Path) -> str:
        """Get MD5 hash of file contents"""
        content = file_path.read_bytes()
        return hashlib.md5(content).hexdigest()
    
    def _find_changed_files(self, directories: List[str]) -> Set[Path]:
        """Find files that have changed since last update"""
        changed = set()
        
        for dir_name in directories:
            dir_path = self.base_dir.parent / dir_name
            if not dir_path.exists():
                continue
            
            for md_file in dir_path.rglob("*.md"):
                if md_file.name == "00-INDEX.md":
                    continue
                
                rel_path = str(md_file.relative_to(self.base_dir.parent))
                current_hash = self._get_file_hash(md_file)
                stored_hash = self.state["file_hashes"].get(rel_path)
                
                if stored_hash != current_hash:
                    changed.add(md_file)
                    self.state["file_hashes"][rel_path] = current_hash
        
        return changed
    
    def _merge_graph_data(self, base_graph: Dict, new_entities: List[Dict], 
                         new_relations: List[Dict]) -> Dict:
        """Merge new entities into base graph"""
        existing_ids = {n["id"] for n in base_graph.get("nodes", [])}
        
        # Add new nodes
        for entity in new_entities:
            if entity["id"] not in existing_ids:
                base_graph.setdefault("nodes", []).append({
                    "id": entity["id"],
                    "label": entity["label"],
                    "type": entity["type"],
                    "category": entity["category"],
                    "description": entity.get("description", ""),
                    **entity.get("metadata", {})
                })
                existing_ids.add(entity["id"])
        
        # Add new relations
        existing_edges = {(e["source"], e["target"], e["type"]) 
                         for e in base_graph.get("edges", [])}
        
        for relation in new_relations:
            edge_key = (relation["source"], relation["target"], relation["type"])
            if edge_key not in existing_edges:
                base_graph.setdefault("edges", []).append({
                    "source": relation["source"],
                    "target": relation["target"],
                    "type": relation["type"],
                    "label": relation.get("label", ""),
                    "weight": relation.get("weight", 1.0)
                })
                existing_edges.add(edge_key)
        
        return base_graph
    
    def update_graph(self, graph_name: str, directories: List[str]) -> bool:
        """Update a specific knowledge graph"""
        print(f"\nUpdating {graph_name}...")
        
        # Find changed files
        changed_files = self._find_changed_files(directories)
        
        if not changed_files:
            print(f"  No changes detected for {graph_name}")
            return False
        
        print(f"  {len(changed_files)} files changed")
        
        # Load existing graph
        graph_file = self.data_dir / f"{graph_name}-graph.json"
        if graph_file.exists():
            base_graph = json.loads(graph_file.read_text(encoding="utf-8"))
        else:
            base_graph = {
                "name": graph_name.replace("-", " ").title() + " Graph",
                "description": f"Auto-generated {graph_name} knowledge graph",
                "version": "1.0",
                "lastUpdated": datetime.now().isoformat(),
                "nodes": [],
                "edges": [],
                "categories": {},
                "relationTypes": {}
            }
        
        # Extract new entities
        extractor = MarkdownEntityExtractor(self.base_dir.parent)
        all_entities = []
        all_relations = []
        
        for md_file in changed_files:
            entities, relations = extractor.extract_from_file(md_file)
            all_entities.extend(entities)
            all_relations.extend(relations)
        
        print(f"  Extracted {len(all_entities)} entities, {len(all_relations)} relations")
        
        # Merge into base graph
        updated_graph = self._merge_graph_data(base_graph, all_entities, all_relations)
        updated_graph["lastUpdated"] = datetime.now().isoformat()
        
        # Save updated graph
        graph_file.write_text(
            json.dumps(updated_graph, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        
        # Update state
        self.state["last_update"] = datetime.now().isoformat()
        self.state["generated_files"].append(str(graph_file))
        
        print(f"  Updated: {graph_file}")
        return True
    
    def export_all_formats(self, graph_name: str, output_dir: Path = None):
        """Export graph to all formats"""
        graph_file = self.data_dir / f"{graph_name}-graph.json"
        if not graph_file.exists():
            print(f"Graph not found: {graph_file}")
            return
        
        graph_data = json.loads(graph_file.read_text(encoding="utf-8"))
        exporter = GraphExporter(graph_data)
        
        output_dir = output_dir or self.base_dir / "exports"
        exports = exporter.export_all(output_dir)
        
        print(f"  Exported to:")
        for fmt, path in exports.items():
            print(f"    {fmt}: {path}")
    
    def run_full_update(self):
        """Run full update cycle"""
        print("=" * 60)
        print("AnalysisDataFlow Knowledge Graph Auto-Update")
        print("=" * 60)
        
        graphs_to_update = [
            ("streaming-theory", ["Struct"]),
            ("flink-technology", ["Flink"]),
            ("design-patterns", ["Knowledge"]),
        ]
        
        any_updated = False
        for graph_name, directories in graphs_to_update:
            if self.update_graph(graph_name, directories):
                any_updated = True
                # Export to all formats
                self.export_all_formats(graph_name)
        
        if any_updated:
            self._save_state()
            print("\n" + "=" * 60)
            print("Update completed successfully")
        else:
            print("\n" + "=" * 60)
            print("No updates needed")
        
        return 0 if any_updated else 1


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description="Auto-update knowledge graphs")
    parser.add_argument("--base-dir", default="..", help="Base directory")
    parser.add_argument("--watch", action="store_true", help="Watch for changes")
    parser.add_argument("--interval", type=int, default=60, help="Watch interval (seconds)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    
    args = parser.parse_args()
    
    updater = GraphAutoUpdater(Path(args.base_dir))
    
    if args.once:
        return updater.run_full_update()
    
    if args.watch:
        import time
        print(f"Watching for changes every {args.interval} seconds...")
        print("Press Ctrl+C to stop")
        try:
            while True:
                updater.run_full_update()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped")
    else:
        return updater.run_full_update()


if __name__ == "__main__":
    exit(main())
