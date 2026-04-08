'use client';

import React from 'react';
import Link from 'next/link';
import { BookOpen, Code, Award, Home } from 'lucide-react';

export default function Navbar() {
  const navItems = [
    { href: '/', label: '首页', icon: Home },
    { href: '/courses/', label: '课程', icon: BookOpen },
    { href: '/challenges/', label: '挑战', icon: Code },
    { href: '/certificates/', label: '证书', icon: Award },
  ];

  return (
    <nav className="border-b bg-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <BookOpen className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-xl text-slate-900">Flink学习平台</span>
            </Link>
          </div>
          
          <div className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors"
              >
                <item.icon className="w-4 h-4" />
                <span className="hidden sm:inline">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
}
