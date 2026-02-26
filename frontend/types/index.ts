export interface PropertyImage {
  id: number;
  image: string;
  caption: string;
  is_primary: boolean;
  order: number;
}

export interface PropertyType {
  id: number;
  name: string;
  slug: string;
  description: string;
  max_guests: number;
  base_price: string;
  size_sqm: number;
  bed_configuration: string;
  view_type: string;
  amenities: string[];
  images: PropertyImage[];
  average_rating: number | null;
}

export interface Reservation {
  id: number;
  confirmation_code: string;
  check_in: string;
  check_out: string;
  status: string;
  total_price: string;
  nights: number;
}

export interface Payment {
  id: number;
  transaction_id: string;
  total_amount: string;
  currency: string;
  status: string;
  payment_method: string;
  paid_at: string;
}
