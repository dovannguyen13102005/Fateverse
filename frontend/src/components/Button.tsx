import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface ButtonProps extends Omit<HTMLMotionProps<'button'>, 'children'> {
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  className = '',
  ...props
}: ButtonProps) => {
  const baseStyles = 'inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200';
  
  const variants = {
    primary: 'bg-accent hover:bg-accent/80 text-white',
    secondary: 'bg-purple-600 hover:bg-purple-700 text-white',
    outline: 'border-2 border-accent hover:bg-accent/10 text-accent'
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg'
  };

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className} ${
        isLoading ? 'opacity-70 cursor-not-allowed' : ''
      }`}
      disabled={isLoading}
      {...props}
    >
      {isLoading ? (
        <div className="mr-2">
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        </div>
      ) : null}
      {children}
    </motion.button>
  );
};

export default Button;