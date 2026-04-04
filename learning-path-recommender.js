/**
 * AnalysisDataFlow 学习路径推荐器 v2.0
 * 
 * 功能：
 * 1. 基于用户当前知识水平推荐学习路径
 * 2. 输入：已掌握的定理/定义列表
 * 3. 输出：推荐学习的下一个概念
 * 4. 算法：拓扑排序 + 依赖满足度
 * 5. 集成到知识图谱页面
 * 
 * @version 2.0.0
 * @author AnalysisDataFlow Team
 */

class LearningPathRecommender {
    constructor() {
        this.graphData = null;
        this.nodes = new Map();
        this.edges = [];
        this.dependencyGraph = new Map();
        this.reverseDependencyGraph = new Map();
        this.nodeScores = new Map();
        this.userProgress = new Set();
        this.cache = new Map();
    }

    /**
     * 设置图谱数据
     * @param {Object} graphData - 图谱数据对象
     */
    setGraphData(graphData) {
        this.graphData = graphData;
        this.buildIndexes();
        this.computeNodeImportance();
    }

    /**
     * 构建索引
     */
    buildIndexes() {
        this.nodes.clear();
        this.edges = [];
        this.dependencyGraph.clear();
        this.reverseDependencyGraph.clear();

        // 索引节点
        if (this.graphData.nodes) {
            this.graphData.nodes.forEach(node => {
                this.nodes.set(node.id, {
                    ...node,
                    inDegree: 0,
                    outDegree: 0,
                    dependencyCount: 0,
                    dependentCount: 0
                });
                this.dependencyGraph.set(node.id, new Set());
                this.reverseDependencyGraph.set(node.id, new Set());
            });
        }

        // 索引边（依赖关系）
        if (this.graphData.edges) {
            this.graphData.edges.forEach(edge => {
                this.edges.push(edge);
                
                // 依赖关系
                if (edge.type === 'dependency' || edge.type === 'depends_on') {
                    if (this.dependencyGraph.has(edge.target)) {
                        this.dependencyGraph.get(edge.target).add(edge.source);
                    }
                    if (this.reverseDependencyGraph.has(edge.source)) {
                        this.reverseDependencyGraph.get(edge.source).add(edge.target);
                    }
                    
                    // 更新节点的度
                    const targetNode = this.nodes.get(edge.target);
                    const sourceNode = this.nodes.get(edge.source);
                    if (targetNode) {
                        targetNode.inDegree++;
                        targetNode.dependencyCount++;
                    }
                    if (sourceNode) {
                        sourceNode.outDegree++;
                        sourceNode.dependentCount++;
                    }
                }
                
                // 引用关系也视为弱依赖
                if (edge.type === 'citation' || edge.type === 'references') {
                    if (this.dependencyGraph.has(edge.target)) {
                        this.dependencyGraph.get(edge.target).add(edge.source);
                    }
                }
            });
        }
    }

    /**
     * 计算节点重要性
     */
    computeNodeImportance() {
        this.nodeScores.clear();
        
        // PageRank-like 算法
        const dampingFactor = 0.85;
        const iterations = 20;
        const nodeIds = Array.from(this.nodes.keys());
        const numNodes = nodeIds.length;
        
        if (numNodes === 0) return;
        
        // 初始化分数
        nodeIds.forEach(id => {
            this.nodeScores.set(id, 1 / numNodes);
        });
        
        // 迭代计算
        for (let i = 0; i < iterations; i++) {
            const newScores = new Map();
            
            nodeIds.forEach(id => {
                let score = (1 - dampingFactor) / numNodes;
                
                // 从依赖该节点的其他节点获得分数
                const dependents = this.reverseDependencyGraph.get(id) || new Set();
                dependents.forEach(dependentId => {
                    const dependentScore = this.nodeScores.get(dependentId) || 0;
                    const dependentOutDegree = this.nodes.get(dependentId)?.outDegree || 1;
                    score += dampingFactor * dependentScore / dependentOutDegree;
                });
                
                newScores.set(id, score);
            });
            
            this.nodeScores = newScores;
        }
        
        // 归一化
        const maxScore = Math.max(...this.nodeScores.values());
        if (maxScore > 0) {
            nodeIds.forEach(id => {
                this.nodeScores.set(id, (this.nodeScores.get(id) || 0) / maxScore);
            });
        }
    }

