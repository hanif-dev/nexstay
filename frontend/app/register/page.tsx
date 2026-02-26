'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import toast from 'react-hot-toast';

interface FormData {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone: string;
  password: string;
  password2: string;
}

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuthStore();
  const [form, setForm] = useState<FormData>({
    email: '', username: '', first_name: '', last_name: '',
    phone: '', password: '', password2: '',
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (form.password !== form.password2) {
      toast.error("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await register(form);
      toast.success('Account created! Please login.');
      router.push('/login');
    } catch (err: unknown) {
      const error = err as { response?: { data?: Record<string, string[]> } };
      const data = error.response?.data;
      if (data) {
        const first = Object.values(data)[0];
        toast.error(Array.isArray(first) ? first[0] : 'Registration failed');
      } else {
        toast.error('Registration failed');
      }
    } finally {
      setLoading(false);
    }
  };

  const fields: { name: keyof FormData; label: string; type?: string }[] = [
    { name: 'first_name', label: 'First Name' },
    { name: 'last_name', label: 'Last Name' },
    { name: 'email', label: 'Email', type: 'email' },
    { name: 'username', label: 'Username' },
    { name: 'phone', label: 'Phone', type: 'tel' },
    { name: 'password', label: 'Password', type: 'password' },
    { name: 'password2', label: 'Confirm Password', type: 'password' },
  ];

  return (
    <div className="flex items-center justify-center py-16 bg-gray-50">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Create Account</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {fields.map(({ name, label, type }) => (
            <div key={name}>
              <label className="block text-sm font-medium mb-1">{label}</label>
              <input
                type={type || 'text'}
                name={name}
                value={form[name]}
                onChange={handleChange}
                required={name !== 'phone'}
                className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
            </div>
          ))}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-teal-600 text-white py-2 rounded-lg hover:bg-teal-700 disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>
        <p className="text-center text-sm text-gray-600 mt-4">
          Already have an account?{' '}
          <a href="/login" className="text-teal-600 hover:underline">Login</a>
        </p>
      </div>
    </div>
  );
}
