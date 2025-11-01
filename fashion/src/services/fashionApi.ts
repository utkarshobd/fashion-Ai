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
    console.error('Error getting recommendation, using fallback:', error);
    
    // Fallback to local recommendations when API fails
    return {
      success: true,
      recommendation: generateLocalRecommendation(params)
    };
  }
}

function generateLocalRecommendation(params: GetRecommendationParams): FashionRecommendation {
  const { itemType, gender, selectedCategories } = params;
  const categories = selectedCategories || ['tops', 'bottoms', 'shoes', 'accessories'];
  
  const fashionRules: Record<string, any> = {
    't-shirt': {
      analysis: 'Casual t-shirt perfect for everyday wear',
      bottoms: [
        { name: 'Slim Fit Jeans', color: 'Dark Blue', style: 'Casual', description: 'Classic denim jeans', matchReason: 'Perfect casual combination' },
        { name: 'Chino Pants', color: 'Khaki', style: 'Smart Casual', description: 'Versatile pants', matchReason: 'Elevates the t-shirt look' }
      ],
      shoes: [
        { name: 'White Sneakers', color: 'White', style: 'Casual', description: 'Clean sneakers', matchReason: 'Classic casual footwear' },
        { name: 'Canvas Shoes', color: 'Navy', style: 'Casual', description: 'Comfortable shoes', matchReason: 'Complements casual style' }
      ],
      accessories: [
        { name: 'Baseball Cap', color: 'Black', style: 'Casual', description: 'Sporty headwear', matchReason: 'Adds sporty element' },
        { name: 'Canvas Backpack', color: 'Navy', style: 'Casual', description: 'Practical bag', matchReason: 'Functional accessory' }
      ]
    },
    'shirt': {
      analysis: 'Versatile button-up shirt suitable for various occasions',
      bottoms: [
        { name: 'Dress Pants', color: 'Navy', style: 'Formal', description: 'Professional trousers', matchReason: 'Creates polished look' },
        { name: 'Dark Jeans', color: 'Indigo', style: 'Smart Casual', description: 'Refined denim', matchReason: 'Balances formal and casual' }
      ],
      shoes: [
        { name: 'Oxford Shoes', color: 'Brown', style: 'Formal', description: 'Classic dress shoes', matchReason: 'Professional pairing' },
        { name: 'Loafers', color: 'Brown', style: 'Smart Casual', description: 'Comfortable dress shoes', matchReason: 'Sophisticated yet comfortable' }
      ],
      accessories: [
        { name: 'Leather Belt', color: 'Brown', style: 'Formal', description: 'Quality belt', matchReason: 'Essential accessory' },
        { name: 'Classic Watch', color: 'Silver', style: 'Formal', description: 'Elegant timepiece', matchReason: 'Adds sophistication' }
      ]
    }
  };

  const rules = fashionRules[itemType] || fashionRules['shirt'];
  const recommendations = [];

  for (const category of categories) {
    if (rules[category]) {
      recommendations.push({
        category,
        items: rules[category].slice(0, 3)
      });
    }
  }

  return {
    analysis: rules.analysis,
    recommendations
  };
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
