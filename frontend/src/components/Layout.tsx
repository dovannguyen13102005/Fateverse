import { motion } from 'framer-motion';
import { ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
  title: string;
  subtitle?: string;
}

const Layout = ({ children, title, subtitle }: LayoutProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="container mx-auto px-4 py-8"
    >
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-cinzel text-accent mb-4">
          {title}
        </h1>
        {subtitle && (
          <p className="text-xl text-white/80">{subtitle}</p>
        )}
      </div>
      {children}
    </motion.div>
  );
};

export default Layout;