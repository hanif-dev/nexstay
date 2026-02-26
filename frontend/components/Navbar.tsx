'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { FiMenu, FiX, FiUser, FiLogOut } from 'react-icons/fi';

export default function Navbar() {
  const { user, isAuthenticated, logout, checkAuth } = useAuthStore();
  const router = useRouter();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const handleLogout = () => {
     logout();
     router.push('/');
   };

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 flex justify-between h-16 items-center">
        <Link href="/" className="text-2xl font-bold text-teal-600">NexStay</Link>
        <div className="hidden md:flex items-center space-x-8">
          <Link href="/properties" className="text-gray-700 hover:text-teal-600">Properties</Link>
          <Link href="/about" className="text-gray-700 hover:text-teal-600">About</Link>
          <Link href="/contact" className="text-gray-700 hover:text-teal-600">Contact</Link>
          {isAuthenticated ? (
            <>
              <Link href="/dashboard" className="flex items-center gap-1 text-gray-700 hover:text-teal-600">
                <FiUser /> {user?.first_name || 'Dashboard'}
              </Link>
              <button onClick={handleLogout} className="flex items-center gap-1 text-red-600 hover:text-red-800">
                <FiLogOut /> Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="text-gray-700 hover:text-teal-600">Login</Link>
              <Link href="/register" className="bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700">Sign Up</Link>
            </>
          )}
        </div>
        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <FiX size={24} /> : <FiMenu size={24} />}
        </button>
      </div>
      {open && (
        <div className="md:hidden bg-white border-t px-4 py-3 space-y-2">
          <Link href="/properties" className="block py-2 text-gray-700">Properties</Link>
          <Link href="/about" className="block py-2 text-gray-700">About</Link>
          <Link href="/contact" className="block py-2 text-gray-700">Contact</Link>
          {isAuthenticated ? (
            <>
              <Link href="/dashboard" className="block py-2 text-gray-700">Dashboard</Link>
              <button onClick={handleLogout} className="block py-2 text-red-600">Logout</button>
            </>
          ) : (
            <>
              <Link href="/login" className="block py-2 text-gray-700">Login</Link>
              <Link href="/register" className="block py-2 bg-teal-600 text-white rounded text-center">Sign Up</Link>
            </>
          )}
        </div>
      )}
    </nav>
  );
}
