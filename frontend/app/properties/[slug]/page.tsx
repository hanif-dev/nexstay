import PropertyDetail from './PropertyDetail';

export async function generateStaticParams() {
  try {
    const res = await fetch(
      process.env.NEXT_PUBLIC_API_URL + '/api/properties/units/'
    );
    const data = await res.json();
    const results = Array.isArray(data) ? data : data.results || [];
    return results.map((p: { slug: string }) => ({ slug: p.slug }));
  } catch {
    return [
      { slug: 'deluxe-room' },
      { slug: 'superior-suite' },
      { slug: 'presidential-suite' },
    ];
  }
}

export default async function PropertyDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <PropertyDetail slug={slug} />;
}

