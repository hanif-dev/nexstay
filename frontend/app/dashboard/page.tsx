'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/axios';
import { useAuthStore } from '@/store/authStore';
import { Reservation, Payment } from '@/types';
import toast from 'react-hot-toast';

export default function DashboardPage() {
  const { isAuthenticated, checkAuth, user } = useAuthStore();
  const router = useRouter();
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { checkAuth(); }, [checkAuth]);
  useEffect(() => {
    if (isAuthenticated === false) router.push('/login');
  }, [isAuthenticated, router]);

  useEffect(() => {
    if (!isAuthenticated) return;
    Promise.all([api.get('/reservations/'), api.get('/payments/')])
      .then(([res, pay]) => { 
        const resData = res.data;
        const payData = pay.data;
        setReservations(Array.isArray(resData) ? resData : resData.results || []);
        setPayments(Array.isArray(payData) ? payData : payData.results || []);
      })
      .catch(() => toast.error('Failed to load dashboard'))
      .finally(() => setLoading(false));
  }, [isAuthenticated]);

  const statusColor: Record<string, string> = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    checked_in: 'bg-green-100 text-green-700',
    checked_out: 'bg-gray-100 text-gray-700',
    cancelled: 'bg-red-100 text-red-700',
    completed: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
  };

  if (loading) return <div className="py-20 text-center">Loading dashboard...</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-2">Welcome, {user?.first_name}!</h1>
      <p className="text-gray-500 mb-8">Manage your reservations and payments here.</p>

      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-semibold mb-4">My Reservations</h2>
          {reservations.length === 0 && (
            <div className="text-center py-10 text-gray-400 border rounded-xl">
              <p>No reservations yet.</p>
              <a href="/properties" className="text-teal-600 hover:underline text-sm mt-2 block">Browse properties</a>
            </div>
          )}
          <div className="space-y-3">
            {reservations.map((r) => (
              <div key={r.id} className="border rounded-xl p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-teal-700">{r.confirmation_code}</p>
                  <span className={`text-xs px-2 py-1 rounded-full ${statusColor[r.status] || 'bg-gray-100'}`}>
                    {r.status.replace('_', ' ')}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{r.check_in} → {r.check_out}</p>
                <p className="text-sm text-gray-600">{r.nights} night(s)</p>
                <p className="text-sm font-bold mt-1">IDR {Number(r.total_price).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">My Payments</h2>
          {payments.length === 0 && (
            <div className="text-center py-10 text-gray-400 border rounded-xl">
              <p>No payments yet.</p>
            </div>
          )}
          <div className="space-y-3">
            {payments.map((p) => (
              <div key={p.id} className="border rounded-xl p-4">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-mono text-sm text-gray-500">{p.transaction_id.slice(0, 16)}...</p>
                  <span className={`text-xs px-2 py-1 rounded-full ${statusColor[p.status] || 'bg-gray-100'}`}>
                    {p.status}
                  </span>
                </div>
                <p className="text-sm text-gray-600">Method: {p.payment_method.replace('_', ' ')}</p>
                <p className="text-sm font-bold mt-1">{p.currency} {Number(p.total_amount).toLocaleString()}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
