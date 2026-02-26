'use client';

import { useEffect, useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/axios';
import { PropertyType } from '@/types';
import { useAuthStore } from '@/store/authStore';
import toast from 'react-hot-toast';
import { FiUsers, FiMaximize2, FiStar, FiCheckCircle } from 'react-icons/fi';

interface Unit {
  id: number;
  unit_number: string;
  floor: number;
}

const OTA_OPTIONS = [
  { value: 'direct', label: 'Direct (Website)' },
  { value: 'booking_com', label: 'Booking.com' },
  { value: 'expedia', label: 'Expedia' },
  { value: 'agoda', label: 'Agoda' },
  { value: 'traveloka', label: 'Traveloka' },
  { value: 'tiket_com', label: 'Tiket.com' },
  { value: 'trip_com', label: 'Trip.com' },
];

const PAYMENT_METHODS = [
  { value: 'credit_card', label: 'Credit Card' },
  { value: 'debit_card', label: 'Debit Card' },
  { value: 'virtual_account', label: 'Virtual Account' },
  { value: 'qris', label: 'QRIS' },
  { value: 'gopay', label: 'GoPay' },
  { value: 'ovo', label: 'OVO' },
  { value: 'dana', label: 'DANA' },
  { value: 'bank_transfer', label: 'Bank Transfer' },
];

export default function PropertyDetail({ slug }: { slug: string }) {
  const router = useRouter();
  const { isAuthenticated, checkAuth } = useAuthStore();
  const [property, setProperty] = useState<PropertyType | null>(null);
  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeImage, setActiveImage] = useState<string>('');
  const [form, setForm] = useState({
    unit_id: '',
    check_in: '',
    check_out: '',
    num_guests: 1,
    special_requests: '',
    ota_source: 'direct',
    payment_method: 'credit_card',
  });
  const [bookingLoading, setBookingLoading] = useState(false);
  const [nights, setNights] = useState(0);
  const [totalPrice, setTotalPrice] = useState(0);

  useEffect(() => { checkAuth(); }, [checkAuth]);

  useEffect(() => {
    api.get(`/properties/types/${slug}/`)
      .then((res) => {
        setProperty(res.data);
        const primary = res.data.images.find((i: { is_primary: boolean }) => i.is_primary) || res.data.images[0];
        if (primary) setActiveImage(primary.image);
        return api.get(`/properties/units/?property_type=${res.data.id}`);
      })
      .then((res) => {
        const data = res.data;
        setUnits(Array.isArray(data) ? data : data.results || []);
      })
      .catch(() => toast.error('Failed to load property'))
      .finally(() => setLoading(false));
  }, [slug]);

  useEffect(() => {
    if (form.check_in && form.check_out && property) {
      const diff = (new Date(form.check_out).getTime() - new Date(form.check_in).getTime()) / 86400000;
      if (diff > 0) {
        setNights(diff);
        const base = Number(property.base_price) * diff;
        setTotalPrice(base + base * 0.11 + base * 0.05);
      } else {
        setNights(0);
        setTotalPrice(0);
      }
    }
  }, [form.check_in, form.check_out, property]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: name === 'num_guests' ? Number(value) : value }));
  };

  const handleBook = async (e: FormEvent) => {
    e.preventDefault();
    if (!isAuthenticated) { toast.error('Please login to book'); router.push('/login'); return; }
    if (!form.unit_id) { toast.error('Please select a unit'); return; }
    if (nights <= 0) { toast.error('Invalid dates'); return; }
    setBookingLoading(true);
    try {
      await api.post('/reservations/', {
        unit_id: Number(form.unit_id),
        check_in: form.check_in,
        check_out: form.check_out,
        num_guests: form.num_guests,
        special_requests: form.special_requests,
      });
      toast.success('Reservation created successfully!');
      router.push('/dashboard');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail || 'Booking failed');
    } finally {
      setBookingLoading(false);
    }
  };

  if (loading) return <div className="py-20 text-center">Loading...</div>;
  if (!property) return <div className="py-20 text-center">Property not found</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          {activeImage ? (
            <div className="h-80 w-full mb-3 overflow-hidden rounded-xl">
              <img src={activeImage} alt={property.name} className="w-full h-full object-cover" />
            </div>
          ) : (
            <div className="h-80 w-full mb-3 bg-teal-100 rounded-xl flex items-center justify-center text-6xl">🏨</div>
          )}
          {property.images.length > 1 && (
            <div className="flex gap-2 mb-6 overflow-x-auto">
              {property.images.map((img) => (
                <img key={img.id} src={img.image} alt={img.caption}
                  onClick={() => setActiveImage(img.image)}
                  className={`h-20 w-32 object-cover rounded-lg cursor-pointer flex-shrink-0 ${activeImage === img.image ? 'ring-2 ring-teal-500' : ''}`}
                />
              ))}
            </div>
          )}
          <h1 className="text-3xl font-bold mb-2">{property.name}</h1>
          <p className="text-gray-600 mb-4">{property.description}</p>
          <div className="flex flex-wrap gap-3 mb-6 text-sm">
            <span className="flex items-center gap-1 bg-gray-100 px-3 py-1 rounded-full">
              <FiUsers /> {property.max_guests} guests
            </span>
            <span className="flex items-center gap-1 bg-gray-100 px-3 py-1 rounded-full">
              <FiMaximize2 /> {property.size_sqm} m²
            </span>
            <span className="bg-gray-100 px-3 py-1 rounded-full">{property.bed_configuration}</span>
            {property.view_type && (
              <span className="bg-gray-100 px-3 py-1 rounded-full">{property.view_type}</span>
            )}
            {property.average_rating && (
              <span className="flex items-center gap-1 bg-yellow-50 px-3 py-1 rounded-full text-yellow-700">
                <FiStar /> {property.average_rating}
              </span>
            )}
          </div>
          <h2 className="text-xl font-semibold mb-3">Amenities</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-8">
            {property.amenities.map((a) => (
              <div key={a} className="flex items-center gap-2 text-sm text-gray-700">
                <FiCheckCircle className="text-teal-500 flex-shrink-0" />
                <span>{a}</span>
              </div>
            ))}
          </div>
        </div>

        <div>
          <div className="bg-white rounded-xl shadow-lg p-6 sticky top-24">
            <p className="text-2xl font-bold text-teal-600 mb-1">
              IDR {Number(property.base_price).toLocaleString()}
              <span className="text-sm font-normal text-gray-500"> / night</span>
            </p>
            <p className="text-xs text-gray-400 mb-4">+11% tax +5% service charge</p>
            <form onSubmit={handleBook} className="space-y-3">
              <div>
                <label className="block text-sm font-medium mb-1">Unit</label>
                <select name="unit_id" value={form.unit_id} onChange={handleChange}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500">
                  <option value="">Select a unit</option>
                  {units.map((u) => (
                    <option key={u.id} value={u.id}>Unit {u.unit_number} (Floor {u.floor})</option>
                  ))}
                </select>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="block text-sm font-medium mb-1">Check-in</label>
                  <input type="date" name="check_in" value={form.check_in} onChange={handleChange} required
                    className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Check-out</label>
                  <input type="date" name="check_out" value={form.check_out} onChange={handleChange} required
                    className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Guests</label>
                <input type="number" name="num_guests" min={1} max={property.max_guests}
                  value={form.num_guests} onChange={handleChange}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Book via</label>
                <select name="ota_source" value={form.ota_source} onChange={handleChange}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500">
                  {OTA_OPTIONS.map((o) => (
                    <option key={o.value} value={o.value}>{o.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Payment Method</label>
                <select name="payment_method" value={form.payment_method} onChange={handleChange}
                  className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500">
                  {PAYMENT_METHODS.map((m) => (
                    <option key={m.value} value={m.value}>{m.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Special Requests</label>
                <textarea name="special_requests" value={form.special_requests} onChange={handleChange}
                  rows={2} className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
              </div>
              {nights > 0 && (
                <div className="bg-teal-50 rounded-lg p-3 text-sm space-y-1">
                  <div className="flex justify-between">
                    <span>IDR {Number(property.base_price).toLocaleString()} x {nights} night(s)</span>
                    <span>IDR {(Number(property.base_price) * nights).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-gray-500">
                    <span>Tax (11%)</span>
                    <span>IDR {(Number(property.base_price) * nights * 0.11).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between text-gray-500">
                    <span>Service (5%)</span>
                    <span>IDR {(Number(property.base_price) * nights * 0.05).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between font-bold border-t pt-1">
                    <span>Total</span>
                    <span className="text-teal-700">IDR {Math.round(totalPrice).toLocaleString()}</span>
                  </div>
                </div>
              )}
              <button type="submit" disabled={bookingLoading}
                className="w-full bg-teal-600 text-white py-3 rounded-lg font-semibold hover:bg-teal-700 disabled:opacity-50">
                {bookingLoading ? 'Processing...' : 'Reserve Now'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
