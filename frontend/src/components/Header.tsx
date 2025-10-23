import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';

const Header = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home' },
    { path: '/numerology', label: 'Numerology' },
    { path: '/zodiac', label: 'Zodiac' },
    { path: '/love', label: 'Love Match' },
    { path: '/tarot', label: 'Tarot' },
    { path: '/daily', label: 'Daily Fortune' },
    { path: '/history', label: 'History' },
    { path: '/settings', label: 'Settings' },
  ];

  return (
    <header className="bg-black/20 backdrop-blur-lg">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-2xl font-cinzel text-accent">
            FateVerse 🔮
          </Link>
          
          <div className="hidden md:flex space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`relative ${
                  location.pathname === item.path
                    ? 'text-accent'
                    : 'text-white/80 hover:text-accent'
                }`}
              >
                {location.pathname === item.path && (
                  <motion.div
                    layoutId="underline"
                    className="absolute left-0 right-0 h-0.5 bg-accent bottom-0"
                  />
                )}
                {item.label}
              </Link>
            ))}
          </div>
          
          <button className="md:hidden">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
        </div>
      </nav>
    </header>
  );
};

export default Header;