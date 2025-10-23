import { motion, HTMLMotionProps } from 'framer-motion';
import type { ReactNode } from 'react';

interface GlowButtonProps extends Omit<HTMLMotionProps<'button'>, 'whileHover' | 'whileTap'> {
  variant?: 'primary' | 'secondary' | 'accent';
  children: ReactNode;
}

const GlowButton = ({ 
  children, 
  variant = 'primary',
  className = '',
  ...props 
}: GlowButtonProps) => {
  const baseClasses = 'px-6 py-3 rounded-full font-semibold transition-all duration-300 hover:shadow-lg active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed';
  const variantClasses = {
    primary: 'bg-gradient-to-r from-primary to-accent text-white hover:shadow-primary/50',
    secondary: 'bg-gradient-to-r from-secondary to-accent text-bg hover:shadow-secondary/50',
    accent: 'bg-gradient-to-r from-accent to-secondary text-bg hover:shadow-accent/50',
  };

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {children}
    </motion.button>
  );
};

export default GlowButton;