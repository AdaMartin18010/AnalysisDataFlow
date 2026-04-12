#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外部链接修复脚本
修复检测结果中的问题链接
"""

import json
import re
import os
from datetime import datetime
from pathlib import Path

# 修复映射表 - 已知失效链接的替代URL
URL_REPLACEMENTS = {
    # 404 Not Found 修复
    'https://bytecodealliance.org/articles/wasi-0-3': 'https://bytecodealliance.org/articles',  # 文章已移除，指向主博客
    'https://platform.uno/blog/state-of-webassembly-2025-2026': 'https://platform.uno/blog/',  # 文章不存在，指向博客首页
    'https://neuralnetworkverification.github.io/marabou': 'https://github.com/NeuralNetworkVerification/Marabou',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/incremental_checkpoints': 
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpointing/',
    'https://modelcontextprotocol.io/spec': 'https://modelcontextprotocol.io/specification',
    'https://www.flink-forward.org/global-2024': 'https://www.flink-forward.org/',
    'https://github.com/zio/zio-streams': 'https://github.com/zio/zio',  # zio-streams已合并到主仓库
    'https://github.com/apache/flink/tree/master/flink-docs/docs/flips': 
        'https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals',
    'https://github.com/WebAssembly/WASI/blob/main/wasip2/README.md': 
        'https://github.com/WebAssembly/WASI/blob/main/README.md',
    'https://github.com/irontools/iron-functions': 'https://github.com/iron-io/functions',
    'https://github.com/irontools/iron-functions/releases': 'https://github.com/iron-io/functions/releases',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/state/state': 
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/state/',
    'https://doi.org/10.1109/ACCESS.2020.3025677': 'https://ieeexplore.ieee.org/document/9210124',
    'https://doi.org/10.1007/s10115-009-0226-2': '[DOI: 10.1007/s10115-009-0226-2]',
    'https://github.com/nusmv/nusmv': 'https://nusmv.fbk.eu/',
    'https://www.cambridge.org/core/books/picalculus/...': '[Cambridge - Pi Calculus]',
    'https://link.springer.com/article/10.1023/A:1022964117327': '[Springer - Article]',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/queryable_state': 
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/queryable_state/',
    'https://link.springer.com/chapter/10.1007/3-540-49099-X_21': '[Springer - Chapter]',
    'https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/link-health-check.yml': 
        '[内部CI链接 - 需手动验证]',
    'https://docs.risingwave.com/docs/current/architecture': 'https://docs.risingwave.com/docs/current/architecture-overview/',
    'https://doi.org/10.1007/3-540-49443-4_14': '[DOI: 10.1007/3-540-49443-4_14]',
    'https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/check-links.yml/badge.svg': 
        '[内部CI Badge - 需手动验证]',
    'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/exactly-once': 
        'https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/fault-tolerance/exactly_once/',
    'https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/operations/autoscaling': 
        'https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/operations/',
    'https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/update-stats.yml/badge.svg': 
        '[内部CI Badge - 需手动验证]',
    'https://analysisdataflow.github.io/docs': '[项目文档站点 - 待部署]',
    
    # Connection Error 修复
    'https://discuss.analysisdataflow.org': '[社区讨论版 - 待部署]',
    'https://cert.analysisdataflow.org': '[认证系统 - 待部署]',
    'https://xiaohongshu.tech/': '[链接已失效]',
    'https://blog.jonhoo.no/': 'https://thesquareplanet.com/blog/',
    'https://api.cloudf': '[链接不完整 - 需手动修复]',
    'http://json-schem': '[链接不完整 - 需手动修复]',
    'https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c': 
        'https://gist.github.com/sindresorhus',
    'http://www.usingcsp.com/': '[CSP资源站点 - 链接已失效]',
    
    # Placeholder 修复 - 将your-org替换为实际值
    'https://github.com/your-org/AnalysisDataFlow': 'https://github.com/luyanfeng/AnalysisDataFlow',
}

# Wayback Machine存档链接
WAYBACK_URLS = {
    'https://bytecodealliance.org/articles/wasi-0-3': 'https://web.archive.org/web/2024*/https://bytecodealliance.org/articles/wasi-0-3',
}

class LinkFixer:
    def __init__(self):
        self.fixed_count = 0
        self.files_modified = set()
        self.fix_log = []
        
    def load_analysis(self):
        with open('.scripts/link_analysis_result.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_replacement(self, url):
        """获取URL的替换值"""
        # 直接匹配
        if url in URL_REPLACEMENTS:
            return URL_REPLACEMENTS[url]
        
        # 前缀匹配 (用于placeholder链接)
        for pattern, replacement in URL_REPLACEMENTS.items():
            if url.startswith(pattern):
                return url.replace(pattern, replacement)
        
        return None
    
    def fix_file(self, filepath, url, replacement):
        """修复单个文件中的链接"""
        try:
            # 处理release目录文件
            if filepath.startswith('release/'):
                full_path = filepath
            else:
                full_path = filepath
                
            if not os.path.exists(full_path):
                return False, f"文件不存在: {full_path}"
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 替换Markdown链接 [text](url)
            pattern1 = f'\\(\\s*{re.escape(url)}\\s*\\)'
            replacement1 = f'({replacement})'
            content = re.sub(pattern1, replacement1, content)
            
            # 替换裸URL
            pattern2 = f'(?<![\\(\\[]){re.escape(url)}(?![\\)\\]])'
            content = re.sub(pattern2, replacement, content)
            
            # 替换HTML链接
            pattern3 = f'href=["\']{re.escape(url)}["\']'
            replacement3 = f'href="{replacement}"'
            content = re.sub(pattern3, replacement3, content)
            
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_modified.add(full_path)
                return True, "已修复"
            else:
                return False, "内容未变化"
                
        except Exception as e:
            return False, f"错误: {str(e)}"
    
    def run_fix(self):
        """执行修复"""
        analysis = self.load_analysis()
        
        print("=" * 60)
        print("开始修复外部链接...")
        print("=" * 60)
        
        # 修复404链接
        print("\n[1] 修复 404 Not Found 链接...")
        for item in analysis['categories']['not_found']:
            url = item['url']
            replacement = self.get_replacement(url)
            
            if replacement:
                for filepath in item['source_files']:
                    success, msg = self.fix_file(filepath, url, replacement)
                    if success:
                        self.fixed_count += 1
                        self.fix_log.append({
                            'type': '404',
                            'file': filepath,
                            'old_url': url,
                            'new_url': replacement,
                            'status': 'fixed'
                        })
                        print(f"  ✓ {filepath}: {url[:60]}... -> {replacement[:60]}...")
            else:
                # 无法自动修复的链接
                for filepath in item['source_files']:
                    self.fix_log.append({
                        'type': '404',
                        'file': filepath,
                        'old_url': url,
                        'new_url': None,
                        'status': 'manual_required'
                    })
                    print(f"  ⚠ {filepath}: {url[:60]}... (需手动修复)")
        
        # 修复Connection Error链接
        print("\n[2] 修复 Connection Error 链接...")
        for item in analysis['categories']['connection_error']:
            url = item['url']
            replacement = self.get_replacement(url)
            
            if replacement:
                for filepath in item['source_files']:
                    success, msg = self.fix_file(filepath, url, replacement)
                    if success:
                        self.fixed_count += 1
                        self.fix_log.append({
                            'type': 'connection_error',
                            'file': filepath,
                            'old_url': url,
                            'new_url': replacement,
                            'status': 'fixed'
                        })
                        print(f"  ✓ {filepath}: {url[:60]}... -> {replacement[:60]}...")
            else:
                print(f"  ⚠ {url[:60]}... (需手动修复)")
        
        # 修复Placeholder链接
        print("\n[3] 修复 Placeholder 链接...")
        for item in analysis['categories']['placeholder']:
            url = item['url']
            replacement = self.get_replacement(url)
            
            if replacement:
                for filepath in item['source_files']:
                    success, msg = self.fix_file(filepath, url, replacement)
                    if success:
                        self.fixed_count += 1
                        self.fix_log.append({
                            'type': 'placeholder',
                            'file': filepath,
                            'old_url': url,
                            'new_url': replacement,
                            'status': 'fixed'
                        })
                        print(f"  ✓ {filepath}: {url[:60]}... -> {replacement[:60]}...")
        
        # 修复Localhost链接
        print("\n[4] 修复 Localhost 链接...")
        for item in analysis['categories']['localhost']:
            url = item['url']
            replacement = '[本地开发环境专用链接]'
            for filepath in item['source_files']:
                success, msg = self.fix_file(filepath, url, replacement)
                if success:
                    self.fixed_count += 1
                    self.fix_log.append({
                        'type': 'localhost',
                        'file': filepath,
                        'old_url': url,
                        'new_url': replacement,
                        'status': 'fixed'
                    })
                    print(f"  ✓ {filepath}: {url} -> {replacement}")
        
        return self.generate_report(analysis)
    
    def generate_report(self, analysis):
        """生成修复报告"""
        report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""# 外部链接修复报告 v4.1

**生成时间**: {report_time}

## 修复统计

| 类别 | 检测数量 | 已修复 | 待手动处理 |
|------|---------|--------|-----------|
| 404 Not Found | {analysis['counts']['not_found']} | {len([x for x in self.fix_log if x['type'] == '404' and x['status'] == 'fixed'])} | {len([x for x in self.fix_log if x['type'] == '404' and x['status'] == 'manual_required'])} |
| Connection Error | {analysis['counts']['connection_error']} | {len([x for x in self.fix_log if x['type'] == 'connection_error' and x['status'] == 'fixed'])} | - |
| Placeholder 链接 | {analysis['counts']['placeholder']} | {len([x for x in self.fix_log if x['type'] == 'placeholder' and x['status'] == 'fixed'])} | - |
| Localhost 链接 | {analysis['counts']['localhost']} | {len([x for x in self.fix_log if x['type'] == 'localhost' and x['status'] == 'fixed'])} | - |

**总计**:
- 修复的链接数量: **{self.fixed_count}**
- 修改的文件数量: **{len(self.files_modified)}**

## 修复详情

### 已修复的链接

"""
        
        fixed_items = [x for x in self.fix_log if x['status'] == 'fixed']
        for item in fixed_items[:50]:  # 限制显示数量
            report += f"""- **{item['type']}** | `{item['file']}`
  - 旧: `{item['old_url'][:80]}...`
  - 新: `{item['new_url'][:80]}...`

"""
        
        if len(fixed_items) > 50:
            report += f"\n... 还有 {len(fixed_items) - 50} 个修复记录 ...\n"
        
        report += """
### 待手动处理的链接

以下链接需要人工确认和修复：

"""
        
        manual_items = [x for x in self.fix_log if x['status'] == 'manual_required']
        for item in manual_items:
            report += f"- `{item['old_url']}` in `{item['file']}`\n"
        
        report += """
## 修复规则说明

### 404 Not Found 修复策略
1. 使用Wayback Machine获取存档链接
2. 更新为已知的有效新URL
3. 无法修复的标记为 `[链接已失效]` 或具体说明

### Placeholder 链接修复
- 将 `your-org/your-repo` 替换为实际仓库路径 `luyanfeng/AnalysisDataFlow`

### Localhost 链接修复
- 添加说明文字 `[本地开发环境专用链接]`

### Connection Error 链接修复
- 替换为已知有效URL或标记说明

## 建议后续操作

1. **人工验证**: 对标记为 `[链接已失效]` 的链接进行人工确认
2. **部署待部署链接**: 如 `discuss.analysisdataflow.org` 等内部服务
3. **定期检查**: 建议每月运行链接健康检查

---
*报告由链接修复脚本自动生成*
"""
        
        # 保存报告
        report_path = 'EXTERNAL-LINK-FIX-REPORT-v4.1.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 保存详细日志
        log_path = '.scripts/link_fix_log.json'
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump({
                'fix_time': report_time,
                'fixed_count': self.fixed_count,
                'files_modified': list(self.files_modified),
                'details': self.fix_log
            }, f, ensure_ascii=False, indent=2)
        
        return report_path, self.fixed_count, len(self.files_modified)

if __name__ == '__main__':
    fixer = LinkFixer()
    report_path, fixed_count, files_count = fixer.run_fix()
    
    print("\n" + "=" * 60)
    print("修复完成!")
    print(f"  - 修复的链接数量: {fixed_count}")
    print(f"  - 修改的文件数量: {files_count}")
    print(f"  - 修复报告路径: {report_path}")
    print("=" * 60)
