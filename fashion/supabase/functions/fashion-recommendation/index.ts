import { createClient } from 'npm:@supabase/supabase-js@2.57.4';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Client-Info, Apikey',
};

interface FashionRecommendationRequest {
  imageBase64: string;
  itemType: string;
  gender: 'male' | 'female' | 'unisex';
  selectedCategories?: string[];
  userId?: string;
}

interface ColorAnalysis {
  dominantColors: string[];
  brightness: 'light' | 'medium' | 'dark';
  pattern: string;
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 200,
      headers: corsHeaders,
    });
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    const requestData: FashionRecommendationRequest = await req.json();
    const { imageBase64, itemType, gender, selectedCategories, userId } = requestData;

    const categoriesToRecommend = selectedCategories && selectedCategories.length > 0
      ? selectedCategories
      : ['tops', 'bottoms', 'shoes', 'accessories'];

    // Use Hugging Face's free BLIP model for image captioning
    const hfToken = Deno.env.get('HUGGINGFACE_API_KEY') || 'hf_demo';
    
    let imageDescription = '';
    try {
      const imageBuffer = Uint8Array.from(atob(imageBase64), c => c.charCodeAt(0));
      
      const captionResponse = await fetch(
        'https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large',
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${hfToken}`,
            'Content-Type': 'application/json',
          },
          body: imageBuffer,
        }
      );

      if (captionResponse.ok) {
        const captionData = await captionResponse.json();
        imageDescription = captionData[0]?.generated_text || 'a clothing item';
      }
    } catch (error) {
      console.log('Image analysis error, using fallback:', error);
      imageDescription = `a ${itemType}`;
    }

    // Generate smart recommendations based on fashion rules
    const recommendationData = generateFashionRecommendations(
      itemType,
      gender,
      categoriesToRecommend,
      imageDescription
    );

    // Store recommendation in database
    const { data: recommendation, error: dbError } = await supabase
      .from('recommendations')
      .insert({
        user_id: userId || null,
        uploaded_item_type: itemType,
        uploaded_image_url: imageBase64.substring(0, 100) + '...',
        gender: gender,
        recommendation_data: recommendationData,
        selected_categories: selectedCategories || null,
      })
      .select()
      .single();

    if (dbError) {
      console.error('Database error:', dbError);
    }

    return new Response(
      JSON.stringify({
        success: true,
        recommendation: recommendationData,
        recommendationId: recommendation?.id,
      }),
      {
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        },
      }
    );
  } catch (error) {
    console.error('Error:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message || 'An error occurred processing your request',
      }),
      {
        status: 500,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
        },
      }
    );
  }
});

function generateFashionRecommendations(
  itemType: string,
  gender: string,
  categories: string[],
  imageDescription: string
) {
  const recommendations = [];

  // Fashion matching rules database
  const fashionRules = {
    't-shirt': {
      analysis: 'Casual t-shirt perfect for everyday wear',
      tops: [],
      bottoms: [
        { name: 'Slim Fit Jeans', color: 'Dark Blue', style: 'Casual', description: 'Classic denim jeans that pair well with any t-shirt', matchReason: 'Denim is a timeless match for casual tees, creating a relaxed yet put-together look' },
        { name: 'Chino Pants', color: 'Khaki or Navy', style: 'Smart Casual', description: 'Versatile pants that elevate your t-shirt look', matchReason: 'Chinos add a touch of sophistication while maintaining comfort' },
        { name: 'Cargo Shorts', color: 'Olive or Beige', style: 'Casual', description: 'Perfect for warm weather and relaxed settings', matchReason: 'Great for a laid-back, functional summer style' },
      ],
      shoes: [
        { name: 'White Sneakers', color: 'White', style: 'Casual', description: 'Clean, minimalist sneakers', matchReason: 'White sneakers are versatile and match any t-shirt color perfectly' },
        { name: 'Canvas Shoes', color: 'Navy or Black', style: 'Casual', description: 'Comfortable everyday footwear', matchReason: 'Canvas shoes complement the casual vibe of a t-shirt' },
        { name: 'Slip-on Sneakers', color: 'Gray', style: 'Casual', description: 'Easy-to-wear comfortable shoes', matchReason: 'Effortless style that matches the easy-going nature of tees' },
      ],
      accessories: [
        { name: 'Baseball Cap', color: 'Black or Navy', style: 'Casual', description: 'Classic sporty headwear', matchReason: 'Adds a sporty, youthful element to your outfit' },
        { name: 'Leather Watch', color: 'Brown or Black', style: 'Casual', description: 'Simple timepiece with leather strap', matchReason: 'Adds a touch of maturity without being too formal' },
        { name: 'Canvas Backpack', color: 'Navy or Gray', style: 'Casual', description: 'Practical and stylish bag', matchReason: 'Functional accessory that fits the casual aesthetic' },
      ],
    },
    'shirt': {
      analysis: 'Versatile button-up shirt suitable for various occasions',
      tops: [],
      bottoms: [
        { name: 'Dress Pants', color: 'Charcoal or Navy', style: 'Formal', description: 'Tailored trousers for professional settings', matchReason: 'Creates a polished, business-appropriate ensemble' },
        { name: 'Dark Jeans', color: 'Dark Indigo', style: 'Smart Casual', description: 'Refined denim for a modern look', matchReason: 'Balances the formality of a shirt with casual comfort' },
        { name: 'Chino Pants', color: 'Navy or Stone', style: 'Smart Casual', description: 'Versatile pants for work or weekend', matchReason: 'Perfect middle ground between formal and casual' },
      ],
      shoes: [
        { name: 'Oxford Shoes', color: 'Brown or Black', style: 'Formal', description: 'Classic leather dress shoes', matchReason: 'Traditional pairing for a professional, put-together look' },
        { name: 'Loafers', color: 'Brown', style: 'Smart Casual', description: 'Slip-on leather shoes', matchReason: 'Sophisticated yet comfortable, ideal for business casual' },
        { name: 'Chelsea Boots', color: 'Black or Tan', style: 'Smart Casual', description: 'Sleek ankle boots', matchReason: 'Modern, versatile footwear that works day to night' },
      ],
      accessories: [
        { name: 'Leather Belt', color: 'Brown or Black', style: 'Formal', description: 'Quality leather belt matching shoes', matchReason: 'Essential accessory that ties the whole outfit together' },
        { name: 'Classic Watch', color: 'Silver or Gold', style: 'Formal', description: 'Elegant timepiece with metal strap', matchReason: 'Adds sophistication and shows attention to detail' },
        { name: 'Leather Briefcase', color: 'Brown', style: 'Professional', description: 'Professional bag for work essentials', matchReason: 'Completes a business-ready appearance' },
      ],
    },
    'pants': {
      analysis: 'Well-fitted pants as a foundation for stylish outfits',
      tops: [
        { name: 'Button-Up Shirt', color: 'White or Light Blue', style: 'Smart Casual', description: 'Classic dress shirt', matchReason: 'Timeless combination for a sharp, professional look' },
        { name: 'Polo Shirt', color: 'Navy or Gray', style: 'Casual', description: 'Collared knit shirt', matchReason: 'Smart casual option that balances comfort and style' },
        { name: 'Crew Neck Sweater', color: 'Navy or Burgundy', style: 'Smart Casual', description: 'Comfortable knitwear', matchReason: 'Adds warmth and sophistication for cooler weather' },
      ],
      shoes: [
        { name: 'Dress Shoes', color: 'Black or Brown', style: 'Formal', description: 'Polished leather footwear', matchReason: 'Elevates the pants for professional or formal occasions' },
        { name: 'Loafers', color: 'Brown or Burgundy', style: 'Smart Casual', description: 'Comfortable slip-on shoes', matchReason: 'Versatile choice that works for various settings' },
        { name: 'Clean Sneakers', color: 'White or Minimal', style: 'Casual', description: 'Modern minimal sneakers', matchReason: 'Contemporary look mixing formal pants with casual footwear' },
      ],
      accessories: [
        { name: 'Leather Belt', color: 'Matching Shoe Color', style: 'Essential', description: 'Quality belt in coordinating color', matchReason: 'Must-have accessory that creates visual cohesion' },
        { name: 'Watch', color: 'Silver or Leather Strap', style: 'Classic', description: 'Elegant timepiece', matchReason: 'Adds a refined finishing touch' },
        { name: 'Pocket Square', color: 'Complementary', style: 'Formal', description: 'Folded fabric for breast pocket', matchReason: 'Adds personality and flair to dressy outfits' },
      ],
    },
    'jeans': {
      analysis: 'Versatile denim perfect for casual and smart-casual looks',
      tops: [
        { name: 'Graphic T-Shirt', color: 'Any', style: 'Casual', description: 'Tee with prints or designs', matchReason: 'Classic casual combo perfect for everyday wear' },
        { name: 'Henley Shirt', color: 'Gray or Navy', style: 'Casual', description: 'Collarless pullover with button placket', matchReason: 'Step up from basic tees while staying comfortable' },
        { name: 'Denim Jacket', color: 'Contrasting Wash', style: 'Casual', description: 'Classic denim jacket in different shade', matchReason: 'Double denim works when washes contrast properly' },
      ],
      shoes: [
        { name: 'Sneakers', color: 'White or Black', style: 'Casual', description: 'Comfortable athletic-inspired shoes', matchReason: 'Perfect pairing for denim, versatile and comfortable' },
        { name: 'Desert Boots', color: 'Tan or Brown', style: 'Casual', description: 'Suede ankle boots', matchReason: 'Adds texture and elevates jeans for smart casual' },
        { name: 'High-Top Sneakers', color: 'Various', style: 'Streetwear', description: 'Athletic shoes with ankle coverage', matchReason: 'Creates a street-style edge with denim' },
      ],
      accessories: [
        { name: 'Canvas Belt', color: 'Navy or Khaki', style: 'Casual', description: 'Fabric belt with metal buckle', matchReason: 'Casual accessory that complements denim perfectly' },
        { name: 'Beanie', color: 'Black or Gray', style: 'Casual', description: 'Knit winter cap', matchReason: 'Adds urban style for cooler weather' },
        { name: 'Backpack', color: 'Black or Navy', style: 'Casual', description: 'Practical everyday bag', matchReason: 'Functional accessory for casual denim outfits' },
      ],
    },
    'shoes': {
      analysis: 'Quality footwear to anchor your outfit',
      tops: [
        { name: 'Casual Shirt', color: 'Complementary', style: 'Casual', description: 'Relaxed button-up or tee', matchReason: 'Balances your shoe choice with appropriate casualness' },
        { name: 'Sweater', color: 'Neutral Tones', style: 'Smart Casual', description: 'Comfortable knitwear', matchReason: 'Creates cohesive look with smart footwear' },
      ],
      bottoms: [
        { name: 'Jeans', color: 'Dark or Medium Wash', style: 'Casual', description: 'Classic denim pants', matchReason: 'Universal pairing that works with most shoe styles' },
        { name: 'Chinos', color: 'Navy or Khaki', style: 'Smart Casual', description: 'Versatile cotton pants', matchReason: 'Elevates sneakers or complements dress shoes' },
        { name: 'Joggers', color: 'Black or Gray', style: 'Athleisure', description: 'Comfortable athletic pants', matchReason: 'Perfect for sporty footwear and casual style' },
      ],
      accessories: [
        { name: 'Watch', color: 'Matches Shoe Hardware', style: 'Coordinated', description: 'Timepiece in coordinating metal', matchReason: 'Creates harmony between shoe details and accessories' },
        { name: 'Belt', color: 'Matches Shoe Color', style: 'Essential', description: 'Belt in similar tone to shoes', matchReason: 'Classic rule of matching leather goods' },
        { name: 'Socks', color: 'Fun or Neutral', style: 'Personal', description: 'Ankle or crew socks', matchReason: 'Shows personality while maintaining comfort' },
      ],
    },
  };

  // Get rules for the item type, default to shirt if not found
  const rules = fashionRules[itemType as keyof typeof fashionRules] || fashionRules['shirt'];
  const analysis = `${rules.analysis}. Detected: ${imageDescription}`;

  // Generate recommendations for selected categories
  for (const category of categories) {
    if (rules[category as keyof typeof rules] && Array.isArray(rules[category as keyof typeof rules])) {
      const items = rules[category as keyof typeof rules] as any[];
      
      // Adjust recommendations based on gender
      const genderItems = items.map(item => {
        if (gender === 'female' && category === 'shoes') {
          // Add female-specific options
          const femaleAlternatives: Record<string, any> = {
            'Sneakers': { ...item, name: 'Fashion Sneakers', description: 'Stylish athletic-inspired shoes with feminine touch' },
            'Loafers': { ...item, name: 'Ballet Flats or Loafers', description: 'Elegant comfortable flat shoes' },
            'Chelsea Boots': { ...item, name: 'Ankle Boots', description: 'Versatile heeled or flat ankle boots' },
          };
          return femaleAlternatives[item.name] || item;
        }
        if (gender === 'female' && category === 'accessories') {
          const femaleAccessories: Record<string, any> = {
            'Baseball Cap': { ...item, name: 'Fashion Hat or Cap', description: 'Stylish headwear options' },
            'Beanie': { ...item, name: 'Beanie or Beret', description: 'Fashionable winter headwear' },
          };
          return femaleAccessories[item.name] || item;
        }
        return item;
      });

      recommendations.push({
        category,
        items: genderItems.slice(0, 3),
      });
    }
  }

  return {
    analysis,
    recommendations,
  };
}
