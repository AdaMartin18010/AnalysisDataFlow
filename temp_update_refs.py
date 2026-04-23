import re
path = r'e:\_src\AnalysisDataFlow\Struct\06-frontier\calvin-deterministic-streaming.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'## 8\. 引用参考 \(References\).*'
new_refs = """## 8. 引用参考 (References)

[^1]: A. Thomson et al., "Calvin: Fast Distributed Transactions for Partitioned Database Systems", Proc. SIGMOD, 2012.

[^2]: FaunaDB, "FaunaDB Architecture: Calvin-based Distributed Transactions at Scale," Fauna Engineering Blog, 2020. <https://fauna.com/blog/distributed-transaction-protocol>

[^3]: J. C. Corbett et al., "Spanner: Google's Globally-Distributed Database", Proc. OSDI, 2012.

[^4]: K. M. Chandy and L. Lamport, "Distributed Snapshots: Determining Global States of Distributed Systems", ACM TOCS, 3(1), 1985.

[^5]: T. Akidau et al., "The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing", PVLDB, 8(12), 2015.

[^6]: D. Ongaro and J. Ousterhout, "In Search of an Understandable Consensus Algorithm", Proc. USENIX ATC, 2014.

[^7]: L. Lamport, "Paxos Made Simple", ACM SIGACT News, 32(4), 2001.

[^8]: M. Kleppmann, "Designing Data-Intensive Applications", O'Reilly Media, 2017.

---

*文档版本: v1.1 | 更新日期: 2026-04-24 | 状态: Complete | 形式化元素统计: Def × 6, Thm × 3, Lemma × 2, Prop × 2 | Mermaid 图: 6 | 引用: 8*

---

*文档版本: v1.0 | 创建日期: 2026-04-19*"""

new_content = re.sub(pattern, new_refs, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done')
