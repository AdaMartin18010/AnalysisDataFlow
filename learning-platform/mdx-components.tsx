import type { MDXComponents } from 'mdx/types'
import Image from 'next/image'

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h1: ({ children }) => <h1 className="text-3xl font-bold text-slate-900 mb-6">{children}</h1>,
    h2: ({ children }) => <h2 className="text-2xl font-semibold text-slate-800 mt-8 mb-4">{children}</h2>,
    h3: ({ children }) => <h3 className="text-xl font-semibold text-slate-800 mt-6 mb-3">{children}</h3>,
    p: ({ children }) => <p className="text-slate-600 leading-relaxed mb-4">{children}</p>,
    code: ({ children }) => (
      <code className="bg-slate-100 text-slate-800 px-2 py-1 rounded text-sm font-mono">{children}</code>
    ),
    pre: ({ children }) => (
      <pre className="bg-slate-900 text-slate-100 p-4 rounded-lg overflow-x-auto mb-4">{children}</pre>
    ),
    ul: ({ children }) => <ul className="list-disc list-inside text-slate-600 mb-4 space-y-1">{children}</ul>,
    ol: ({ children }) => <ol className="list-decimal list-inside text-slate-600 mb-4 space-y-1">{children}</ol>,
    li: ({ children }) => <li className="ml-4">{children}</li>,
    blockquote: ({ children }) => (
      <blockquote className="border-l-4 border-blue-500 pl-4 italic text-slate-600 mb-4">{children}</blockquote>
    ),
    img: (props) => <Image {...props} alt={props.alt || ''} className="rounded-lg my-4" />,
    ...components,
  }
}
