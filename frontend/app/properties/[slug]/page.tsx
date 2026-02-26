import PropertyDetail from './PropertyDetail';

export async function generateStaticParams() {
  try {
    const res = await fetch(
      process.env.NEXT_PUBLIC_API_URL + '/api/properties/types/'
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

export default function PropertyDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  return <PropertyDetail slug={params.slug} />;
}
