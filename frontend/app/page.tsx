'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { useAuthStore } from '@/store/authStore';
import { FiSearch, FiStar, FiShield, FiClock } from 'react-icons/fi';

export default function Home() {
  const { checkAuth } = useAuthStore();
  useEffect(() => { checkAuth(); }, [checkAuth]);

  return (
    <div>
      <section className="relative h-[520px] bg-gradient-to-r from-teal-700 to-teal-900 text-white flex items-center">
        <div className="absolute inset-0 bg-black opacity-20" />
        <div className="relative z-10 max-w-7xl mx-auto px-4">
          <h1 className="text-5xl font-bold mb-4">Welcome to NexStay</h1>
          <p className="text-xl mb-8 max-w-2xl">Discover premium stays with curated amenities and exceptional service.</p>
          <div className="flex gap-4">
            <Link href="/properties" className="bg-white text-teal-700 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 flex items-center gap-2">
              <FiSearch /> Explore Stays
            </Link>
            <Link href="/register" className="border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-teal-700">
              Sign Up
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Why NexStay?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: FiStar, title: 'Curated Quality', desc: 'Hand-picked properties with world-class amenities.' },
              { icon: FiShield, title: 'Secure Booking', desc: 'Advanced security with encrypted payments.' },
              { icon: FiClock, title: '24/7 Support', desc: 'Round-the-clock assistance for all your needs.' },
            ].map(({ icon: Icon, title, desc }) => (
              <div key={title} className="bg-white p-8 rounded-xl shadow-md text-center">
                <div className="bg-teal-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Icon className="text-teal-600" size={28} />
                </div>
                <h3 className="text-xl font-semibold mb-3">{title}</h3>
                <p className="text-gray-600">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-teal-600 text-white text-center">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-4xl font-bold mb-4">Ready to Book Your Stay?</h2>
          <p className="text-xl mb-8">Join thousands of guests and find your perfect stay.</p>
          <Link href="/properties" className="bg-white text-teal-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 inline-block">
            View All Stays
          </Link>
        </div>
      </section>
    </div>
  );
}
