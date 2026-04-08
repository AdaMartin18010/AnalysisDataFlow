'use client';

import React, { useState } from 'react';
import { CheckCircle, Circle, Play, FileText, HelpCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import type { Course } from '@/lib/courses';
import Mermaid from './Mermaid';

interface CoursePlayerProps {
  course: Course;
  currentLessonId: string;
  completedLessons: string[];
  onLessonComplete: (lessonId: string) => void;
  onLessonSelect: (lessonId: string) => void;
}

const lessonTypeIcons = {
  video: Play,
  reading: FileText,
  quiz: HelpCircle,
  practice: Play
};

export default function CoursePlayer({
  course,
  currentLessonId,
  completedLessons,
  onLessonComplete,
  onLessonSelect
}: CoursePlayerProps) {
  const [activeTab, setActiveTab] = useState<'content' | 'notes'>('content');

  const currentLesson = course.modules
    .flatMap(m => m.lessons)
    .find(l => l.id === currentLessonId);

  const totalLessons = course.modules.reduce((acc, m) => acc + m.lessons.length, 0);
  const progress = Math.round((completedLessons.length / totalLessons) * 100);

  return (
    <div className="flex flex-col lg:flex-row gap-6">
      {/* Main Content */}
      <div className="flex-1">
        <div className="bg-slate-900 rounded-lg overflow-hidden mb-4">
          <div className="aspect-video flex items-center justify-center bg-slate-800">
            {currentLesson?.type === 'video' ? (
              <div className="text-center">
                <Play className="w-16 h-16 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-400">视频播放器占位</p>
                <p className="text-slate-500 text-sm mt-2">
                  实际部署时请替换为真实视频内容
                </p>
              </div>
            ) : (
              <FileText className="w-16 h-16 text-slate-400" />
            )}
          </div>
        </div>

        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold">{currentLesson?.title}</h1>
          <div className="flex items-center gap-2">
            {!completedLessons.includes(currentLessonId) && (
              <Button onClick={() => onLessonComplete(currentLessonId)}>
                <CheckCircle className="w-4 h-4 mr-2" />
                标记完成
              </Button>
            )}
            {completedLessons.includes(currentLessonId) && (
              <Badge variant="success">
                <CheckCircle className="w-3 h-3 mr-1" />
                已完成
              </Badge>
            )}
          </div>
        </div>

        <div className="flex gap-4 border-b mb-4">
          <button
            onClick={() => setActiveTab('content')}
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'content'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            课程内容
          </button>
          <button
            onClick={() => setActiveTab('notes')}
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'notes'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            我的笔记
          </button>
        </div>

        {activeTab === 'content' && (
          <div className="prose max-w-none">
            <h2>课程讲解</h2>
            <p>
              这里是课程内容的详细讲解。在实际部署时，这部分可以替换为真实的视频转录文本或文档内容。
            </p>
            
            <Mermaid chart={`
              graph TD
                A[数据源] --> B[DataStream]
                B --> C[Transformation]
                C --> D[Sink]
                
                style A fill:#e1f5fe
                style B fill:#fff3e0
                style C fill:#e8f5e9
                style D fill:#fce4ec
            `} />

            <h3>核心概念</h3>
            <ul>
              <li>DataStream API 基础</li>
              <li>Transformation 操作</li>
              <li>Execution Environment</li>
              <li>并行度配置</li>
            </ul>
          </div>
        )}

        {activeTab === 'notes' && (
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <p className="text-slate-600 italic">
              在此添加您的学习笔记...（功能开发中，数据将保存在本地）
            </p>
          </div>
        )}
      </div>

      {/* Sidebar */}
      <div className="w-full lg:w-80 shrink-0">
        <div className="bg-white rounded-lg border p-4">
          <div className="mb-4">
            <h3 className="font-semibold mb-2">{course.title}</h3>
            <div className="flex items-center gap-2 text-sm text-slate-500 mb-2">
              <span>{completedLessons.length} / {totalLessons} 课时</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          <div className="space-y-4">
            {course.modules.map((module, moduleIndex) => (
              <div key={moduleIndex}>
                <h4 className="font-medium text-sm text-slate-700 mb-2">
                  {module.title}
                </h4>
                <div className="space-y-1">
                  {module.lessons.map((lesson) => {
                    const isCompleted = completedLessons.includes(lesson.id);
                    const isActive = lesson.id === currentLessonId;
                    const Icon = lessonTypeIcons[lesson.type];

                    return (
                      <button
                        key={lesson.id}
                        onClick={() => onLessonSelect(lesson.id)}
                        className={`w-full flex items-center gap-3 p-2 rounded text-left transition-colors ${
                          isActive
                            ? 'bg-blue-50 text-blue-700'
                            : 'hover:bg-slate-50'
                        }`}
                      >
                        {isCompleted ? (
                          <CheckCircle className="w-4 h-4 text-green-500 shrink-0" />
                        ) : (
                          <Circle className="w-4 h-4 text-slate-300 shrink-0" />
                        )}
                        <Icon className="w-4 h-4 text-slate-400 shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className={`text-sm truncate ${
                            isActive ? 'font-medium' : ''
                          }`}>
                            {lesson.title}
                          </p>
                          <p className="text-xs text-slate-400">{lesson.duration}</p>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
