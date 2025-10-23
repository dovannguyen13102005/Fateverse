import { ReactNode } from 'react';
import { motion } from 'framer-motion';
import Navigation from './Navigation';

interface LayoutProps {
  children: ReactNode;
  title?: string;
}

const Layout = ({ children, title }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-gradient-cosmic">
      <Navigation />
      <main className="container mx-auto px-4 pt-20 pb-12">
        {title && (
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-display text-center mb-12 text-accent"
          >
            {title}
          </motion.h1>
        )}
        {children}
      </main>
    </div>
  );
};

export default Layout;