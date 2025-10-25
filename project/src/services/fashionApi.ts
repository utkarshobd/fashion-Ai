import { Gender, ClothingType, FashionRecommendation } from '../types/fashion';

const API_URL = `${import.meta.env.VITE_SUPABASE_URL}/functions/v1/fashion-recommendation`;

export interface GetRecommendationParams {
  imageBase64: string;
  itemType: ClothingType;
  gender: Gender;
  selectedCategories?: string[];
  userId?: string;
}

export async function getRecommendation(
  params: GetRecommendationParams
): Promise<{ success: boolean; recommendation?: FashionRecommendation; error?: string }> {
  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${import.meta.env.VITE_SUPABASE_ANON_KEY}`,
      },
      body: JSON.stringify(params),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to get recommendation');
    }

    return data;
  } catch (error) {
    console.error('Error getting recommendation:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'An unknown error occurred',
    };
  }
}

export function imageToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      const base64 = result.split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}
