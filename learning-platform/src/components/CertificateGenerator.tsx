'use client';

import React, { useRef, useState } from 'react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import { Button } from './ui/button';
import { Download, Award } from 'lucide-react';
import { Badge } from './ui/badge';

interface CertificateGeneratorProps {
  courseName: string;
  courseId: string;
  completionDate: string;
  studentName?: string;
}

export default function CertificateGenerator({
  courseName,
  courseId,
  completionDate,
  studentName = '学员'
}: CertificateGeneratorProps) {
  const certificateRef = useRef<HTMLDivElement>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const generatePDF = async () => {
    if (!certificateRef.current) return;
    
    setIsGenerating(true);
    try {
      const canvas = await html2canvas(certificateRef.current, {
        scale: 2,
        useCORS: true,
        backgroundColor: '#ffffff'
      });
      
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('landscape', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
      pdf.save(`证书-${courseId}-${Date.now()}.pdf`);
    } catch (error) {
      console.error('PDF generation error:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const certificateId = `CERT-${courseId.toUpperCase()}-${new Date(completionDate).getTime()}`;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <Badge variant="success" className="text-base px-4 py-2">
          <Award className="w-5 h-5 mr-2" />
          课程已完成！
        </Badge>
        <Button 
          onClick={generatePDF} 
          disabled={isGenerating}
          className="ml-auto"
        >
          <Download className="w-4 h-4 mr-2" />
          {isGenerating ? '生成中...' : '下载证书'}
        </Button>
      </div>

      {/* Certificate Preview */}
      <div 
        ref={certificateRef}
        className="bg-gradient-to-br from-amber-50 to-orange-50 border-4 border-amber-400 rounded-lg p-8 text-center"
        style={{ aspectRatio: '1.414/1', maxWidth: '800px', margin: '0 auto' }}
      >
        <div className="h-full flex flex-col justify-between">
          <div>
            <div className="text-amber-600 text-lg font-semibold tracking-widest uppercase mb-2">
              Apache Flink 学习平台
            </div>
            <div className="w-32 h-1 bg-amber-400 mx-auto mb-6" />
            <h1 className="text-4xl font-bold text-slate-800 mb-4">
              结 业 证 书
            </h1>
            <p className="text-slate-600 text-lg">
              兹证明
            </p>
          </div>

          <div>
            <p className="text-3xl font-bold text-slate-900 my-6">
              {studentName}
            </p>
            <p className="text-slate-600 text-lg">
              已完成以下课程的学习
            </p>
            <p className="text-2xl font-semibold text-amber-700 my-4">
              《{courseName}》
            </p>
          </div>

          <div className="flex justify-between items-end text-sm text-slate-500">
            <div className="text-left">
              <p>证书编号:</p>
              <p className="font-mono">{certificateId}</p>
            </div>
            <div className="text-center">
              <div className="w-24 h-24 border-4 border-amber-400 rounded-full flex items-center justify-center mx-auto mb-2">
                <Award className="w-12 h-12 text-amber-500" />
              </div>
            </div>
            <div className="text-right">
              <p>完成日期:</p>
              <p>{new Date(completionDate).toLocaleDateString('zh-CN')}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
