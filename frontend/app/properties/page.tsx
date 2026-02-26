'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import api from '@/lib/axios';
import { PropertyType } from '@/types';
import { FiUsers, FiStar } from 'react-icons/fi';
import toast from 'react-hot-toast';

export default function PropertiesPage() {
  const [properties, setProperties] = useState<PropertyType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/properties/types/')
      .then((res) => {
        const data = res.data;
        setProperties(Array.isArray(data) ? data : data.results || []);
  })
      .catch(() => toast.error('Failed to load properties'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="py-20 text-center text-gray-500">Loading properties...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-2">Available Stays</h1>
      <p className="text-gray-500 mb-8">Browse our curated selection of premium properties.</p>

      {properties.length === 0 && (
        <div className="text-center py-20 text-gray-500">
          <p className="text-lg">No properties available.</p>
          <p className="text-sm mt-2">Add properties via the admin panel.</p>
          <a href={process.env.NEXT_PUBLIC_API_URL + '/admin'} target="_blank" className="text-teal-600 hover:underline text-sm">
            Go to Admin
          </a>
        </div>
      )}

      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {properties.map((p) => {
          const primary = p.images.find((i) => i.is_primary) || p.images[0];
          return (
            <Link key={p.id} href={`/properties/${p.slug}`}
              className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition flex flex-col">
              {primary ? (
                <div className="h-56 overflow-hidden">
                  <img src={primary.image} alt={p.name} className="w-full h-full object-cover hover:scale-105 transition-transform" />
                </div>
              ) : (
                <div className="h-56 bg-teal-100 flex items-center justify-center text-teal-400 text-4xl">🏨</div>
              )}
              <div className="p-5 flex flex-col flex-1">
                <h2 className="text-xl font-semibold mb-1">{p.name}</h2>
                <p className="text-gray-500 text-sm mb-3 line-clamp-2">{p.description}</p>
                <div className="flex flex-wrap gap-2 mb-3">
                  {p.amenities.slice(0, 4).map((a) => (
                    <span key={a} className="px-2 py-1 bg-teal-50 text-teal-700 rounded-full text-xs">{a}</span>
                  ))}
                  {p.amenities.length > 4 && (
                    <span className="px-2 py-1 bg-gray-100 text-gray-500 rounded-full text-xs">+{p.amenities.length - 4} more</span>
                  )}
                </div>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-3">
                  <span className="flex items-center gap-1"><FiUsers /> {p.max_guests} guests max</span>
                  {p.average_rating && (
                    <span className="flex items-center gap-1"><FiStar className="text-yellow-400" /> {p.average_rating}</span>
                  )}
                </div>
                <div className="flex items-center justify-between mt-auto">
                  <div>
                    <p className="text-xs text-gray-400">{p.bed_configuration}</p>
                    <p className="text-xs text-gray-400">{p.size_sqm} m²</p>
                  </div>
                  <p className="text-lg font-bold text-teal-600">
                    IDR {Number(p.base_price).toLocaleString()}
                    <span className="text-xs font-normal text-gray-400">/night</span>
                  </p>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
