#!/usr/bin/env python3
"""
外部链接健康检测与修复脚本 v4.1 (T3任务)

功能:
1. 扫描项目中所有 .md 文件的外部链接
2. 对高优先级链接进行批量可用性检测 (抽样+高价值优先)
3. 分类记录结果
4. 修复确认失效的链接
5. 生成 EXTERNAL-LINK-AUDIT-v4.1.md 报告
"""

import re
import json
import time
import random
import requests
import threading
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 配置
ROOT_DIR = Path(".")
OUTPUT_REPORT = ROOT_DIR / "EXTERNAL-LINK-AUDIT-v4.1.md"
EXTERNAL_LINKS_FILE = ROOT_DIR / ".scripts" / ".external_links_extracted.json"
PREV_RESULTS_FILE = ROOT_DIR / ".scripts" / ".link_health_results.json"
CACHE_FILE = ROOT_DIR / ".scripts" / ".link_audit_cache_v4.1.json"

TIMEOUT_SECONDS = 8
MAX_RETRIES = 2
CONCURRENT_LIMIT = 25
DELAY_BETWEEN_REQUESTS = 0.15
MAX_URLS_TO_CHECK = 450

# 高价值/高优先级域名
HIGH_VALUE_DOMAINS = {
    'nightlies.apache.org', 'flink.apache.org', 'github.com',
    'doi.org', 'dl.acm.org', 'arxiv.org', 'en.wikipedia.org',
    'cwiki.apache.org', 'issues.apache.org', 'kafka.apache.org',
    'spark.apache.org', 'paimon.apache.org', 'arrow.apache.org',
    'pekko.apache.org', 'downloads.apache.org', 'dist.apache.org',
    'www.apache.org', 'calcite.apache.org', 'pulsar.apache.org',
    'docs.risingwave.com', 'risingwave.com', 'www.risingwave.dev',
    'kubernetes.io', 'doc.rust-lang.org', 'docs.scala-lang.org',
    'go.dev', 'cloud.google.com', 'aws.amazon.com', 'azure.microsoft.com',
    'docs.microsoft.com', 'developers.google.com', 'stripe.com',
    'www.uber.com', 'netflixtechblog.com', 'engineering.linkedin.com',
    'blog.cloudflare.com', 'developers.cloudflare.com', 'martin.kleppmann.com',
    'ocw.mit.edu', 'pdos.csail.mit.edu', 'www.cs.cmu.edu', 'www.usenix.org',
    'www.vldb.org', 'cidrdb.org', 'link.springer.com', 'www.cambridge.org',
    'www.oreilly.com', 'www.confluent.io', 'www.ververica.com',
    'www.mongodb.com', 'neo4j.com', 'opentelemetry.io', 'materialize.com',
    'temporal.io', 'code.visualstudio.com', 'stackoverflow.com',
    'coq.inria.fr', 'lean-lang.org', 'isabelle.in.tum.de', 'nusmv.fbk.eu',
    'spinroot.com', 'uppaal.org', 'jepsen.io', 'bartoszmilewski.com',
    'softwarefoundations.cis.upenn.edu', 'iris-project.org',
    'leanprover-community.github.io', 'leanprover.github.io',
    'homotopytypetheory.org', 'rocq-prover.org', 'cvc5.github.io',
    'cpntools.org', 'plv.mpi-sws.org', 'verdi.uwplse.org',
    'groups.google.com', 'gist.github.com', 'raw.githubusercontent.com',
    'repo1.maven.org', 'mermaid.js.org', 'mermaid.live',
    'www.youtube.com', 'zenodo.org', 'www.distributed-systems.net',
    'www.sciencedirect.com', 'www.ijcai.org', 'www.morganclaypool.com',
    'www.routledge.com', 'resources.flexera.com', 'www.flexera.com',
    'www.cs.ox.ac.uk', 'www.cs.huji.ac.il', 'users.cs.duke.edu',
    'sites.cs.ucsb.edu', 'web.science.mq.edu.au', 'adamartin18010.github.io',
    'sre.google', 'v8.dev', 'bytecodealliance.org', 'platform.uno',
    'modelcontextprotocol.io', 'neuralnetworkverification.github.io',
    'www.tensorflow.org', 'www.flink-forward.org', 'www.mediatek.com',
    'www.conduktor.io', 'streamkap.com', 'etcd.io', 'developer.nvidia.com',
    'operatorframework.io', 'glue.us-east-1.amazonaws.com',
    's3tables.us-west-2.amazonaws.com', 'coq.discourse.group',
    'dlcdn.apache.org', 'example.com', 'lamport.azurewebsites.net',
    'blog.jonhoo.no', 'xiaohongshu.tech', 'www.usingcsp.com',
    'api.cloudf', 'json-schem',
}

