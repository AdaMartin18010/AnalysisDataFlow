'use client';

import { useState } from 'react';
import { Challenge } from '@/lib/challenges';
import CodeEditor from '@/components/CodeEditor';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, CheckCircle, XCircle, Trophy, RotateCcw } from 'lucide-react';
import Link from 'next/link';
import { useProgress } from '@/hooks/useProgress';

interface ChallengeClientProps {
  challenge: Challenge;
}

export default function ChallengeClient({ challenge }: ChallengeClientProps) {
  const { saveChallenge, progress } = useProgress();
  const [result, setResult] = useState<'success' | 'error' | null>(null);

  const challengeProgress = progress.challenges.find(c => c.challengeId === challenge.id);

  const handleSubmit = (code: string) => {
    // Simplified evaluation - in real app, this would run tests
    const hasRequiredElements = 
      code.includes('env.execute') &&
      (code.includes('DataStream') ||
      code.includes('public static void main'));
    
    if (hasRequiredElements) {
      setResult('success');
      saveChallenge(challenge.id, code, true);
    } else {
      setResult('error');
      saveChallenge(challenge.id, code, false);
    }
  };

  const difficultyLabels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  };

  const difficultyColors = {
    easy: 'bg-green-100 text-green-800',
    medium: 'bg-amber-100 text-amber-800',
    hard: 'bg-red-100 text-red-800'
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link href="/challenges/" className="text-slate-500 hover:text-slate-700 flex items-center gap-1 mb-4">
          <ArrowLeft className="w-4 h-4" />
          返回挑战列表
        </Link>
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className={`px-2 py-1 rounded text-sm font-medium ${difficultyColors[challenge.difficulty]}`}>
                {difficultyLabels[challenge.difficulty]}
              </span>
              <Badge variant="secondary">{challenge.category}</Badge>
              {challengeProgress?.completed && (
                <Badge variant="success" className="flex items-center gap-1">
                  <Trophy className="w-3 h-3" />
                  已完成
                </Badge>
              )}
            </div>
            <h1 className="text-3xl font-bold text-slate-900">{challenge.title}</h1>
          </div>
        </div>
        <p className="text-slate-600 mt-2">{challenge.description}</p>
      </div>

      {result === 'success' && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
          <CheckCircle className="w-6 h-6 text-green-600" />
          <div>
            <p className="font-medium text-green-800">挑战完成！</p>
            <p className="text-sm text-green-600">你的代码通过了基本检查。</p>
          </div>
        </div>
      )}

      {result === 'error' && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-3">
          <XCircle className="w-6 h-6 text-red-600" />
          <div>
            <p className="font-medium text-red-800">代码需要改进</p>
            <p className="text-sm text-red-600">请检查是否包含必要的Flink组件。</p>
          </div>
          <Button
            variant="outline"
            size="sm"
            className="ml-auto"
            onClick={() => setResult(null)}
          >
            <RotateCcw className="w-4 h-4 mr-1" />
            重试
          </Button>
        </div>
      )}

      <div className="h-[600px]">
        <CodeEditor
          starterCode={challenge.starterCode}
          solution={challenge.solution}
          hints={challenge.hints}
          onSubmit={handleSubmit}
        />
      </div>

      <div className="mt-8 bg-slate-50 rounded-lg p-6">
        <h2 className="text-lg font-semibold text-slate-900 mb-4">测试用例</h2>
        {challenge.testCases.length > 0 ? (
          <div className="space-y-3">
            {challenge.testCases.map((testCase, index) => (
              <div key={index} className="bg-white rounded p-3 border">
                <div className="flex items-center gap-4 text-sm">
                  <div>
                    <span className="text-slate-500">输入:</span>
                    <code className="ml-2 bg-slate-100 px-2 py-1 rounded">{testCase.input || '(无)'}</code>
                  </div>
                  <div>
                    <span className="text-slate-500">期望输出:</span>
                    <code className="ml-2 bg-slate-100 px-2 py-1 rounded">{testCase.expected}</code>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-slate-500 text-sm">
            此挑战需要本地Flink环境才能运行完整测试。
          </p>
        )}
      </div>
    </div>
  );
}
