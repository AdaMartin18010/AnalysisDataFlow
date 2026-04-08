'use client';

import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Clock, BookOpen, Award } from 'lucide-react';
import type { Course } from '@/lib/courses';

interface CourseCardProps {
  course: Course;
  completedLessons?: number;
  hasCertificate?: boolean;
}

export default function CourseCard({ course, completedLessons = 0, hasCertificate = false }: CourseCardProps) {
  const progress = Math.round((completedLessons / course.lessons) * 100);
  
  const levelColors = {
    beginner: 'success',
    intermediate: 'warning',
    advanced: 'destructive'
  } as const;
  
  const levelLabels = {
    beginner: '初级',
    intermediate: '中级',
    advanced: '高级'
  };

  return (
    <Card className="flex flex-col h-full hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <Badge variant={levelColors[course.level]} className="mb-2">
              {levelLabels[course.level]}
            </Badge>
            <CardTitle className="text-xl mb-2">{course.title}</CardTitle>
            <CardDescription>{course.description}</CardDescription>
          </div>
          {hasCertificate && (
            <Award className="w-6 h-6 text-amber-500 ml-2" />
          )}
        </div>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col">
        <div className="flex flex-wrap gap-2 mb-4">
          {course.tags.map((tag) => (
            <span key={tag} className="text-xs px-2 py-1 bg-slate-100 rounded text-slate-600">
              {tag}
            </span>
          ))}
        </div>
        
        <div className="flex items-center gap-4 text-sm text-slate-500 mb-4">
          <div className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            {course.duration}
          </div>
          <div className="flex items-center gap-1">
            <BookOpen className="w-4 h-4" />
            {course.lessons} 课时
          </div>
        </div>

        {completedLessons > 0 && (
          <div className="mb-4">
            <div className="flex justify-between text-sm mb-1">
              <span className="text-slate-600">学习进度</span>
              <span className="font-medium">{progress}%</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        <div className="mt-auto">
          <Link href={`/courses/${course.id}/`}>
            <Button className="w-full">
              {completedLessons > 0 ? '继续学习' : '开始学习'}
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