# 已知链接替换映射
URL_REPLACEMENTS = {
    'https://bytecodealliance.org/articles/wasi-0-3': 'https://bytecodealliance.org/articles',
    'https://platform.uno/blog/state-of-webassembly-2025-2026': 'https://platform.uno/blog/',
    'https://neuralnetworkverification.github.io/marabou': 'https://github.com/NeuralNetworkVerification/Marabou',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/incremental_checkpoints':
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpointing/',
    'https://modelcontextprotocol.io/spec': 'https://modelcontextprotocol.io/specification',
    'https://www.flink-forward.org/global-2024': 'https://www.flink-forward.org/',
    'https://github.com/zio/zio-streams': 'https://github.com/zio/zio',
    'https://github.com/apache/flink/tree/master/flink-docs/docs/flips':
        'https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals',
    'https://github.com/WebAssembly/WASI/blob/main/wasip2/README.md':
        'https://github.com/WebAssembly/WASI/blob/main/README.md',
    'https://github.com/irontools/iron-functions': 'https://github.com/iron-io/functions',
    'https://github.com/irontools/iron-functions/releases': 'https://github.com/iron-io/functions/releases',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/state/state':
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/state/',
    'https://doi.org/10.1109/ACCESS.2020.3025677': 'https://ieeexplore.ieee.org/document/9210124',
    'https://github.com/nusmv/nusmv': 'https://nusmv.fbk.eu/',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/queryable_state':
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/queryable_state/',
    'https://docs.risingwave.com/docs/current/architecture': 'https://docs.risingwave.com/docs/current/architecture-overview/',
    'https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/link-health-check.yml':
        '[内部CI链接 - 需手动验证]',
    'https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/check-links.yml/badge.svg':
        '[内部CI Badge - 需手动验证]',
    'https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/update-stats.yml/badge.svg':
        '[内部CI Badge - 需手动验证]',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/exactly-once':
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/exactly_once/',
    'https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/operations/autoscaling':
        'https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/operations/',
    'https://analysisdataflow.github.io/docs': '[项目文档站点 - 待部署]',
    'https://discuss.analysisdataflow.org': '[社区讨论版 - 待部署]',
    'https://cert.analysisdataflow.org': '[认证系统 - 待部署]',
    'https://xiaohongshu.tech/': '[链接已失效]',
    'https://blog.jonhoo.no/': 'https://thesquareplanet.com/blog/',
    'https://api.cloudf': '[链接不完整 - 需手动修复]',
    'http://json-schem': '[链接不完整 - 需手动修复]',
    'https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c':
        'https://gist.github.com/sindresorhus',
    'http://www.usingcsp.com/': '[CSP资源站点 - 链接已失效]',
    'https://github.com/your-org/AnalysisDataFlow': 'https://github.com/luyanfeng/AnalysisDataFlow',
    'https://github.com/your-org/AnalysisDataFlow/releases/tag/v3.0.0': 'https://github.com/luyanfeng/AnalysisDataFlow/releases/tag/v3.0.0',
    'https://github.com/your-org/AnalysisDataFlow/releases/tag/v2.8.0': 'https://github.com/luyanfeng/AnalysisDataFlow/releases/tag/v2.8.0',
    'https://bytecodealliance.org/articles/WASI-Preview-2': 'https://bytecodealliance.org/articles',
    'https://arrow.apache.org/benchmarks': 'https://arrow.apache.org/',
    'https://arrow.apache.org/docs/java': 'https://arrow.apache.org/docs/',
    'https://cs263.readthedocs.io': '[链接已失效: cs263.readthedocs.io]',
    'https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-stable/docs/operations/autoscaler': 'https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-stable/docs/operations/',
    'https://homotopytypetheory.org/2017/01/30/higher-inductive-types-tour': 'https://homotopytypetheory.org/2017/01/30/higher-inductive-types-tour/',
    'https://www.cs.cmu.edu/~fp/courses/theorem-proving': 'https://www.cs.cmu.edu/~fp/courses/theorem-proving/',
    'https://materialize.com/blog/flink-tco-analysis-20': 'https://materialize.com/blog/',
    'https://materialize.com/blog/flink-tco-analysis-2026': 'https://materialize.com/blog/',
    'https://blog.cloudflare.com/pipelines-ga': 'https://blog.cloudflare.com/',
    'http://spinroot.com/spin/maillist.html': 'https://spinroot.com/spin/',
    'https://www.risingwave.dev/blog': 'https://www.risingwave.dev/',
    'https://pdos.csail.mit.edu/6.826': 'https://pdos.csail.mit.edu/6.826/',
    'https://ocw.mit.edu/courses/6-826-principles-of-computer-systems-fall-2002': 'https://ocw.mit.edu/courses/6-826-principles-of-computer-systems/',
    'https://paimon.apache.org/docs/master/flink/lookup-joins': 'https://paimon.apache.org/docs/master/flink/',
    'https://paimon.apache.org/docs/master/flink/materialized-table': 'https://paimon.apache.org/docs/master/flink/',
    'https://flink.apache.org/news/2021/01/11/incremental-checkpointing.html': 'https://flink.apache.org/',
    'https://flink.apache.org/documentation/exactly-once.html': 'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/exactly_once/',
    'https://developers.cloudflare.com/pipelines/sinks/r2': 'https://developers.cloudflare.com/pipelines/',
    'https://developers.cloudflare.com/pipelines/sources/kafka': 'https://developers.cloudflare.com/pipelines/',
    'https://kafka.apache.org/documentation/transactions': 'https://kafka.apache.org/documentation/#transactionalproducer',
    'https://kafka.apache.org/documentation/producer-configs': 'https://kafka.apache.org/documentation/#producerconfigs',
    'https://docs.risingwave.com/sql/udfs/udfs': 'https://docs.risingwave.com/sql/udfs/',
    'https://etcd.io/docs/v3.5/learning/raft': 'https://etcd.io/docs/v3.5/learning/raft/',
    'https://www.confluent.io/blog/kafka-streams-vs-fli': 'https://www.confluent.io/blog/',
    'https://lamport.azurewebsites.net/pubs/tla+book.pdf': 'https://lamport.azurewebsites.net/tla/book.html',
    'https://cwiki.apache.org/confluence/display/FLINK/FLIP-531': 'https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals',
    'https://cwiki.apache.org/confluence/display/FLINK/FLIP-500': 'https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals',
    'https://platform.uno/blog/webassembly-memory64-performance': 'https://platform.uno/blog/',
    'https://www.ververica.com/blog/stream-processing-concepts': 'https://www.ververica.com/blog/',
    'https://doi.org/10.1145/3698034': '[DOI: 10.1145/3698034]',
    'https://doi.org/10.1145/3138088': '[DOI: 10.1145/3138088]',
    'https://doi.ieeecomputersociety.org/10.1109/ICDE60146.2024': '[DOI: 10.1109/ICDE60146.2024]',
    'https://link.springer.com/article/10.1023/A:1022964117327': '[Springer - Article]',
    'https://link.springer.com/chapter/10.1007/3-540-49099-X_21': '[Springer - Chapter]',
    'https://users.cs.duke.edu/~badi/papers/cap.pdf': 'https://users.cs.duke.edu/~badi/papers/cap.pdf',
    'https://repo1.maven.org/maven2/org/apache/flink/${artifact}/${VERSION}': '[Maven坐标模板 - 需替换变量]',
    'https://glue.us-east-1.amazonaws.com': '[AWS Glue API端点 - 需按区域配置]',
    'https://aws.amazon.com/blogs/big-data/etl-on-aws': 'https://aws.amazon.com/blogs/big-data/',
}


