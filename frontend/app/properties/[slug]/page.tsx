import PropertyDetail from './PropertyDetail';

export const dynamic = 'force-dynamic';

export async function generateStaticParams() {
  return [];
}

export default async function PropertyDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <PropertyDetail slug={slug} />;
}

