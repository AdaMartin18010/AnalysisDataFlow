'use client';

import { courses } from '@/lib/courses';
import { useProgress } from '@/hooks/useProgress';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Award, BookOpen, CheckCircle } from 'lucide-react';
import Link from 'next/link';
import CertificateGenerator from '@/components/CertificateGenerator';

export default function CertificatesPage() {
  const { checkCertificate, getCourseProgressCount, progress } = useProgress();

  const completedCourses = courses.filter(course => {
    const completedLessons = getCourseProgressCount(course.id);
    return completedLessons >= course.lessons;
  });

  const inProgressCourses = courses.filter(course => {
    const completedLessons = getCourseProgressCount(course.id);
    return completedLessons > 0 && completedLessons < course.lessons;
  });

  const notStartedCourses = courses.filter(course => {
    const completedLessons = getCourseProgressCount(course.id);
    return completedLessons === 0;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Award className="w-8 h-8 text-amber-500" />
          <h1 className="text-3xl font-bold text-slate-900">我的证书</h1>
        </div>
        <p className="text-slate-600">
          完成课程学习并获得认证证书，证明你的Flink技术能力
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-amber-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-amber-600">
            {progress.certificates.length}
          </div>
          <div className="text-sm text-slate-600">已获得证书</div>
        </div>
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">
            {completedCourses.length}
          </div>
          <div className="text-sm text-slate-600">已完成课程</div>
        </div>
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">
            {inProgressCourses.length}
          </div>
          <div className="text-sm text-slate-600">学习中</div>
        </div>
        <div className="bg-slate-50 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-slate-600">
            {notStartedCourses.length}
          </div>
          <div className="text-sm text-slate-600">未开始</div>
        </div>
      </div>

      {/* Earned Certificates */}
      {progress.certificates.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-slate-900 mb-4">已获得的证书</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {progress.certificates.map(certId => {
              const course = courses.find(c => c.id === certId);
              if (!course) return null;
              
              return (
                <Card key={certId} className="border-amber-200 bg-gradient-to-br from-amber-50 to-orange-50">
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <Award className="w-6 h-6 text-amber-500" />
                      <Badge variant="success">已认证</Badge>
                    </div>
                    <CardTitle className="text-lg mt-2">{course.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-slate-600 mb-4">
                      完成日期: {new Date().toLocaleDateString('zh-CN')}
                    </p>
                    <CertificateGenerator
                      courseName={course.title}
                      courseId={course.id}
                      completionDate={new Date().toISOString()}
                    />
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      )}

      {/* Available Certificates */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold text-slate-900 mb-4">可获取的证书</h2>
        {completedCourses.filter(c => !checkCertificate(c.id)).length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {completedCourses
              .filter(c => !checkCertificate(c.id))
              .map(course => (
                <Card key={course.id} className="border-green-200">
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <CheckCircle className="w-6 h-6 text-green-500" />
                      <Badge variant="success">课程已完成</Badge>
                    </div>
                    <CardTitle className="text-lg mt-2">{course.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-slate-600 mb-4">
                      你已完成全部课程内容，可以获取证书了！
                    </p>
                    <CertificateGenerator
                      courseName={course.title}
                      courseId={course.id}
                      completionDate={new Date().toISOString()}
                    />
                  </CardContent>
                </Card>
              ))}
          </div>
        ) : completedCourses.length === 0 ? (
          <div className="bg-slate-50 rounded-lg p-8 text-center">
            <BookOpen className="w-12 h-12 text-slate-300 mx-auto mb-4" />
            <p className="text-slate-500 mb-4">还没有完成任何课程</p>
            <Link href="/courses/">
              <Button>开始学习</Button>
            </Link>
          </div>
        ) : (
          <div className="bg-green-50 rounded-lg p-6 text-center">
            <CheckCircle className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <p className="text-green-800">所有已完成的课程证书都已领取！</p>
          </div>
        )}
      </div>

      {/* In Progress */}
      {inProgressCourses.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-slate-900 mb-4">学习中的课程</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {inProgressCourses.map(course => {
              const completed = getCourseProgressCount(course.id);
              const progressPct = Math.round((completed / course.lessons) * 100);
              
              return (
                <Card key={course.id}>
                  <CardHeader>
                    <CardTitle className="text-lg">{course.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-slate-600">学习进度</span>
                        <span className="font-medium">{progressPct}%</span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all"
                          style={{ width: `${progressPct}%` }}
                        />
                      </div>
                      <p className="text-sm text-slate-500 mt-1">
                        已完成 {completed} / {course.lessons} 课时
                      </p>
                    </div>
                    <Link href={`/courses/${course.id}/`}>
                      <Button variant="outline" className="w-full">
                        继续学习
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
