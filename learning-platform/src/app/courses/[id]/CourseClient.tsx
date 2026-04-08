'use client';

import { useState } from 'react';
import { Course } from '@/lib/courses';
import CoursePlayer from '@/components/CoursePlayer';
import CertificateGenerator from '@/components/CertificateGenerator';
import { ArrowLeft, Award } from 'lucide-react';
import Link from 'next/link';
import { useProgress } from '@/hooks/useProgress';

interface CourseClientProps {
  course: Course;
}

export default function CourseClient({ course }: CourseClientProps) {
  const { 
    checkLessonComplete, 
    completeLesson, 
    getCourseProgressCount,
    checkCertificate
  } = useProgress();

  const allLessons = course.modules.flatMap(m => m.lessons);
  const [currentLessonId, setCurrentLessonId] = useState(allLessons[0]?.id || '');

  const completedCount = getCourseProgressCount(course.id);
  const allCompleted = completedCount >= allLessons.length;
  const hasCert = checkCertificate(course.id);

  const handleLessonComplete = (lessonId: string) => {
    completeLesson(course.id, lessonId);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link href="/courses/" className="text-slate-500 hover:text-slate-700 flex items-center gap-1 mb-4">
          <ArrowLeft className="w-4 h-4" />
          返回课程列表
        </Link>
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold text-slate-900">{course.title}</h1>
          {hasCert && (
            <div className="flex items-center gap-2 text-amber-600">
              <Award className="w-6 h-6" />
              <span className="font-medium">已获得证书</span>
            </div>
          )}
        </div>
      </div>

      {allCompleted && !hasCert && (
        <div className="mb-8">
          <CertificateGenerator
            courseName={course.title}
            courseId={course.id}
            completionDate={new Date().toISOString()}
          />
        </div>
      )}

      <CoursePlayer
        course={course}
        currentLessonId={currentLessonId}
        completedLessons={allLessons.filter(l => checkLessonComplete(course.id, l.id)).map(l => l.id)}
        onLessonComplete={handleLessonComplete}
        onLessonSelect={setCurrentLessonId}
      />
    </div>
  );
}
