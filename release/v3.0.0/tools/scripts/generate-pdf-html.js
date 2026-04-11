/**
 * AnalysisDataFlow 白皮书 PDF 生成脚本 (HTML版本)
 * 使用 Playwright + Paged.js 生成高质量PDF
 * 
 * 优点:
 * - 更好的中文支持
 * - CSS控制排版
 * - 支持复杂图表
 * - 无需LaTeX环境
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// 白皮书配置
const WHITEPAPERS = {
  'streaming-technology-trends-2026': {
    title: '流计算技术趋势白皮书 2026',
    english_title: 'Streaming Technology Trends Whitepaper 2026',
    subtitle: '技术趋势预测、市场分析、选型指南',
    version: 'v1.0',
    date: '2026-04-08',
    pages: '40+',
    color: '#1f4e79'
  },
  'flink-enterprise-implementation-guide': {
    title: 'Flink企业落地指南',
    english_title: 'Flink Enterprise Implementation Guide',
    subtitle: '实施路线图、最佳实践、成功案例',
    version: 'v1.0',
    date: '2026-04-08',
    pages: '60+',
    color: '#1f4e79'
  },
  'realtime-ai-architecture-practice': {
    title: '实时AI架构实践白皮书',
    english_title: 'Real-Time AI Architecture Practice Whitepaper',
    subtitle: 'AI+流计算架构、生产案例、技术实现',
    version: 'v1.0',
    date: '2026-04-08',
    pages: '50+',
    color: '#1f4e79'
  }
};

// HTML模板
const HTML_TEMPLATE = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
  <script src="https://unpkg.com/pagedjs/dist/paged.polyfill.js"></script>
  <style>
    /* Paged.js 设置 */
    @page {
      size: A4;
      margin: 2.5cm;
      
      @top-center {
        content: string(chapter-title);
        font-size: 9pt;
        color: #666;
        border-bottom: 0.5pt solid #1f4e79;
        padding-bottom: 5pt;
      }
      
      @top-right {
        content: "AnalysisDataFlow Whitepaper";
        font-size: 9pt;
        color: #666;
      }
      
      @bottom-center {
        content: counter(page);
        font-size: 10pt;
        color: #333;
      }
      
      @bottom-left {
        content: "";
        border-top: 0.5pt solid #c5a464;
        width: 100%;
      }
    }
    
    @page:first {
      @top-center { content: none; }
      @top-right { content: none; }
      @bottom-center { content: none; }
      @bottom-left { content: none; }
    }
    
    @page cover {
      margin: 0;
      @top-center { content: none; }
      @top-right { content: none; }
      @bottom-center { content: none; }
      @bottom-left { content: none; }
    }
    
    @page toc {
      @top-center { content: "目录"; }
    }
    
    /* 基础样式 */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: "Noto Serif CJK SC", "Source Han Serif SC", "SimSun", serif;
      font-size: 11pt;
      line-height: 1.6;
      color: #333;
    }
    
    /* 封面样式 */
    .cover {
      page: cover;
      break-after: page;
      width: 210mm;
      height: 297mm;
      position: relative;
      overflow: hidden;
    }
    
    .cover-top {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 100mm;
      background: linear-gradient(135deg, #1f4e79 0%, #3a7bd5 100%);
    }
    
    .cover-gold-line {
      position: absolute;
      top: 100mm;
      left: 0;
      right: 0;
      height: 3mm;
      background: #c5a464;
    }
    
    .cover-content {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
      width: 80%;
    }
    
    .cover-org {
      font-size: 14pt;
      color: white;
      margin-bottom: 10mm;
      position: absolute;
      top: 20mm;
      left: 50%;
      transform: translateX(-50%);
    }
    
    .cover-badge {
      font-size: 28pt;
      font-weight: bold;
      color: white;
      letter-spacing: 3pt;
      position: absolute;
      top: 40mm;
      left: 50%;
      transform: translateX(-50%);
    }
    
    .cover-title {
      font-size: 32pt;
      font-weight: bold;
      color: #1f4e79;
      margin-bottom: 5mm;
      line-height: 1.3;
    }
    
    .cover-subtitle {
      font-size: 16pt;
      color: #666;
      margin-bottom: 3mm;
    }
    
    .cover-subtitle-cn {
      font-size: 12pt;
      color: #888;
      margin-bottom: 20mm;
    }
    
    .cover-divider {
      width: 60%;
      height: 2pt;
      background: #c5a464;
      margin: 15mm auto;
    }
    
    .cover-meta {
      font-size: 11pt;
      color: #333;
      line-height: 2;
    }
    
    .cover-url {
      position: absolute;
      bottom: 15mm;
      left: 50%;
      transform: translateX(-50%);
      font-size: 9pt;
      color: #888;
    }
    
    /* 目录样式 */
    .toc {
      page: toc;
      break-after: page;
    }
    
    .toc h2 {
      font-size: 18pt;
      color: #1f4e79;
      margin-bottom: 15pt;
      padding-bottom: 5pt;
      border-bottom: 2pt solid #1f4e79;
    }
    
    .toc ul {
      list-style: none;
      padding: 0;
    }
    
    .toc li {
      margin: 8pt 0;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
    }
    
    .toc a {
      color: #333;
      text-decoration: none;
      flex: 1;
    }
    
    .toc .level-1 { font-weight: bold; font-size: 11pt; }
    .toc .level-2 { padding-left: 15pt; font-size: 10pt; }
    .toc .level-3 { padding-left: 30pt; font-size: 9pt; color: #666; }
    
    /* 章节标题 */
    h1 {
      string-set: chapter-title content();
      font-size: 20pt;
      color: #1f4e79;
      margin: 30pt 0 15pt 0;
      padding-bottom: 8pt;
      border-bottom: 1.5pt solid #1f4e79;
      page-break-before: always;
    }
    
    h1:first-of-type {
      page-break-before: auto;
    }
    
    h2 {
      font-size: 14pt;
      color: #1f4e79;
      margin: 20pt 0 10pt 0;
    }
    
    h3 {
      font-size: 12pt;
      color: #1f4e79;
      margin: 15pt 0 8pt 0;
    }
    
    h4 {
      font-size: 11pt;
      color: #333;
      margin: 10pt 0 5pt 0;
    }
    
    /* 段落 */
    p {
      margin: 8pt 0;
      text-align: justify;
    }
    
    /* 表格 */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 15pt 0;
      font-size: 10pt;
    }
    
    th, td {
      border: 0.5pt solid #ddd;
      padding: 8pt;
      text-align: left;
    }
    
    th {
      background: #f5f5f5;
      font-weight: bold;
      color: #1f4e79;
    }
    
    tr:nth-child(even) {
      background: #fafafa;
    }
    
    /* 代码块 */
    pre {
      background: #f5f5f5;
      padding: 10pt;
      border-radius: 3pt;
      overflow-x: auto;
      font-size: 9pt;
      font-family: "Consolas", "Monaco", monospace;
      margin: 10pt 0;
      border-left: 3pt solid #1f4e79;
    }
    
    code {
      font-family: "Consolas", "Monaco", monospace;
      background: #f0f0f0;
      padding: 1pt 3pt;
      border-radius: 2pt;
      font-size: 9pt;
    }
    
    pre code {
      background: none;
      padding: 0;
    }
    
    /* 列表 */
    ul, ol {
      margin: 10pt 0;
      padding-left: 25pt;
    }
    
    li {
      margin: 5pt 0;
    }
    
    /* 引用块 */
    blockquote {
      border-left: 3pt solid #c5a464;
      padding-left: 15pt;
      margin: 15pt 0;
      color: #555;
      font-style: italic;
    }
    
    /* 图表标题 */
    figcaption, .caption {
      text-align: center;
      font-size: 9pt;
      color: #666;
      margin-top: 5pt;
    }
    
    /* 分页控制 */
    .page-break {
      break-after: page;
    }
    
    .no-break {
      break-inside: avoid;
    }
    
    /* 链接 */
    a {
      color: #1f4e79;
      text-decoration: none;
    }
    
    a:hover {
      text-decoration: underline;
    }
    
    /* 摘要框 */
    .abstract {
      background: #f8f9fa;
      border: 1pt solid #e9ecef;
      padding: 15pt;
      margin: 20pt 0;
      border-radius: 3pt;
    }
    
    .abstract h3 {
      margin-top: 0;
      color: #1f4e79;
    }
    
    /* 强调 */
    strong {
      color: #1f4e79;
    }
    
    /* 脚注 */
    .footnote {
      font-size: 8pt;
      color: #666;
      border-top: 0.5pt solid #ddd;
      padding-top: 5pt;
      margin-top: 20pt;
    }
  </style>
</head>
<body>
  <!-- 封面 -->
  <div class="cover">
    <div class="cover-top"></div>
    <div class="cover-gold-line"></div>
    <div class="cover-org">AnalysisDataFlow Project</div>
    <div class="cover-badge">WHITEPAPER</div>
    <div class="cover-content">
      <div class="cover-title">{{title}}</div>
      <div class="cover-subtitle">{{english_title}}</div>
      <div class="cover-subtitle-cn">{{subtitle}}</div>
      <div class="cover-divider"></div>
      <div class="cover-meta">
        <div><strong>版本:</strong> {{version}}</div>
        <div><strong>发布日期:</strong> {{date}}</div>
        <div><strong>规模:</strong> {{pages}} 页</div>
      </div>
    </div>
    <div class="cover-url">https://github.com/AnalysisDataFlow</div>
  </div>
  
  <!-- 目录 -->
  <div class="toc">
    <h2>目录</h2>
    <div id="toc-content"></div>
  </div>
  
  <!-- 正文内容 -->
  <div id="content">
    {{content}}
  </div>
</body>
</html>`;

async function markdownToHtml(markdownPath, config) {
  const markdown = fs.readFileSync(markdownPath, 'utf-8');
  
  // 简单的Markdown转HTML转换
  let html = markdown
    // 移除第一个H1（使用封面）
    .replace(/^# .+$/m, '')
    // 处理H1-H6
    .replace(/^###### (.+)$/gm, '<h6>$1</h6>')
    .replace(/^##### (.+)$/gm, '<h5>$1</h5>')
    .replace(/^#### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    // 处理代码块
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // 处理行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 处理粗体和斜体
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // 处理引用
    .replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>')
    // 处理无序列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.+<\/li>\n?)+/g, '<ul>$&</ul>')
    // 处理表格（简化）
    .replace(/\|(.+)\|/g, (match) => {
      const cells = match.split('|').filter(c => c.trim());
      return '<tr>' + cells.map(c => `<td>${c.trim()}</td>`).join('') + '</tr>';
    })
    // 处理段落
    .replace(/\n\n/g, '</p><p>')
    .replace(/^(.+)$/gm, (match, p1) => {
      if (!p1.match(/^<[hluo]/)) {
        return `<p>${p1}</p>`;
      }
      return p1;
    })
    // 清理空标签
    .replace(/<p><\/p>/g, '')
    .replace(/\n+/g, '\n');
  
  // 替换模板
  return HTML_TEMPLATE
    .replace(/{{title}}/g, config.title)
    .replace(/{{english_title}}/g, config.english_title)
    .replace(/{{subtitle}}/g, config.subtitle)
    .replace(/{{version}}/g, config.version)
    .replace(/{{date}}/g, config.date)
    .replace(/{{pages}}/g, config.pages)
    .replace(/{{content}}/g, html);
}

async function generatePdf(paperId, config, whitepapersDir, outputDir) {
  console.log(`📄 正在生成: ${config.title}`);
  
  const markdownPath = path.join(whitepapersDir, `${paperId}.md`);
  const outputPath = path.join(outputDir, `${paperId}.pdf`);
  
  if (!fs.existsSync(markdownPath)) {
    console.error(`❌ 未找到文件: ${markdownPath}`);
    return null;
  }
  
  // 启动浏览器
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // 生成HTML
  const html = await markdownToHtml(markdownPath, config);
  
  // 加载页面
  await page.setContent(html, { waitUntil: 'networkidle' });
  
  // 等待Paged.js渲染完成
  await page.waitForTimeout(3000);
  
  // 生成PDF
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '2.5cm',
      right: '2.5cm',
      bottom: '2.5cm',
      left: '2.5cm'
    }
  });
  
  await browser.close();
  
  const stats = fs.statSync(outputPath);
  console.log(`✅ 完成: ${outputPath} (${(stats.size / 1024).toFixed(1)} KB)`);
  
  return outputPath;
}

async function main() {
  const args = process.argv.slice(2);
  const specificPaper = args.find(arg => !arg.startsWith('--'));
  const outputDir = args.includes('--output') 
    ? args[args.indexOf('--output') + 1] 
    : 'whitepapers/pdf';
  
  const scriptDir = __dirname;
  const rootDir = path.join(scriptDir, '..');
  const whitepapersDir = path.join(rootDir, 'whitepapers');
  const pdfDir = path.join(rootDir, outputDir);
  
  // 确保输出目录存在
  if (!fs.existsSync(pdfDir)) {
    fs.mkdirSync(pdfDir, { recursive: true });
  }
  
  const papersToGenerate = specificPaper 
    ? { [specificPaper]: WHITEPAPERS[specificPaper] }
    : WHITEPAPERS;
  
  console.log('='.repeat(60));
  console.log('AnalysisDataFlow 白皮书 PDF 生成器 (HTML版)');
  console.log('='.repeat(60));
  
  const generated = [];
  for (const [paperId, config] of Object.entries(papersToGenerate)) {
    if (!config) {
      console.error(`❌ 未知的白皮书: ${paperId}`);
      continue;
    }
    
    const pdfPath = await generatePdf(paperId, config, whitepapersDir, pdfDir);
    if (pdfPath) {
      generated.push(pdfPath);
    }
  }
  
  console.log('\n' + '='.repeat(60));
  console.log(`✅ 生成完成! 共 ${generated.length}/${Object.keys(papersToGenerate).length} 个PDF`);
  console.log('='.repeat(60));
}

main().catch(console.error);
