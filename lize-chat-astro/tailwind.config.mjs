/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'cyan': '#00AEEF',      // 主色（Cyan）
        'deep-blue': '#0054A6',  // 深色（Deep Blue）
        'text-dark': '#1F2937',  // 文字深灰色
        'bg-light': '#F9FAFB',   // 极简浅灰背景
      },
      fontFamily: {
        'serif': ['"Noto Serif SC"', '"Source Han Serif SC"', 'serif'], // 衬线体（标题）
        'sans': ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'], // 无衬线体（正文）
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