class LinkAuditor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        self.results = []
        self.fix_log = []
        self.files_modified = set()
        self.checked_urls = set()

    def load_external_links(self):
        """加载已提取的外部链接"""
        with open(EXTERNAL_LINKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_prev_results(self):
        """加载之前的检测结果"""
        if not PREV_RESULTS_FILE.exists():
            return None
        with open(PREV_RESULTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_cache(self):
        """加载检测缓存"""
        if CACHE_FILE.exists():
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_cache(self, cache):
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    def normalize_url(self, url):
        url = url.split('#')[0]
        if url.endswith('/') and url.count('/') > 3:
            url = url.rstrip('/')
        return url

    def check_url(self, url, source_files):
        """检测单个URL的可用性"""
        url = self.normalize_url(url)

        if url in self.checked_urls:
            return None
        self.checked_urls.add(url)

        result = {
            'url': url,
            'source_files': source_files,
            'status_code': None,
            'category': 'unknown',
            'is_accessible': False,
            'error_message': None,
            'response_time_ms': 0,
            'redirect_url': None,
            'check_time': datetime.now().isoformat(),
        }

        # 跳过明显不需要检测的链接
        if 'localhost' in url or '127.0.0.1' in url:
            result['category'] = 'localhost'
            result['error_message'] = 'Localhost link - development only'
            return result

        if 'analysisdataflow.org' in url and 'github.com' not in url:
            result['category'] = 'internal_domain'
            result['error_message'] = 'Internal domain not yet deployed'
            return result

        if 'github.com/your-org' in url:
            result['category'] = 'placeholder'
            result['error_message'] = 'Placeholder link'
            return result

        session = requests.Session()
        session.headers.update(self.session.headers)

        for attempt in range(MAX_RETRIES):
            start = time.time()
            try:
                resp = session.head(
                    url,
                    timeout=TIMEOUT_SECONDS,
                    allow_redirects=True,
                    verify=False
                )
                elapsed = (time.time() - start) * 1000
                result['response_time_ms'] = round(elapsed, 2)
                result['status_code'] = resp.status_code
                result['redirect_url'] = str(resp.url) if resp.history else None

                if resp.status_code == 200:
                    result['is_accessible'] = True
                    result['category'] = 'ok'
                elif resp.status_code in (301, 302, 307, 308):
                    result['is_accessible'] = True
                    result['category'] = 'redirect'
                elif resp.status_code == 404:
                    result['category'] = 'not_found'
                    result['error_message'] = 'HTTP 404 Not Found'
                elif resp.status_code == 403:
                    result['category'] = 'forbidden'
                    result['error_message'] = 'HTTP 403 Forbidden'
                elif resp.status_code == 405:
                    # HEAD 不允许，尝试 GET
                    resp2 = session.get(
                        url,
                        timeout=TIMEOUT_SECONDS,
                        allow_redirects=True,
                        verify=False
                    )
                    result['status_code'] = resp2.status_code
                    result['redirect_url'] = str(resp2.url) if resp2.history else None
                    result['is_accessible'] = 200 <= resp2.status_code < 400
                    if resp2.status_code == 404:
                        result['category'] = 'not_found'
                        result['error_message'] = 'HTTP 404 Not Found'
                    elif result['is_accessible']:
                        result['category'] = 'ok'
                    else:
                        result['category'] = 'other'
                        result['error_message'] = f'HTTP {resp2.status_code}'
                elif 400 <= resp.status_code < 500:
                    result['category'] = 'client_error'
                    result['error_message'] = f'HTTP {resp.status_code}'
                elif 500 <= resp.status_code < 600:
                    result['category'] = 'server_error'
                    result['error_message'] = f'HTTP {resp.status_code}'
                else:
                    result['is_accessible'] = 200 <= resp.status_code < 400
                    result['category'] = 'ok' if result['is_accessible'] else 'other'

                break  # 成功，不需要重试

            except requests.exceptions.Timeout:
                result['category'] = 'timeout'
                result['error_message'] = 'Connection timeout'
                result['response_time_ms'] = TIMEOUT_SECONDS * 1000
            except requests.exceptions.SSLError as e:
                result['category'] = 'ssl_error'
                result['error_message'] = f'SSL Error: {str(e)[:50]}'
            except requests.exceptions.ConnectionError as e:
                result['category'] = 'connection_error'
                result['error_message'] = f'Connection Error: {str(e)[:50]}'
            except Exception as e:
                result['category'] = 'other'
                result['error_message'] = f'Error: {str(e)[:50]}'

            if attempt < MAX_RETRIES - 1:
                time.sleep(1 + attempt)

        time.sleep(DELAY_BETWEEN_REQUESTS + random.uniform(0, 0.1))
        return result

    def select_urls_to_check(self, url_to_files):
        """选择需要检测的URL（抽样+高价值优先，确保域名覆盖）"""
        prev_results = self.load_prev_results()
        prev_by_url = {}
        if prev_results:
            for r in prev_results.get('results', []):
                prev_by_url[self.normalize_url(r['url'])] = r

        # 按域名分组
        domain_to_urls = defaultdict(list)
        for url, files in url_to_files.items():
            domain = urlparse(url).netloc
            domain_to_urls[domain].append((url, files))

        # 为每个域名内的URL打分排序
        domain_scored = {}
        for domain, urls in domain_to_urls.items():
            is_high_value = domain in HIGH_VALUE_DOMAINS or any(
                d in domain for d in HIGH_VALUE_DOMAINS
            )
            scored = []
            for url, files in urls:
                norm_url = self.normalize_url(url)
                prev = prev_by_url.get(norm_url)
                score = 0

                # 高价值域名加分
                if is_high_value:
                    score += 10

                # 之前检测结果可疑的加分
                if prev:
                    code = prev.get('status_code')
                    err = prev.get('error_message', '') or ''
                    if code == 404:
                        score += 20
                    elif 'Connection Error' in err:
                        score += 15
                    elif 'Timeout' in err:
                        score += 5
                    elif code == 200:
                        score += 2  # 验证通过的也适度检测
                    elif code in (301, 302):
                        score += 3

                # 引用次数多的加分
                score += min(len(files), 5)

                scored.append((score, url, files))

            scored.sort(reverse=True)
            domain_scored[domain] = scored

        selected = []
        domain_count = defaultdict(int)

        # 第一轮：每个域名最多选2个，优先高价值/可疑
        for domain, scored in domain_scored.items():
            limit = 2 if domain in HIGH_VALUE_DOMAINS or any(d in domain for d in HIGH_VALUE_DOMAINS) else 1
            for score, url, files in scored[:limit]:
                selected.append((url, files))
                domain_count[domain] += 1

        # 第二轮：如果还有余量，补充到每个域名最多3个（仅高价值）或2个
        for domain, scored in domain_scored.items():
            if len(selected) >= MAX_URLS_TO_CHECK:
                break
            limit = 3 if domain in HIGH_VALUE_DOMAINS or any(d in domain for d in HIGH_VALUE_DOMAINS) else 2
            for score, url, files in scored[domain_count[domain]:limit]:
                if len(selected) >= MAX_URLS_TO_CHECK:
                    break
                selected.append((url, files))
                domain_count[domain] += 1

        # 去重
        seen = set()
        unique_selected = []
        for url, files in selected:
            if url not in seen:
                seen.add(url)
                unique_selected.append((url, files))

        return unique_selected[:MAX_URLS_TO_CHECK]

    def run_check(self):
        """执行检测"""
        url_to_files = self.load_external_links()
        print(f"📊 项目中共有 {len(url_to_files)} 个唯一外部链接")

        selected = self.select_urls_to_check(url_to_files)
        print(f"🎯 选定检测链接数: {len(selected)}")

        # 统计域名覆盖
        domains = set(urlparse(u).netloc for u, _ in selected)
        print(f"🌐 覆盖域名数: {len(domains)}")

        results = []
        total = len(selected)
        completed = 0
        lock = threading.Lock()

        def check_one(args):
            nonlocal completed
            url, files = args
            result = self.check_url(url, files)
            with lock:
                completed += 1
                if result:
                    results.append(result)
                    status = "✅ OK" if result['is_accessible'] else f"❌ {result['category']}"
                    print(f"[{completed}/{total}] {status} {url[:70]}...")
                else:
                    print(f"[{completed}/{total}] ⏭️ Skipped {url[:70]}...")
            return result

        print(f"\n🚀 开始并发检测 (并发数: {CONCURRENT_LIMIT})...")
        with ThreadPoolExecutor(max_workers=CONCURRENT_LIMIT) as executor:
            list(executor.map(check_one, selected))

        self.results = results
        return results

    def fix_broken_links(self):
        """修复失效链接"""
        fixed_count = 0
        manual_count = 0

        broken = [r for r in self.results if not r['is_accessible']]
        print(f"\n🔧 开始修复 {len(broken)} 个失效链接...")

        for result in broken:
            url = result['url']
            replacement = None

            # 查找替换映射（只使用精确匹配）
            replacement = URL_REPLACEMENTS.get(url)

            if replacement:
                for filepath in result['source_files']:
                    success, msg = self._replace_in_file(filepath, url, replacement)
                    if success:
                        fixed_count += 1
                        self.fix_log.append({
                            'file': filepath,
                            'old_url': url,
                            'new_url': replacement,
                            'status': 'fixed',
                            'category': result['category']
                        })
                        print(f"  ✓ Fixed: {filepath}")
                    else:
                        print(f"  ⚠ Failed to fix {filepath}: {msg}")
            else:
                for filepath in result['source_files']:
                    manual_count += 1
                    self.fix_log.append({
                        'file': filepath,
                        'old_url': url,
                        'new_url': None,
                        'status': 'manual_required',
                        'category': result['category']
                    })

        return fixed_count, manual_count

    def _replace_in_file(self, filepath, old_url, new_url):
        """在文件中精确替换链接，避免破坏Markdown语法"""
        try:
            full_path = ROOT_DIR / filepath
            if not full_path.exists():
                return False, "File not found"

            content = full_path.read_text(encoding='utf-8')
            original = content

            # 准备两种形式的URL（带/不带末尾斜杠）
            urls_to_try = [old_url]
            if old_url.endswith('/') and old_url.count('/') > 3:
                urls_to_try.append(old_url.rstrip('/'))
            elif not old_url.endswith('/') and not old_url.endswith(('.html', '.md', '.pdf', '.png', '.jpg')):
                urls_to_try.append(old_url + '/')

            for target_url in urls_to_try:
                # 策略1: 替换Markdown链接中的URL [text](url)
                md_pattern = re.compile(r'(\[([^\]]+)\]\()' + re.escape(target_url) + r'(\))')
                content = md_pattern.sub(r'\1' + new_url + r'\3', content)

                # 策略2: 替换引用定义 [ref]: url
                ref_pattern = re.compile(r'(\[[^\]]+\]:\s*)' + re.escape(target_url) + r'(\s*$)', re.MULTILINE)
                content = ref_pattern.sub(r'\1' + new_url + r'\2', content)

                # 策略3: 替换裸URL <url>，但保留尖括号
                bare_pattern = re.compile(r'(<)' + re.escape(target_url) + r'(>)')
                content = bare_pattern.sub(r'\1' + new_url + r'\2', content)

                # 策略4: 替换HTML href
                href_pattern = re.compile(r'(href=["\'])' + re.escape(target_url) + r'(["\'])')
                content = href_pattern.sub(r'\1' + new_url + r'\2', content)

            if content != original:
                full_path.write_text(content, encoding='utf-8')
                self.files_modified.add(str(filepath))
                return True, "Replaced"
            return False, "No change"
        except Exception as e:
            return False, str(e)

    def generate_report(self):
        """生成检测报告"""
        total = len(self.results)
        ok = [r for r in self.results if r['category'] == 'ok']
        redirect = [r for r in self.results if r['category'] == 'redirect']
        not_found = [r for r in self.results if r['category'] == 'not_found']
        timeout_links = [r for r in self.results if r['category'] == 'timeout']
        ssl_error = [r for r in self.results if r['category'] == 'ssl_error']
        forbidden = [r for r in self.results if r['category'] == 'forbidden']
        client_error = [r for r in self.results if r['category'] == 'client_error']
        server_error = [r for r in self.results if r['category'] == 'server_error']
        connection_error = [r for r in self.results if r['category'] == 'connection_error']
        other_error = [r for r in self.results if r['category'] in ('other', 'unknown', 'internal_domain', 'localhost', 'placeholder')]

        failed = [r for r in self.results if not r['is_accessible']]

        fixed = [x for x in self.fix_log if x['status'] == 'fixed']
        manual = [x for x in self.fix_log if x['status'] == 'manual_required']
        fixed_unique_urls = len(set(x['old_url'] for x in fixed))
        manual_unique_urls = len(set(x['old_url'] for x in manual))

        all_files = set()
        for r in self.results:
            all_files.update(r['source_files'])

        report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        lines = [
            "# 外部链接健康检测与修复报告 v4.1",
            "",
            f"> **检测时间**: {report_time}",
            f"> **检测文档数**: {len(all_files)}",
            f"> **检测链接数**: {total}",
            f"> **覆盖域名数**: {len(set(urlparse(r['url']).netloc for r in self.results))}",
            "",
            "## 📊 检测统计",
            "",
            "### 总体统计",
            "",
            "| 类别 | 数量 | 百分比 | 状态 |",
            "|------|------|--------|------|",
            f"| 总检测链接数 | {total} | 100% | - |",
            f"| 200 OK | {len(ok)} | {len(ok)/total*100:.1f}% | ✅ |",
            f"| 301/302 重定向* | {len(redirect)} | {len(redirect)/total*100:.1f}% | 🔄 |",
            f"| 404 Not Found | {len(not_found)} | {len(not_found)/total*100:.1f}% | ❌ |",
            f"| 连接超时 | {len(timeout_links)} | {len(timeout_links)/total*100:.1f}% | ⏱️ |",
            f"| SSL 错误 | {len(ssl_error)} | {len(ssl_error)/total*100:.1f}% | 🔒 |",
            f"| 403 Forbidden | {len(forbidden)} | {len(forbidden)/total*100:.1f}% | 🚫 |",
            f"| 其他客户端错误 (4xx) | {len(client_error)} | {len(client_error)/total*100:.1f}% | ⚠️ |",
            f"| 服务器错误 (5xx) | {len(server_error)} | {len(server_error)/total*100:.1f}% | 🔥 |",
            f"| 连接错误 | {len(connection_error)} | {len(connection_error)/total*100:.1f}% | 🔌 |",
            f"| 其他/特殊 | {len(other_error)} | {len(other_error)/total*100:.1f}% | 📌 |",
            f"| **失效链接总计** | **{len(failed)}** | **{len(failed)/total*100:.1f}%** | ❌ |",
            "",
            '> *注: 重定向链接因请求自动跟随，大部分最终返回 200 OK，已计入 200 OK 统计中。',
            "",
            "### 按域名分类统计 (Top 30)",
            "",
            "| 域名 | 检测数 | 有效 | 失效 | 主要问题 |",
            "|------|--------|------|------|----------|",
        ]

        domain_stats = defaultdict(lambda: {'total': 0, 'ok': 0, 'failed': 0, 'issues': Counter()})
        for r in self.results:
            d = urlparse(r['url']).netloc
            domain_stats[d]['total'] += 1
            if r['is_accessible']:
                domain_stats[d]['ok'] += 1
            else:
                domain_stats[d]['failed'] += 1
                domain_stats[d]['issues'][r['category']] += 1

        for d, s in sorted(domain_stats.items(), key=lambda x: -x[1]['total'])[:30]:
            top_issue = s['issues'].most_common(1)
            issue_str = top_issue[0][0] if top_issue else '-'
            lines.append(f"| {d} | {s['total']} | {s['ok']} | {s['failed']} | {issue_str} |")

        lines.append("")

        # 修复记录
        lines.extend([
            "## 🔧 修复记录",
            "",
            f"**已自动修复**: {fixed_unique_urls} 个唯一 URL (涉及 {len(fixed)} 个文件位置)",
            f"**待人工确认**: {manual_unique_urls} 个唯一 URL (涉及 {len(manual)} 个文件位置)",
            f"**修改文件数**: {len(self.files_modified)} 个",
            "",
            "### 已修复链接清单",
            "",
            "| 原链接 | 修复后链接/标记 | 来源文档 | 问题类型 |",
            "|--------|----------------|----------|----------|",
        ])

        shown_urls = set()
        for item in fixed:
            if item['old_url'] in shown_urls:
                continue
            shown_urls.add(item['old_url'])
            old = item['old_url'][:60] + '...' if len(item['old_url']) > 60 else item['old_url']
            new = item['new_url'][:60] + '...' if len(item['new_url']) > 60 else item['new_url']
            lines.append(f"| `{old}` | `{new}` | `{item['file']}` | {item['category']} |")
            if len(shown_urls) >= 50:
                break

        if len(shown_urls) >= 50:
            lines.append(f"| ... | ... | ... | *还有 {fixed_unique_urls - 50} 个* |")

        lines.append("")

        # 失效清单
        if failed:
            lines.extend([
                "## ❌ 失效链接清单",
                "",
                "| 链接 | 问题类型 | 错误信息 | 来源文档 |",
                "|------|----------|----------|----------|",
            ])
            for r in sorted(failed, key=lambda x: x['url'])[:80]:
                url_display = r['url'][:55] + '...' if len(r['url']) > 55 else r['url']
                files = ', '.join(r['source_files'][:2])
                err = (r['error_message'] or r['category'])[:30]
                lines.append(f"| `{url_display}` | {r['category']} | {err} | `{files[:30]}` |")
            if len(failed) > 80:
                lines.append(f"| ... | ... | ... | *还有 {len(failed) - 80} 个* |")
            lines.append("")

        # 待人工确认清单
        if manual:
            lines.extend([
                "## ⏳ 待人工确认清单",
                "",
                "| 链接 | 问题类型 | 来源文档 | 建议操作 |",
                "|------|----------|----------|----------|",
            ])
            for item in manual[:50]:
                url_display = item['old_url'][:50] + '...' if len(item['old_url']) > 50 else item['old_url']
                suggestion = {
                    'not_found': '查找Wayback Machine存档或替代链接',
                    'timeout': '稍后重试或寻找替代源',
                    'ssl_error': '检查证书或使用HTTP替代',
                    'forbidden': '确认是否需要认证或寻找公开镜像',
                    'connection_error': '检查域名是否已下线',
                }.get(item['category'], '手动检查确认')
                lines.append(f"| `{url_display}` | {item['category']} | `{item['file']}` | {suggestion} |")
            if len(manual) > 50:
                lines.append(f"| ... | ... | ... | *还有 {len(manual) - 50} 个* |")
            lines.append("")

        # 自动化建议
        lines.extend([
            "## 🤖 自动化建议",
            "",
            "### 短期行动",
            "1. **部署内部服务**: `analysisdataflow.org` 及相关子域名的服务需要尽快部署",
            "2. **替换占位符**: 将文档中剩余的 `your-org` 占位符替换为实际组织名",
            "3. **Wayback存档**: 对无法找到替代的失效学术/博客链接，优先使用 Wayback Machine 存档",
            "",
            "### 中期优化",
            "1. **建立链接白名单**: 对已知稳定的官方文档源（Apache Flink、GitHub）建立快速通道",
            "2. **智能重定向跟踪**: 对 301 重定向链接，开发自动更新脚本批量替换为最终目标 URL",
            "3. **月度检测**: 建议每月运行一次外部链接健康检查，保持链接库更新",
            "",
            "### 长期治理",
            "1. **链接集中管理**: 考虑将高频引用的外部链接维护到统一的引用库中",
            "2. **DOI优先策略**: 学术论文优先使用 DOI 链接，提高长期稳定性",
            "3. **文档版本锁定**: 对 Flink 等快速迭代的文档，明确标注检测时的文档版本",
            "",
            "## 📈 统计摘要",
            "",
            "```",
            f"检测时间: {report_time}",
            f"检测文档: {len(all_files)} 个",
            f"检测链接: {total} 个",
            f"覆盖域名: {len(set(urlparse(r['url']).netloc for r in self.results))} 个",
            f"  - 200 OK: {len(ok)} 个 ({len(ok)/total*100:.1f}%)",
            f"  - 重定向: {len(redirect)} 个 ({len(redirect)/total*100:.1f}%)",
            f"  - 失效: {len(failed)} 个 ({len(failed)/total*100:.1f}%)",
            f"    - 404 Not Found: {len(not_found)} 个",
            f"    - Timeout: {len(timeout_links)} 个",
            f"    - SSL Error: {len(ssl_error)} 个",
            f"    - 403 Forbidden: {len(forbidden)} 个",
            f"    - Connection Error: {len(connection_error)} 个",
            f"    - Other: {len(client_error) + len(server_error) + len(other_error)} 个",
            f"已修复: {len(fixed)} 个",
            f"待人工确认: {len(manual)} 个",
            "```",
            "",
            "---",
            "",
            "*此报告由 AnalysisDataFlow 外部链接审计脚本自动生成*",
            f"*生成时间: {report_time}*",
        ])

        report = '\n'.join(lines)
        OUTPUT_REPORT.write_text(report, encoding='utf-8')
        print(f"\n📝 报告已保存: {OUTPUT_REPORT}")

        # 保存JSON结果
        json_output = ROOT_DIR / ".scripts" / ".link_audit_results_v4.1.json"
        with open(json_output, 'w', encoding='utf-8') as f:
            json.dump({
                'check_time': report_time,
                'total': total,
                'ok': len(ok),
                'redirect': len(redirect),
                'failed': len(failed),
                'fixed': len(fixed),
                'manual': len(manual),
                'domains': len(set(urlparse(r['url']).netloc for r in self.results)),
                'results': self.results,
                'fix_log': self.fix_log,
            }, f, ensure_ascii=False, indent=2)
        print(f"📊 JSON结果已保存: {json_output}")

        return total, len(failed), len(fixed)


def main():
    auditor = LinkAuditor()
    results = auditor.run_check()
    fixed, manual = auditor.fix_broken_links()
    total, failed, fixed_count = auditor.generate_report()

    print("\n" + "=" * 60)
    print("外部链接审计完成!")
    print(f"  检测总数: {total}")
    print(f"  失效数: {failed}")
    print(f"  修复数: {fixed_count}")
    print(f"  待人工确认: {manual}")
    print("=" * 60)


if __name__ == '__main__':
    main()
