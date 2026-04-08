'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { BookOpen, Code, Award, TrendingUp } from 'lucide-react';

interface ProgressTrackerProps {
  coursesCompleted: number;
  challengesCompleted: number;
  certificatesEarned: number;
  totalCourses: number;
  totalChallenges: number;
}

export default function ProgressTracker({
  coursesCompleted,
  challengesCompleted,
  certificatesEarned,
  totalCourses,
  totalChallenges
}: ProgressTrackerProps) {
  const stats = [
    {
      icon: BookOpen,
      label: '已完成课程',
      value: coursesCompleted,
      total: totalCourses,
      color: 'text-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      icon: Code,
      label: '已完成挑战',
      value: challengesCompleted,
      total: totalChallenges,
      color: 'text-green-600',
      bgColor: 'bg-green-50'
    },
    {
      icon: Award,
      label: '获得证书',
      value: certificatesEarned,
      total: 3,
      color: 'text-amber-600',
      bgColor: 'bg-amber-50'
    }
  ];

  const totalProgress = Math.round(
    ((coursesCompleted + challengesCompleted) / (totalCourses + totalChallenges)) * 100
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <TrendingUp className="w-5 h-5" />
          学习进度
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="text-slate-600">总体进度</span>
            <span className="font-semibold">{totalProgress}%</span>
          </div>
          <div className="w-full bg-slate-200 rounded-full h-3">
            <div
              className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500"
              style={{ width: `${totalProgress}%` }}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          {stats.map((stat, index) => (
            <div
              key={index}
              className={`${stat.bgColor} rounded-lg p-4 text-center`}
            >
              <div className={`${stat.color} mb-2`}>
                <stat.icon className="w-8 h-8 mx-auto" />
              </div>
              <div className="text-2xl font-bold text-slate-800">
                {stat.value}
                <span className="text-sm text-slate-400 font-normal">
                  /{stat.total}
                </span>
              </div>
              <div className="text-sm text-slate-600">{stat.label}</div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
