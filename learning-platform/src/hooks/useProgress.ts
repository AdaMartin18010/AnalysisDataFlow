'use client';

import { useState, useEffect, useCallback } from 'react';
import { 
  getProgress, 
  markLessonComplete, 
  isLessonCompleted,
  getCourseProgress,
  saveChallengeProgress,
  addCertificate,
  hasCertificate,
  getOverallProgress
} from '@/lib/progress';

export function useProgress() {
  const [mounted, setMounted] = useState(false);
  const [progress, setProgress] = useState(getProgress());

  useEffect(() => {
    setMounted(true);
    setProgress(getProgress());
  }, []);

  const completeLesson = useCallback((courseId: string, lessonId: string) => {
    markLessonComplete(courseId, lessonId);
    setProgress(getProgress());
  }, []);

  const checkLessonComplete = useCallback((courseId: string, lessonId: string) => {
    return isLessonCompleted(courseId, lessonId);
  }, []);

  const getCourseProgressCount = useCallback((courseId: string) => {
    return getCourseProgress(courseId);
  }, []);

  const saveChallenge = useCallback((challengeId: string, code: string, completed: boolean) => {
    saveChallengeProgress(challengeId, code, completed);
    setProgress(getProgress());
  }, []);

  const issueCertificate = useCallback((courseId: string) => {
    addCertificate(courseId);
    setProgress(getProgress());
  }, []);

  const checkCertificate = useCallback((courseId: string) => {
    return hasCertificate(courseId);
  }, []);

  const overallProgress = useCallback(() => {
    return getOverallProgress();
  }, []);

  if (!mounted) {
    return {
      progress: { courses: [], challenges: [], certificates: [] },
      completeLesson: () => {},
      checkLessonComplete: () => false,
      getCourseProgressCount: () => 0,
      saveChallenge: () => {},
      issueCertificate: () => {},
      checkCertificate: () => false,
      overallProgress: () => ({ courses: 0, challenges: 0, certificates: 0 })
    };
  }

  return {
    progress,
    completeLesson,
    checkLessonComplete,
    getCourseProgressCount,
    saveChallenge,
    issueCertificate,
    checkCertificate,
    overallProgress
  };
}
