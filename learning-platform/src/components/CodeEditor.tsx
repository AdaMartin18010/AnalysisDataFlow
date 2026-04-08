'use client';

import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import { Button } from './ui/button';
import { Play, RotateCcw, Lightbulb } from 'lucide-react';

interface CodeEditorProps {
  starterCode: string;
  solution: string;
  hints: string[];
  onSubmit: (code: string) => void;
}

export default function CodeEditor({ starterCode, solution, hints, onSubmit }: CodeEditorProps) {
  const [code, setCode] = useState(starterCode);
  const [showSolution, setShowSolution] = useState(false);
  const [showHint, setShowHint] = useState<number | null>(null);

  const handleReset = () => {
    setCode(starterCode);
    setShowSolution(false);
  };

  const handleSubmit = () => {
    onSubmit(code);
  };

  return (
    <div className="flex flex-col h-full border rounded-lg overflow-hidden bg-slate-900">
      <div className="flex items-center justify-between px-4 py-2 bg-slate-800 border-b border-slate-700">
        <div className="flex items-center gap-2">
          <span className="text-sm font-medium text-slate-200">代码编辑器</span>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleReset}
            className="text-slate-400 hover:text-white"
          >
            <RotateCcw className="w-4 h-4 mr-1" />
            重置
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowSolution(!showSolution)}
            className="text-amber-400 hover:text-amber-300"
          >
            <Lightbulb className="w-4 h-4 mr-1" />
            {showSolution ? '隐藏答案' : '查看答案'}
          </Button>
        </div>
      </div>

      <div className="flex-1 relative">
        <Editor
          height="100%"
          language="java"
          theme="vs-dark"
          value={showSolution ? solution : code}
          onChange={(value) => !showSolution && setCode(value || '')}
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            roundedSelection: false,
            scrollBeyondLastLine: false,
            readOnly: showSolution,
            automaticLayout: true,
          }}
        />
      </div>

      {hints.length > 0 && (
        <div className="px-4 py-3 bg-slate-800 border-t border-slate-700">
          <div className="flex items-center gap-2 mb-2">
            <Lightbulb className="w-4 h-4 text-amber-400" />
            <span className="text-sm font-medium text-slate-200">提示</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {hints.map((hint, index) => (
              <button
                key={index}
                onClick={() => setShowHint(showHint === index ? null : index)}
                className={`px-3 py-1 text-xs rounded-full transition-colors ${
                  showHint === index
                    ? 'bg-amber-500 text-white'
                    : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
                }`}
              >
                提示 {index + 1}
              </button>
            ))}
          </div>
          {showHint !== null && (
            <div className="mt-2 p-3 bg-slate-700 rounded text-sm text-slate-200">
              {hints[showHint]}
            </div>
          )}
        </div>
      )}

      <div className="flex items-center justify-between px-4 py-3 bg-slate-800 border-t border-slate-700">
        <span className="text-xs text-slate-400">
          {showSolution ? '查看模式中 - 编辑器只读' : '编辑模式'}
        </span>
        <Button onClick={handleSubmit} disabled={showSolution}>
          <Play className="w-4 h-4 mr-2" />
          运行代码
        </Button>
      </div>
    </div>
  );
}
