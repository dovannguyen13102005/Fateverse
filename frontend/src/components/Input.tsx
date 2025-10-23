import { forwardRef } from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface InputProps extends Omit<HTMLMotionProps<'input'>, 'whileFocus'> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, icon, className = '', ...props }, ref) => {
    return (
      <div className="mb-4">
        {label && (
          <label className="block text-white/80 mb-2 text-sm">
            {label}
          </label>
        )}
        <div className="relative">
          <motion.input
            whileFocus={{ scale: 1.01 }}
            ref={ref}
            className={`
              w-full px-4 py-3 bg-white/5 border rounded-lg
              focus:outline-none focus:ring-2 focus:ring-accent
              text-white placeholder-white/50
              ${error ? 'border-red-500' : 'border-white/20'}
              ${icon ? 'pl-12' : ''}
              ${className}
            `}
            {...props}
          />
          {icon && (
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white/50">
              {icon}
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1 text-sm text-red-500">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;