import { courses, getCourseById } from '@/lib/courses';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import CourseClient from './CourseClient';

export function generateStaticParams() {
  return courses.map((course) => ({
    id: course.id,
  }));
}

export default function CoursePage({ params }: { params: { id: string } }) {
  const course = getCourseById(params.id);

  if (!course) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-4">课程未找到</h1>
          <Link href="/courses/">
            <Button>
              <ArrowLeft className="w-4 h-4 mr-2" />
              返回课程列表
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return <CourseClient course={course} />;
}
