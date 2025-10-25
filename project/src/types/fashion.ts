export interface RecommendationItem {
  name: string;
  color: string;
  style: string;
  description: string;
  matchReason: string;
}

export interface RecommendationCategory {
  category: string;
  items: RecommendationItem[];
}

export interface FashionRecommendation {
  analysis: string;
  recommendations: RecommendationCategory[];
  rawResponse?: string;
}

export type Gender = 'male' | 'female' | 'unisex';

export type ClothingType =
  | 't-shirt'
  | 'shirt'
  | 'pants'
  | 'jeans'
  | 'shoes'
  | 'jacket'
  | 'dress'
  | 'skirt'
  | 'shorts'
  | 'sweater'
  | 'hoodie'
  | 'other';

export type RecommendationCategory = 'tops' | 'bottoms' | 'shoes' | 'accessories';
