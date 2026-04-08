'use client';

import { useState } from 'react';
import { challenges } from '@/lib/challenges';
import ChallengeCard from '@/components/ChallengeCard';
import { Button } from '@/components/ui/button';
import { useProgress } from '@/hooks/useProgress';
import { Trophy, Target, Code, Filter } from 'lucide-react';

export default function ChallengesPage() {
  const [filter, setFilter] = useState<'all' | 'easy' | 'medium' | 'hard'>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const { progress } = useProgress();

  const categories = Array.from(new Set(challenges.map(c => c.category)));

  const filteredChallenges = challenges.filter(c => {
    if (filter !== 'all' && c.difficulty !== filter) return false;
    if (categoryFilter !== 'all' && c.category !== categoryFilter) return false;
    return true;
  });

  const completedCount = progress.challenges.filter(c => c.completed).length;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Trophy className="w-8 h-8 text-amber-500" />
          <h1 className="text-3xl font-bold text-slate-900">编程挑战</h1>
        </div>
        <p className="text-slate-600">
          通过实战编程挑战巩固所学知识，从基础API到高级特性，共 {challenges.length} 个挑战
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">{completedCount}</div>
          <div className="text-sm text-slate-600">已完成</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">
            {challenges.filter(c => c.difficulty === 'easy').length}
          </div>
          <div className="text-sm text-slate-600">简单</div>
        </div>
        <div className="bg-amber-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-amber-600">
            {challenges.filter(c => c.difficulty === 'medium').length}
          </div>
          <div className="text-sm text-slate-600">中等</div>
        </div>
        <div className="bg-red-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-red-600">
            {challenges.filter(c => c.difficulty === 'hard').length}
          </div>
          <div className="text-sm text-slate-600">困难</div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4 mb-8">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-500" />
          <span className="text-sm text-slate-600">难度筛选:</span>
          <div className="flex gap-2">
            {(['all', 'easy', 'medium', 'hard'] as const).map((f) => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`px-3 py-1 text-sm rounded-full transition-colors ${
                  filter === f
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {f === 'all' ? '全部' : f === 'easy' ? '简单' : f === 'medium' ? '中等' : '困难'}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Code className="w-4 h-4 text-slate-500" />
          <span className="text-sm text-slate-600">分类:</span>
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="px-3 py-1 text-sm rounded-full border border-slate-200 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">全部</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Challenge Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredChallenges.map((challenge) => {
          const challengeProgress = progress.challenges.find(c => c.challengeId === challenge.id);
          return (
            <ChallengeCard
              key={challenge.id}
              challenge={challenge}
              isCompleted={challengeProgress?.completed || false}
              attempts={challengeProgress?.attempts || 0}
            />
          );
        })}
      </div>

      {filteredChallenges.length === 0 && (
        <div className="text-center py-12">
          <Target className="w-12 h-12 text-slate-300 mx-auto mb-4" />
          <p className="text-slate-500">没有找到符合条件的挑战</p>
          <Button
            variant="outline"
            className="mt-4"
            onClick={() => { setFilter('all'); setCategoryFilter('all'); }}
          >
            清除筛选
          </Button>
        </div>
      )}
    </div>
  );
}
