'use client';

import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Code, CheckCircle, Trophy } from 'lucide-react';
import type { Challenge } from '@/lib/challenges';

interface ChallengeCardProps {
  challenge: Challenge;
  isCompleted?: boolean;
  attempts?: number;
}

export default function ChallengeCard({ challenge, isCompleted = false, attempts = 0 }: ChallengeCardProps) {
  const difficultyColors = {
    easy: 'success',
    medium: 'warning',
    hard: 'destructive'
  } as const;
  
  const difficultyLabels = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  };

  return (
    <Card className={`flex flex-col h-full hover:shadow-lg transition-shadow ${
      isCompleted ? 'border-green-300' : ''
    }`}>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant={difficultyColors[challenge.difficulty]}>
                {difficultyLabels[challenge.difficulty]}
              </Badge>
              <Badge variant="secondary">{challenge.category}</Badge>
            </div>
            <CardTitle className="text-lg mb-2">{challenge.title}</CardTitle>
            <CardDescription className="line-clamp-2">
              {challenge.description}
            </CardDescription>
          </div>
          {isCompleted && (
            <Trophy className="w-6 h-6 text-amber-500 ml-2" />
          )}
        </div>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <div className="flex items-center gap-4 text-sm text-slate-500 mb-4">
          <div className="flex items-center gap-1">
            <Code className="w-4 h-4" />
            Java
          </div>
          {attempts > 0 && (
            <div className="flex items-center gap-1">
              <span>尝试次数: {attempts}</span>
            </div>
          )}
        </div>

        <div className="mt-auto flex gap-2">
          <Link href={`/challenges/${challenge.id}/`} className="flex-1">
            <Button className="w-full" variant={isCompleted ? 'outline' : 'default'}>
              {isCompleted ? (
                <>
                  <CheckCircle className="w-4 h-4 mr-2" />
                  已完成
                </>
              ) : (
                <>
                  <Code className="w-4 h-4 mr-2" />
                  {attempts > 0 ? '继续挑战' : '开始挑战'}
                </>
              )}
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
