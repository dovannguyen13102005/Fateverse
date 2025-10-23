import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '../../contexts/AuthContext';

interface NavigationLink {
  path: string;
  label: string;
}

const navigationLinks: NavigationLink[] = [
  { path: '/', label: 'Home' },
  { path: '/numerology', label: 'Thần Số Học' },
  { path: '/zodiac', label: 'Cung Hoàng Đạo' },
  { path: '/love', label: 'Bói Tình Duyên' },
  { path: '/tarot', label: 'Tarot' },
  { path: '/daily', label: 'Lá Số Hôm Nay' },
  { path: '/history', label: 'Lịch Sử' },
  { path: '/settings', label: 'Cài Đặt' },
];

const Navigation = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const location = useLocation();
  const { user, logout } = useAuth();

  const toggleMenu = () => setIsOpen(!isOpen);
  const toggleUserMenu = () => setUserMenuOpen(!userMenuOpen);

  const handleLogout = () => {
    logout();
    setUserMenuOpen(false);
  };

  return (
    <nav className="fixed top-0 left-0 right-0 bg-bg/80 backdrop-blur-lg z-50 shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl">🔮</span>
            <span className="font-display text-xl text-accent">FateVerse</span>
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex md:items-center md:space-x-8">
            {navigationLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={'nav-link ' + (location.pathname === link.path ? 'active' : '')}
              >
                {link.label}
              </Link>
            ))}
            
            {/* User Menu */}
            <div className="relative">
              <button
                onClick={toggleUserMenu}
                className="flex items-center space-x-2 text-white/70 hover:text-white transition-colors duration-200"
              >
                {user?.picture ? (
                  <img
                    src={user.picture}
                    alt={user.name}
                    className="w-8 h-8 rounded-full"
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center">
                    <span className="text-accent text-sm">
                      {user?.name?.charAt(0) || 'U'}
                    </span>
                  </div>
                )}
                <span className="hidden lg:block">{user?.name}</span>
                <span className="text-xs">▼</span>
              </button>

              <AnimatePresence>
                {userMenuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -10 }}
                    className="absolute right-0 top-full mt-2 w-48 bg-bg/95 backdrop-blur-lg rounded-lg border border-white/20 shadow-lg"
                  >
                    <div className="py-2">
                      <Link
                        to="/settings"
                        onClick={() => setUserMenuOpen(false)}
                        className="block px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 transition-colors duration-200"
                      >
                        ⚙️ Cài Đặt
                      </Link>
                      <Link
                        to="/history"
                        onClick={() => setUserMenuOpen(false)}
                        className="block px-4 py-2 text-white/70 hover:text-white hover:bg-white/10 transition-colors duration-200"
                      >
                        📜 Lịch Sử
                      </Link>
                      <hr className="border-white/20 my-2" />
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-red-300 hover:text-red-200 hover:bg-red-500/10 transition-colors duration-200"
                      >
                        🚪 Đăng Xuất
                      </button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMenu}
            className="md:hidden text-white/70 hover:text-white p-2"
            aria-label="Toggle menu"
          >
            {isOpen ? "✕" : "☰"}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden bg-bg/95 backdrop-blur-lg"
          >
            <div className="container mx-auto px-4 py-4 space-y-4">
              {navigationLinks.map((link) => (
                <Link
                  key={link.path}
                  to={link.path}
                  onClick={() => setIsOpen(false)}
                  className={'nav-link block py-2 ' + (location.pathname === link.path ? 'active' : '')}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

export default Navigation;