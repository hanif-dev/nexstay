export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white mt-20">
      <div className="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 className="text-2xl font-bold text-teal-400 mb-4">NexStay</h3>
          <p className="text-gray-400">Premium property reservation platform.</p>
        </div>
        <div>
          <h4 className="font-semibold mb-4">Navigation</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="/properties" className="hover:text-white">Properties</a></li>
            <li><a href="/about" className="hover:text-white">About Us</a></li>
            <li><a href="/contact" className="hover:text-white">Contact</a></li>
          </ul>
        </div>
        <div>
          <h4 className="font-semibold mb-4">Policies</h4>
          <ul className="space-y-2 text-gray-400">
            <li><a href="#" className="hover:text-white">Privacy Policy</a></li>
            <li><a href="#" className="hover:text-white">Terms of Service</a></li>
            <li><a href="#" className="hover:text-white">Cancellation Policy</a></li>
          </ul>
        </div>
        <div>
          <h4 className="font-semibold mb-4">Contact</h4>
          <ul className="space-y-2 text-gray-400">
            <li>Jakarta, Indonesia</li>
            <li>info@nexstay.com</li>
            <li>+62 21 1234 5678</li>
          </ul>
        </div>
      </div>
      <div className="border-t border-gray-800 py-6 text-center text-gray-400">
        <p>&copy; 2026 NexStay. All rights reserved.</p>
      </div>
    </footer>
  );
}
