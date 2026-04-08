'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  BookOpen, 
  Code, 
  Award, 
  Zap,
  ArrowRight
} from 'lucide-react';
import { useProgress } from '@/hooks/useProgress';
import { courses } from '@/lib/courses';
import { challenges } from '@/lib/challenges';
import ProgressTracker from '@/components/ProgressTracker';

export default function Home() {
  const { overallProgress } = useProgress();
  
  const progress = overallProgress();

  const features = [
    {
      icon: BookOpen,
      title: '系统课程',
      description: '从入门到精通的完整Flink学习路径，3门课程，17个课时'
    },
    {
      icon: Code,
      title: '编程挑战',
      description: '20个实战编程挑战，从基础API到高级特性，循序渐进'
    },
    {
      icon: Award,
      title: '认证证书',
      description: '完成课程获得PDF证书，支持下载和分享'
    },
    {
      icon: Zap,
      title: '即时反馈',
      description: '在线代码编辑器和自动评测，快速验证学习成果'
    }
  ];

  const stats = [
    { label: '课程数量', value: '3' },
    { label: '编程挑战', value: '20' },
    { label: '学习时长', value: '20+' },
    { label: '难度级别', value: '3' }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <Badge className="bg-blue-500 text-white mb-4 text-sm">
                免费在线学习平台
              </Badge>
              <h1 className="text-4xl lg:text-6xl font-bold mb-6 leading-tight">
                掌握 Apache Flink
                <br />
                <span className="text-blue-300">流处理技术</span>
              </h1>
              <p className="text-xl text-blue-100 mb-8 leading-relaxed">
                从零开始学习流处理，系统化的课程体系、实战编程挑战、
                即时反馈机制，助你快速掌握Flink核心技术。
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/courses/">
                  <Button size="lg" className="bg-white text-blue-700 hover:bg-blue-50">
                    开始学习
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </Link>
                <Link href="/challenges/">
                  <Button size="lg" variant="outline" className="border-white text-white hover:bg-blue-600">
                    <Code className="w-4 h-4 mr-2" />
                    编程挑战
                  </Button>
                </Link>
              </div>
            </div>
            <div className="hidden lg:block">
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
                <div className="grid grid-cols-2 gap-4">
                  {stats.map((stat, index) => (
                    <div key={index} className="bg-white/10 rounded-lg p-4 text-center">
                      <div className="text-3xl font-bold mb-1">{stat.value}</div>
                      <div className="text-blue-200 text-sm">{stat.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">平台特色</h2>
            <p className="text-slate-600 max-w-2xl mx-auto">
              精心设计的课程体系和学习工具，让流处理技术学习更加高效
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index} className="text-center hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                    <feature.icon className="w-6 h-6 text-blue-600" />
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-slate-600 text-sm">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Progress Section */}
      {(progress.courses > 0 || progress.challenges > 0) && (
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">我的学习进度</h2>
            <ProgressTracker
              coursesCompleted={progress.courses}
              challengesCompleted={progress.challenges}
              certificatesEarned={progress.certificates}
              totalCourses={courses.reduce((acc, c) => acc + c.lessons, 0)}
              totalChallenges={challenges.length}
            />
          </div>
        </section>
      )}

      {/* Courses Preview */}
      <section className="py-16 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-2">精品课程</h2>
              <p className="text-slate-600">由浅入深，系统学习Flink流处理技术</p>
            </div>
            <Link href="/courses/">
              <Button variant="outline">
                查看全部
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
          </div>
          <div className="grid md:grid-cols-3 gap-6">
            {courses.map((course) => (
              <Card key={course.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <Badge variant={course.level === 'beginner' ? 'success' : course.level === 'intermediate' ? 'warning' : 'destructive'}>
                    {course.level === 'beginner' ? '初级' : course.level === 'intermediate' ? '中级' : '高级'}
                  </Badge>
                  <CardTitle className="mt-2">{course.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-slate-600 text-sm mb-4">{course.description}</p>
                  <div className="flex items-center justify-between text-sm text-slate-500">
                    <span>{course.lessons} 课时</span>
                    <span>{course.duration}</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-slate-900 to-slate-800 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl lg:text-4xl font-bold mb-6">
            准备好开始学习了吗？
          </h2>
          <p className="text-slate-300 text-lg mb-8">
            立即加入，免费获取完整课程内容，完成学习获得认证证书
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/courses/">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                <BookOpen className="w-4 h-4 mr-2" />
                浏览课程
              </Button>
            </Link>
            <Link href="/challenges/">
              <Button size="lg" variant="outline" className="border-slate-500 text-slate-300 hover:bg-slate-700">
                <Code className="w-4 h-4 mr-2" />
                开始挑战
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-950 text-slate-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <BookOpen className="w-6 h-6 text-blue-500" />
                <span className="font-bold text-lg text-white">Flink学习平台</span>
              </div>
              <p className="text-sm">
                致力于流处理技术的普及和教育，为开发者提供优质的Flink学习资源。
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">学习资源</h4>
              <ul className="space-y-2 text-sm">
                <li><Link href="/courses/" className="hover:text-white transition-colors">全部课程</Link></li>
                <li><Link href="/challenges/" className="hover:text-white transition-colors">编程挑战</Link></li>
                <li><Link href="/certificates/" className="hover:text-white transition-colors">我的证书</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">技术栈</h4>
              <ul className="space-y-2 text-sm">
                <li>Next.js 14</li>
                <li>Tailwind CSS</li>
                <li>Monaco Editor</li>
                <li>GitHub Pages</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">关于</h4>
              <p className="text-sm">
                本学习平台使用静态网站技术构建，数据保存在本地浏览器中。
              </p>
            </div>
          </div>
          <div className="border-t border-slate-800 mt-8 pt-8 text-center text-sm">
            <p>&copy; 2026 Flink学习平台. 基于 MIT 协议开源.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
