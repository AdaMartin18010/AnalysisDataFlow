import { challenges, getChallengeById } from '@/lib/challenges';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import ChallengeClient from './ChallengeClient';

export function generateStaticParams() {
  return challenges.map((challenge) => ({
    id: challenge.id,
  }));
}

export default function ChallengePage({ params }: { params: { id: string } }) {
  const challenge = getChallengeById(params.id);

  if (!challenge) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-slate-900 mb-4">挑战未找到</h1>
          <Link href="/challenges/">
            <Button>
              <ArrowLeft className="w-4 h-4 mr-2" />
              返回挑战列表
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return <ChallengeClient challenge={challenge} />;
}
