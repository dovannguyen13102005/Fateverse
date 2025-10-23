import { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface ResultCardProps {
  title: string;
  children: ReactNode;
  emoji?: string;
  className?: string;
  onShare?: () => void;
}

const ResultCard = ({
  title,
  children,
  emoji,
  className = '',
  onShare,
}: ResultCardProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className={`card relative overflow-hidden ${className}`}
    >
      {/* Background Stars */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-4 right-4 text-white/10 text-6xl animate-float">
          ✨
        </div>
        <div className="absolute bottom-4 left-4 text-white/10 text-6xl animate-float" style={{ animationDelay: '1s' }}>
          ⭐
        </div>
      </div>

      {/* Content */}
      <div className="relative">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-2xl font-display text-accent">
            {emoji && <span className="mr-2">{emoji}</span>}
            {title}
          </h3>
          {onShare && (
            <button
              onClick={onShare}
              className="text-white/50 hover:text-white transition-colors duration-200"
              aria-label="Share result"
            >
              🌠
            </button>
          )}
        </div>
        <div className="space-y-4">
          {children}
        </div>
      </div>
    </motion.div>
  );
};

export default ResultCard;