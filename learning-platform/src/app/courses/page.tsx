'use client';

import { courses } from '@/lib/courses';
import CourseCard from '@/components/CourseCard';
import { useProgress } from '@/hooks/useProgress';

export default function CoursesPage() {
  const { getCourseProgressCount, checkCertificate } = useProgress();

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">全部课程</h1>
        <p className="text-slate-600">
          系统化的Flink学习路径，从入门到精通，掌握流处理核心技术
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <CourseCard
            key={course.id}
            course={course}
            completedLessons={getCourseProgressCount(course.id)}
            hasCertificate={checkCertificate(course.id)}
          />
        ))}
      </div>

      <div className="mt-12 bg-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-slate-900 mb-2">学习建议</h2>
        <ul className="space-y-2 text-slate-600">
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold">1.</span>
            <span>建议按顺序学习，从《Flink基础入门》开始</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold">2.</span>
            <span>每个课时完成后可以进行对应的编程挑战</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold">3.</span>
            <span>完成全部课程可获得结业证书</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
