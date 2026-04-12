#!/bin/bash
# AnalysisDataFlow SEO维护脚本
# 版本: 4.2 | 更新日期: 2026-04-12
# 用途: 自动化SEO维护任务

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
PROJECT_ROOT="$(dirname "$(dirname "$(readlink -f "$0")")")"
SITEMAP_URL="https://analysisdataflow.github.io/sitemap.xml"
ROBOTS_URL="https://analysisdataflow.github.io/robots.txt"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  AnalysisDataFlow SEO 维护工具 v4.2${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 函数: 显示帮助
show_help() {
    echo "用法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  validate      验证SEO文件有效性"
    echo "  update-dates  更新SEO文件日期"
    echo "  check-links   检查死链"
    echo "  compress      压缩资源文件"
    echo "  full-check    执行完整检查"
    echo "  help          显示此帮助"
    echo ""
}

# 函数: 验证Sitemap
validate_sitemap() {
    echo -e "${YELLOW}[1/5] 验证 Sitemap.xml...${NC}"
    
    if [ ! -f "$PROJECT_ROOT/sitemap.xml" ]; then
        echo -e "${RED}✗ sitemap.xml 不存在${NC}"
        return 1
    fi
    
    # 检查XML格式
    if command -v xmllint &> /dev/null; then
        if xmllint --noout "$PROJECT_ROOT/sitemap.xml" 2>/dev/null; then
            echo -e "${GREEN}✓ Sitemap XML格式有效${NC}"
        else
            echo -e "${RED}✗ Sitemap XML格式错误${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}! xmllint 未安装，跳过XML验证${NC}"
    fi
    
    # 统计URL数量
    URL_COUNT=$(grep -o '<loc>' "$PROJECT_ROOT/sitemap.xml" | wc -l)
    echo -e "${GREEN}✓ Sitemap包含 $URL_COUNT 个URL${NC}"
}

# 函数: 验证Robots.txt
validate_robots() {
    echo -e "${YELLOW}[2/5] 验证 Robots.txt...${NC}"
    
    if [ ! -f "$PROJECT_ROOT/robots.txt" ]; then
        echo -e "${RED}✗ robots.txt 不存在${NC}"
        return 1
    fi
    
    # 检查必要的指令
    if grep -q "User-agent:" "$PROJECT_ROOT/robots.txt"; then
        echo -e "${GREEN}✓ Robots.txt 包含 User-agent 指令${NC}"
    else
        echo -e "${RED}✗ Robots.txt 缺少 User-agent 指令${NC}"
    fi
    
    if grep -q "Sitemap:" "$PROJECT_ROOT/robots.txt"; then
        echo -e "${GREEN}✓ Robots.txt 包含 Sitemap 引用${NC}"
    else
        echo -e "${RED}✗ Robots.txt 缺少 Sitemap 引用${NC}"
    fi
}

# 函数: 验证结构化数据
validate_structured_data() {
    echo -e "${YELLOW}[3/5] 验证结构化数据...${NC}"
    
    if [ ! -f "$PROJECT_ROOT/structured-data.json" ]; then
        echo -e "${RED}✗ structured-data.json 不存在${NC}"
        return 1
    fi
    
    # 检查JSON格式
    if command -v jq &> /dev/null; then
        if jq empty "$PROJECT_ROOT/structured-data.json" 2>/dev/null; then
            echo -e "${GREEN}✓ 结构化数据 JSON格式有效${NC}"
        else
            echo -e "${RED}✗ 结构化数据 JSON格式错误${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}! jq 未安装，跳过JSON验证${NC}"
    fi
    
    # 检查必要的Schema类型
    if grep -q '"@type": "WebSite"' "$PROJECT_ROOT/structured-data.json"; then
        echo -e "${GREEN}✓ 包含 WebSite Schema${NC}"
    fi
    
    if grep -q '"@type": "Organization"' "$PROJECT_ROOT/structured-data.json"; then
        echo -e "${GREEN}✓ 包含 Organization Schema${NC}"
    fi
}

# 函数: 更新文件日期
update_dates() {
    echo -e "${YELLOW}[4/5] 更新文件日期...${NC}"
    
    CURRENT_DATE=$(date +%Y-%m-%d)
    CURRENT_DATETIME=$(date +"%Y-%m-%d %H:%M:%S")
    
    # 更新robots.txt日期
    if [ -f "$PROJECT_ROOT/robots.txt" ]; then
        sed -i "s/Updated: .*/Updated: $CURRENT_DATE (Q2-3 SEO优化)/" "$PROJECT_ROOT/robots.txt"
        echo -e "${GREEN}✓ 更新 robots.txt 日期${NC}"
    fi
    
    echo -e "${GREEN}✓ 日期更新完成${NC}"
}

# 函数: 检查死链 (简化版)
check_links() {
    echo -e "${YELLOW}[5/5] 检查内部链接...${NC}"
    
    echo -e "${BLUE}提示: 使用 lychee 进行完整死链检查${NC}"
    echo -e "  安装: cargo install lychee"
    echo -e "  运行: lychee --verbose './**/*.md'"
    
    # 统计链接数量
    LINK_COUNT=$(find "$PROJECT_ROOT" -name "*.md" -exec grep -o '\[.*\](.*)' {} \; | wc -l)
    echo -e "${GREEN}✓ 发现约 $LINK_COUNT 个Markdown链接${NC}"
}

# 函数: 完整检查
full_check() {
    echo -e "${BLUE}执行完整SEO检查...${NC}"
    echo ""
    
    validate_sitemap
    validate_robots
    validate_structured_data
    update_dates
    check_links
    
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  SEO检查完成!${NC}"
    echo -e "${GREEN}========================================${NC}"
}

# 主程序
case "${1:-}" in
    validate)
        validate_sitemap
        validate_robots
        validate_structured_data
        ;;
    update-dates)
        update_dates
        ;;
    check-links)
        check_links
        ;;
    compress)
        echo "压缩功能待实现"
        ;;
    full-check)
        full_check
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        exit 1
        ;;
esac
