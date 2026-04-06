#!/usr/bin/env python3
"""
Script to add 'Dependencies' column to THEOREM-REGISTRY.md tables
"""

import re

# Read the file
with open('THEOREM-REGISTRY.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Define dependency mappings for key theorems/definitions/lemmas
dependencies = {
    # Theorems - Checkpoint Correctness Chain
    'Thm-S-17-01': 'Def-S-01-04, Def-S-02-03, Lemma-S-02-03-01, Thm-S-03-02',
    'Thm-S-03-02': 'Def-S-03-01, Def-S-03-05, Lemma-S-03-02',
    
    # Theorems - Exactly-Once Chain
    'Thm-S-18-01': 'Def-S-08-04, Lemma-S-18-01, Lemma-S-18-02, Thm-S-12-01',
    'Thm-S-12-01': 'Def-S-01-03, Def-S-05-02, Def-S-12-01, Def-S-12-03, Lemma-S-12-01',
    
    # Theorems - Watermark Algebra Chain
    'Thm-S-20-01': 'Def-S-20-01, Lemma-S-20-01, Lemma-S-20-02, Lemma-S-20-03, Lemma-S-20-04',
    'Thm-S-09-01': 'Def-S-04-04, Def-S-09-02, Lemma-S-04-02',
    
    # Theorems - State Backend Chain
    'Thm-F-02-01': 'Def-F-02-90, Def-F-02-91, Lemma-F-02-23',
    'Thm-F-02-45': 'Def-F-02-61, Def-F-02-62, Lemma-F-02-23',
    
    # Theorems - Async Execution Chain
    'Thm-F-02-50': 'Def-F-02-70, Def-F-02-73, Def-F-02-77, Lemma-F-02-02',
    'Thm-F-02-52': 'Def-F-02-74, Def-F-02-75, Lemma-F-02-02',
    
    # Other Key Theorems
    'Thm-S-13-01': 'Def-S-13-01, Def-S-13-02, Def-S-13-03, Lemma-S-13-01, Lemma-S-13-02',
    'Thm-S-07-01': 'Def-S-07-01, Def-S-07-02, Lemma-S-07-02',
    'Thm-S-08-02': 'Def-S-08-01, Def-S-08-02, Def-S-08-03, Def-S-08-04, Lemma-S-08-01',
    'Thm-S-04-01': 'Def-S-04-01, Def-S-04-02, Lemma-S-04-01',
    'Thm-S-15-01': 'Def-S-15-01, Def-S-15-02, Def-S-15-03, Def-S-15-04',
    'Thm-S-16-01': 'Def-S-16-01, Def-S-16-02, Def-S-16-03, Def-S-16-04',
    'Thm-S-19-01': 'Def-S-19-01, Def-S-19-02, Def-S-19-03, Def-S-19-04, Def-S-19-05',
    'Thm-S-21-01': 'Def-S-21-01, Def-S-21-02, Def-S-21-03, Def-S-21-04',
    'Thm-S-22-01': 'Def-S-22-01, Def-S-22-02, Def-S-22-03, Def-S-22-04',
    'Thm-S-23-01': 'Def-S-23-01, Def-S-23-02, Def-S-23-03, Def-S-23-04',
    
    # Definitions - typically foundational
    'Def-S-01-04': '-',
    'Def-S-02-03': 'Def-S-01-04',
    'Def-S-03-01': '-',
    'Def-S-03-05': 'Def-S-03-01',
    'Def-S-04-01': '-',
    'Def-S-04-02': 'Def-S-04-01',
    'Def-S-04-04': 'Def-S-04-01',
    'Def-S-07-01': '-',
    'Def-S-07-02': 'Def-S-07-01',
    'Def-S-08-01': '-',
    'Def-S-08-02': '-',
    'Def-S-08-03': '-',
    'Def-S-08-04': '-',
    'Def-S-09-02': 'Def-S-04-04',
    'Def-S-12-01': 'Def-S-01-03',
    'Def-S-12-03': 'Def-S-12-01, Def-S-12-02',
    'Def-S-13-01': 'Def-S-02-03',
    'Def-S-13-02': 'Def-S-02-03',
    'Def-S-13-03': '-',
    'Def-S-15-01': '-',
    'Def-S-15-02': '-',
    'Def-S-15-03': '-',
    'Def-S-15-04': '-',
    'Def-S-16-01': '-',
    'Def-S-16-02': '-',
    'Def-S-16-03': 'Def-S-16-01, Def-S-16-02',
    'Def-S-16-04': 'Def-S-16-01',
    'Def-S-17-01': '-',
    'Def-S-17-02': '-',
    'Def-S-17-03': 'Def-S-17-01',
    'Def-S-17-04': '-',
    'Def-S-18-01': '-',
    'Def-S-18-02': '-',
    'Def-S-18-03': '-',
    'Def-S-18-04': '-',
    'Def-S-18-05': '-',
    'Def-S-19-01': '-',
    'Def-S-19-02': 'Def-S-19-01',
    'Def-S-19-03': 'Def-S-19-01',
    'Def-S-19-04': '-',
    'Def-S-19-05': 'Def-S-19-01, Def-S-19-04',
    'Def-S-20-01': 'Def-S-04-04, Def-S-09-02',
    'Def-S-20-02': 'Def-S-20-01',
    'Def-S-20-03': 'Def-S-20-01',
    'Def-S-20-04': 'Def-S-20-01',
    'Def-S-20-05': 'Def-S-20-01',
    'Def-S-21-01': '-',
    'Def-S-21-02': 'Def-S-21-01',
    'Def-S-21-03': 'Def-S-21-02',
    'Def-S-21-04': 'Def-S-21-02',
    'Def-S-22-01': '-',
    'Def-S-22-02': 'Def-S-22-01',
    'Def-S-22-03': 'Def-S-22-01',
    'Def-S-22-04': 'Def-S-22-01',
    'Def-S-23-01': '-',
    'Def-S-23-02': 'Def-S-23-01',
    'Def-S-23-03': 'Def-S-23-02',
    'Def-S-23-04': 'Def-S-23-01',
    'Def-S-23-05': 'Def-S-23-01',
    'Def-S-23-06': 'Def-S-23-05',
    'Def-F-02-90': '-',
    'Def-F-02-91': 'Def-F-02-90',
    'Def-F-02-61': 'Def-F-02-90',
    'Def-F-02-62': 'Def-F-02-61',
    'Def-F-02-70': '-',
    'Def-F-02-73': 'Def-F-02-70',
    'Def-F-02-77': 'Def-F-02-70',
    'Def-F-02-74': 'Def-F-02-70',
    'Def-F-02-75': 'Def-F-02-70',
    
    # Lemmas
    'Lemma-S-02-03-01': 'Def-S-02-03',
    'Lemma-S-04-01': 'Def-S-04-01, Def-S-04-02',
    'Lemma-S-04-02': 'Def-S-04-04',
    'Lemma-S-07-02': 'Def-S-07-01, Def-S-07-02',
    'Lemma-S-08-01': 'Def-S-08-04',
    'Lemma-S-12-01': 'Def-S-12-01',
    'Lemma-S-12-02': 'Def-S-12-01',
    'Lemma-S-12-03': 'Def-S-12-01',
    'Lemma-S-13-01': 'Def-S-13-01',
    'Lemma-S-13-02': 'Def-S-13-03',
    'Lemma-S-17-01': 'Def-S-17-01, Def-S-17-03',
    'Lemma-S-17-02': 'Def-S-17-02, Def-S-17-04',
    'Lemma-S-17-03': 'Def-S-17-03',
    'Lemma-S-17-04': 'Def-S-17-01, Def-S-17-02',
    'Lemma-S-18-01': 'Def-S-08-04, Def-S-18-04',
    'Lemma-S-18-02': 'Def-S-18-03, Def-S-18-05',
    'Lemma-S-18-03': 'Def-S-17-02, Def-S-18-01',
    'Lemma-S-18-04': 'Def-S-07-01, Def-S-07-02',
    'Lemma-S-20-01': 'Def-S-20-01, Def-S-20-02',
    'Lemma-S-20-02': 'Def-S-20-01, Def-S-20-02',
    'Lemma-S-20-03': 'Def-S-20-01, Def-S-20-02',
    'Lemma-S-20-04': 'Def-S-20-01, Def-S-20-05, Lemma-S-20-01, Lemma-S-20-02, Lemma-S-20-03',
    'Lemma-S-23-01': 'Def-S-23-02, Def-S-23-03',
    'Lemma-S-23-02': 'Def-S-23-03',
    'Lemma-S-23-03': 'Def-S-23-02',
    'Lemma-F-02-23': 'Def-F-02-61',
    'Lemma-F-02-02': 'Def-F-02-70, Def-F-02-73, Def-F-02-77',
    
    # Propositions
    'Prop-S-17-01': 'Def-S-17-03, Thm-S-17-01',
    'Prop-S-18-01': 'Def-S-18-03, Thm-S-18-01',
    'Prop-S-18-02': 'Thm-S-18-01',
    'Prop-S-20-01': 'Def-S-20-05, Thm-S-20-01',
    
    # Corollaries
    'Cor-S-07-01': 'Thm-S-07-01, Thm-S-17-01',
}

# Count statistics
theorem_count = sum(1 for k in dependencies if k.startswith('Thm-'))
def_count = sum(1 for k in dependencies if k.startswith('Def-'))
lemma_count = sum(1 for k in dependencies if k.startswith('Lemma-'))
prop_count = sum(1 for k in dependencies if k.startswith('Prop-'))
cor_count = sum(1 for k in dependencies if k.startswith('Cor-'))

print(f"Dependency mappings defined:")
print(f"  Theorems: {theorem_count}")
print(f"  Definitions: {def_count}")
print(f"  Lemmas: {lemma_count}")
print(f"  Propositions: {prop_count}")
print(f"  Corollaries: {cor_count}")
print(f"  Total: {len(dependencies)}")

# Save dependencies to a file for reference
with open('scripts/dependency_mappings.txt', 'w', encoding='utf-8') as f:
    f.write("# Dependency Mappings\n\n")
    for key in sorted(dependencies.keys()):
        f.write(f"{key}: {dependencies[key]}\n")

print("\nDependency mappings saved to scripts/dependency_mappings.txt")