    /**
     * 基于已掌握的概念推荐下一个学习内容
     * @param {string[]} knownConcepts - 已掌握的定理/定义ID列表
     * @param {Object} options - 配置选项
     * @returns {Array} 推荐列表
     */
    recommend(knownConcepts, options = {}) {
        const {
            limit = 10,
            includePrerequisites = true,
            prioritizeCompleteness = true,
            minDependencyRatio = 0.5
        } = options;
        
        // 更新用户进度
        this.userProgress = new Set(knownConcepts);
        
        // 缓存键
        const cacheKey = `rec_${knownConcepts.sort().join(',')}_${limit}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }
        
        // 计算每个候选节点的得分
        const candidates = [];
        
        this.nodes.forEach((node, id) => {
            // 跳过已掌握的内容
            if (this.userProgress.has(id)) return;
            
            // 只推荐形式化元素和文档
            if (!['theorem', 'definition', 'lemma', 'proposition', 'corollary', 'document'].includes(node.type)) {
                return;
            }
            
            // 计算依赖满足度
            const dependencies = this.dependencyGraph.get(id) || new Set();
            const satisfiedDeps = Array.from(dependencies).filter(dep => this.userProgress.has(dep));
            const dependencyRatio = dependencies.size > 0 ? satisfiedDeps.length / dependencies.size : 1;
            
            // 如果依赖满足度太低，跳过（除非是入门内容）
            if (dependencies.size > 0 && dependencyRatio < minDependencyRatio) {
                return;
            }
            
            // 计算推荐得分
            const score = this.calculateScore(node, {
                dependencyRatio,
                satisfiedDeps: satisfiedDeps.length,
                totalDeps: dependencies.size
            });
            
            candidates.push({
                id,
                name: node.label || node.id,
                type: node.type,
                score: score.total,
                components: score.components,
                dependencies: Array.from(dependencies),
                satisfiedDependencies: satisfiedDeps,
                dependencyRatio,
                path: node.metadata?.path || '',
                reason: this.generateReason(node, score, dependencyRatio)
            });
        });
        
        // 排序：先按依赖满足度，再按综合得分
        candidates.sort((a, b) => {
            if (prioritizeCompleteness) {
                if (Math.abs(a.dependencyRatio - b.dependencyRatio) > 0.1) {
                    return b.dependencyRatio - a.dependencyRatio;
                }
            }
            return b.score - a.score;
        });
        
        const result = candidates.slice(0, limit);
        this.cache.set(cacheKey, result);
        
        return result;
    }

    /**
     * 从特定节点推荐相关内容
     * @param {string} nodeId - 起始节点ID
     * @param {Object} options - 配置选项
     * @returns {Array} 推荐列表
     */
    recommendFromNode(nodeId, options = {}) {
        const { limit = 5, depth = 2 } = options;
        
        const node = this.nodes.get(nodeId);
        if (!node) return [];
        
        // 获取相关节点
        const relatedNodes = new Set();
        const visited = new Set([nodeId]);
        const queue = [{ id: nodeId, level: 0 }];
        
        while (queue.length > 0) {
            const { id, level } = queue.shift();
            
            if (level >= depth) continue;
            
            // 获取依赖该节点的节点
            const dependents = this.reverseDependencyGraph.get(id) || new Set();
            dependents.forEach(depId => {
                if (!visited.has(depId)) {
                    visited.add(depId);
                    relatedNodes.add(depId);
                    queue.push({ id: depId, level: level + 1 });
                }
            });
            
            // 获取该节点依赖的节点（前置知识）
            const dependencies = this.dependencyGraph.get(id) || new Set();
            dependencies.forEach(depId => {
                if (!visited.has(depId)) {
                    visited.add(depId);
                    relatedNodes.add(depId);
                    queue.push({ id: depId, level: level + 1 });
                }
            });
        }
        
        // 为相关节点打分
        const candidates = [];
        relatedNodes.forEach(id => {
            const relatedNode = this.nodes.get(id);
            if (!relatedNode) return;
            
            const nodeScore = this.nodeScores.get(id) || 0;
            const importance = this.calculateImportance(relatedNode);
            
            candidates.push({
                id,
                name: relatedNode.label || id,
                type: relatedNode.type,
                score: nodeScore * importance,
                dependencies: Array.from(this.dependencyGraph.get(id) || new Set()),
                path: relatedNode.metadata?.path || '',
                reason: `与 "${node.label || nodeId}" 相关联`
            });
        });
        
        candidates.sort((a, b) => b.score - a.score);
        return candidates.slice(0, limit);
    }

    /**
     * 计算节点推荐得分
     * @param {Object} node - 节点对象
     * @param {Object} context - 上下文信息
     * @returns {Object} 得分详情
     */
    calculateScore(node, context) {
        const { dependencyRatio, satisfiedDeps, totalDeps } = context;
        
        // 1. 基础重要性得分 (0-1)
        const importanceScore = this.nodeScores.get(node.id) || 0;
        
        // 2. 依赖满足度得分 (0-1)
        const dependencyScore = dependencyRatio;
        
        // 3. 学习进度得分 - 前置知识越完整越好
        const progressScore = totalDeps > 0 ? satisfiedDeps / totalDeps : 0.5;
        
        // 4. 类型权重
        const typeWeights = {
            'theorem': 1.0,
            'definition': 0.9,
            'lemma': 0.8,
            'proposition': 0.85,
            'corollary': 0.75,
            'document': 0.7
        };
        const typeScore = typeWeights[node.type] || 0.5;
        
        // 5. 层次深度得分 - 避免跳跃过大
        const levelScore = this.calculateLevelAppropriateness(node);
        
        // 综合得分
        const weights = {
            importance: 0.25,
            dependency: 0.30,
            progress: 0.20,
            type: 0.15,
            level: 0.10
        };
        
        const total = 
            importanceScore * weights.importance +
            dependencyScore * weights.dependency +
            progressScore * weights.progress +
            typeScore * weights.type +
            levelScore * weights.level;
        
        return {
            total,
            components: {
                importance: importanceScore,
                dependency: dependencyScore,
                progress: progressScore,
                type: typeScore,
                level: levelScore
            }
        };
    }

    /**
     * 计算节点重要性
     * @param {Object} node - 节点对象
     * @returns {number} 重要性得分
     */
    calculateImportance(node) {
        let score = 0;
        
        // 被引用次数
        score += (node.inDegree || 0) * 0.1;
        
        // 引用其他节点数
        score += (node.outDegree || 0) * 0.05;
        
        // 类型权重
        const typeWeights = {
            'theorem': 1.5,
            'definition': 1.3,
            'lemma': 1.0,
            'proposition': 1.1,
            'corollary': 0.9,
            'document': 0.8
        };
        score += typeWeights[node.type] || 0.5;
        
        // 归一化
        return Math.min(score / 5, 1);
    }

    /**
     * 计算层次适宜性
     * @param {Object} node - 节点对象
     * @returns {number} 适宜性得分
     */
    calculateLevelAppropriateness(node) {
        // 获取当前用户掌握的知识的平均层次
        let totalLevel = 0;
        let count = 0;
        
        this.userProgress.forEach(id => {
            const knownNode = this.nodes.get(id);
            if (knownNode && knownNode.metadata?.formality_level) {
                const level = parseInt(knownNode.metadata.formality_level.replace('L', ''));
                if (!isNaN(level)) {
                    totalLevel += level;
                    count++;
                }
            }
        });
        
        const avgKnownLevel = count > 0 ? totalLevel / count : 1;
        
        // 获取目标节点的层次
        let nodeLevel = 1;
        if (node.metadata?.formality_level) {
            const parsed = parseInt(node.metadata.formality_level.replace('L', ''));
            if (!isNaN(parsed)) nodeLevel = parsed;
        }
        
        // 理想的下一个层次是当前平均层次 + 1 或相同
        const levelDiff = Math.abs(nodeLevel - avgKnownLevel);
        
        // 层次差异越小越好
        return Math.max(0, 1 - levelDiff * 0.3);
    }

    /**
     * 生成推荐理由
     * @param {Object} node - 节点对象
     * @param {Object} score - 得分详情
     * @param {number} dependencyRatio - 依赖满足度
     * @returns {string} 推荐理由
     */
    generateReason(node, score, dependencyRatio) {
        const reasons = [];
        
        if (dependencyRatio >= 1) {
            reasons.push('前置知识已完备');
        } else if (dependencyRatio >= 0.7) {
            reasons.push('前置知识大部分已掌握');
        }
        
        if (score.components.importance > 0.7) {
            reasons.push('核心概念');
        }
        
        if (node.dependentCount > 5) {
            reasons.push(`被 ${node.dependentCount} 个概念依赖`);
        }
        
        if (node.type === 'theorem') {
            reasons.push('重要定理');
        } else if (node.type === 'definition') {
            reasons.push('基础定义');
        }
        
        return reasons.join(' · ') || '推荐学习';
    }

    /**
     * 生成完整学习路径
     * @param {string} targetId - 目标节点ID
     * @returns {Object} 学习路径
     */
    generateLearningPath(targetId) {
        const target = this.nodes.get(targetId);
        if (!target) return null;
        
        // 获取所有前置依赖
        const prerequisites = this.getAllPrerequisites(targetId);
        
        // 拓扑排序
        const sorted = this.topologicalSort(prerequisites, targetId);
        
        // 分组为学习阶段
        const stages = this.organizeIntoStages(sorted);
        
        return {
            target: {
                id: targetId,
                name: target.label || targetId,
                type: target.type
            },
            stages,
            totalSteps: sorted.length,
            estimatedHours: this.estimateStudyTime(sorted)
        };
    }

    /**
     * 获取所有前置依赖
     * @param {string} nodeId - 节点ID
     * @returns {Set} 前置依赖集合
     */
    getAllPrerequisites(nodeId) {
        const prerequisites = new Set();
        const visited = new Set();
        
        const visit = (id) => {
            if (visited.has(id)) return;
            visited.add(id);
            
            const deps = this.dependencyGraph.get(id) || new Set();
            deps.forEach(dep => {
                prerequisites.add(dep);
                visit(dep);
            });
        };
        
        visit(nodeId);
        return prerequisites;
    }

    /**
     * 拓扑排序
     * @param {Set} nodes - 节点集合
     * @param {string} targetId - 目标节点
     * @returns {Array} 排序后的节点列表
     */
    topologicalSort(nodes, targetId) {
        const nodeIds = Array.from(nodes);
        const inDegree = new Map();
        const adjList = new Map();
        
        // 初始化
        nodeIds.forEach(id => {
            inDegree.set(id, 0);
            adjList.set(id, []);
        });
        
        // 构建邻接表
        nodeIds.forEach(id => {
            const deps = this.dependencyGraph.get(id) || new Set();
            deps.forEach(dep => {
                if (nodes.has(dep)) {
                    adjList.get(dep).push(id);
                    inDegree.set(id, inDegree.get(id) + 1);
                }
            });
        });
        
        // Kahn算法
        const queue = [];
        const result = [];
        
        nodeIds.forEach(id => {
            if (inDegree.get(id) === 0) {
                queue.push(id);
            }
        });
        
        while (queue.length > 0) {
            // 优先选择重要性高的节点
            queue.sort((a, b) => (this.nodeScores.get(b) || 0) - (this.nodeScores.get(a) || 0));
            
            const current = queue.shift();
            result.push(current);
            
            adjList.get(current).forEach(neighbor => {
                inDegree.set(neighbor, inDegree.get(neighbor) - 1);
                if (inDegree.get(neighbor) === 0) {
                    queue.push(neighbor);
                }
            });
        }
        
        return result;
    }

    /**
     * 组织为学习阶段
     * @param {Array} sortedNodes - 排序后的节点
     * @returns {Array} 学习阶段
     */
    organizeIntoStages(sortedNodes) {
        const stages = [];
        const stageSize = 5; // 每个阶段5个节点
        
        for (let i = 0; i < sortedNodes.length; i += stageSize) {
            const stageNodes = sortedNodes.slice(i, i + stageSize);
            const items = stageNodes.map(id => {
                const node = this.nodes.get(id);
                return {
                    id,
                    name: node?.label || id,
                    type: node?.type || 'unknown',
                    estimatedHours: this.estimateNodeStudyTime(node)
                };
            });
            
            stages.push({
                name: `阶段 ${Math.floor(i / stageSize) + 1}`,
                items,
                totalHours: items.reduce((sum, item) => sum + item.estimatedHours, 0),
                description: this.generateStageDescription(items)
            });
        }
        
        return stages;
    }

    /**
     * 生成阶段描述
     * @param {Array} items - 阶段中的项目
     * @returns {string} 描述
     */
    generateStageDescription(items) {
        const types = new Set(items.map(i => i.type));
        if (types.has('definition') && types.has('theorem')) {
            return '学习基础定义和相关定理';
        } else if (types.has('definition')) {
            return '掌握核心定义';
        } else if (types.has('theorem')) {
            return '理解重要定理';
        } else {
            return '继续深入学习';
        }
    }

    /**
     * 估计单个节点的学习时间
     * @param {Object} node - 节点对象
     * @returns {number} 估计小时数
     */
    estimateNodeStudyTime(node) {
        if (!node) return 1;
        
        // 根据类型估计
        const typeHours = {
            'definition': 0.5,
            'theorem': 1.5,
            'lemma': 1.0,
            'proposition': 1.0,
            'corollary': 0.8,
            'document': 2.0
        };
        
        let hours = typeHours[node.type] || 1;
        
        // 根据形式化等级调整
        if (node.metadata?.formality_level) {
            const level = parseInt(node.metadata.formality_level.replace('L', ''));
            if (!isNaN(level)) {
                hours *= (1 + level * 0.2);
            }
        }
        
        // 根据字数调整
        if (node.metadata?.word_count) {
            hours += node.metadata.word_count / 5000;
        }
        
        return Math.round(hours * 10) / 10;
    }

    /**
     * 估计总学习时间
     * @param {Array} nodeIds - 节点ID列表
     * @returns {number} 估计总小时数
     */
    estimateStudyTime(nodeIds) {
        return nodeIds.reduce((sum, id) => {
            const node = this.nodes.get(id);
            return sum + this.estimateNodeStudyTime(node);
        }, 0);
    }

    /**
     * 获取学习进度统计
     * @returns {Object} 统计信息
     */
    getProgressStats() {
        const total = this.nodes.size;
        const known = this.userProgress.size;
        const byType = {};
        const byGroup = {};
        
        this.userProgress.forEach(id => {
            const node = this.nodes.get(id);
            if (node) {
                byType[node.type] = (byType[node.type] || 0) + 1;
                byGroup[node.group] = (byGroup[node.group] || 0) + 1;
            }
        });
        
        return {
            total,
            known,
            percentage: total > 0 ? Math.round((known / total) * 100) : 0,
            byType,
            byGroup,
            remaining: total - known
        };
    }

    /**
     * 清除缓存
     */
    clearCache() {
        this.cache.clear();
    }
}

// 导出
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LearningPathRecommender;
}
