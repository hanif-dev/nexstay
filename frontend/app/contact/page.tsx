'use client';

import { useState, FormEvent } from 'react';
import toast from 'react-hot-toast';
import { FiMapPin, FiPhone, FiMail } from 'react-icons/fi';

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    toast.success('Message sent! We will get back to you soon.');
    setForm({ name: '', email: '', message: '' });
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold mb-8">Contact Us</h1>
      <div className="grid md:grid-cols-2 gap-12">
        <div>
          <p className="text-gray-600 mb-6">We are here to help with your reservations, partnerships, or any questions.</p>
          <div className="space-y-4">
            <div className="flex items-center gap-3 text-gray-700">
              <FiMapPin className="text-teal-600" size={20} />
              <span>Jakarta, Indonesia</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <FiPhone className="text-teal-600" size={20} />
              <span>+62 21 1234 5678</span>
            </div>
            <div className="flex items-center gap-3 text-gray-700">
              <FiMail className="text-teal-600" size={20} />
              <span>info@nexstay.com</span>
            </div>
          </div>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Name</label>
            <input type="text" required value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input type="email" required value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Message</label>
            <textarea rows={5} required value={form.message}
              onChange={(e) => setForm({ ...form, message: e.target.value })}
              className="w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-teal-500" />
          </div>
          <button type="submit"
            className="w-full bg-teal-600 text-white py-2 rounded-lg hover:bg-teal-700">
            Send Message
          </button>
        </form>
      </div>
    </div>
  );
}
