import { useState } from 'react';
import { Loader2, Sparkles } from 'lucide-react';
import { ImageUploader } from './components/ImageUploader';
import { ClothingTypeSelector } from './components/ClothingTypeSelector';
import { GenderSelector } from './components/GenderSelector';
import { CategorySelector } from './components/CategorySelector';
import { RecommendationDisplay } from './components/RecommendationDisplay';
import { getRecommendation, imageToBase64 } from './services/fashionApi';
import { ClothingType, Gender, FashionRecommendation } from './types/fashion';

function App() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [clothingType, setClothingType] = useState<ClothingType>('t-shirt');
  const [gender, setGender] = useState<Gender>('male');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [recommendation, setRecommendation] = useState<FashionRecommendation | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = (file: File) => {
    setSelectedImage(file);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setRecommendation(null);
    setError(null);
  };

  const handleClearImage = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setSelectedImage(null);
    setPreviewUrl(null);
    setRecommendation(null);
    setError(null);
  };

  const handleGetRecommendations = async () => {
    if (!selectedImage) {
      setError('Please upload an image first');
      return;
    }

    setLoading(true);
    setError(null);
    setRecommendation(null);

    try {
      const base64 = await imageToBase64(selectedImage);
      const result = await getRecommendation({
        imageBase64: base64,
        itemType: clothingType,
        gender,
        selectedCategories: selectedCategories.length > 0 ? selectedCategories : undefined,
      });

      if (result.success && result.recommendation) {
        setRecommendation(result.recommendation);
      } else {
        setError(result.error || 'Failed to get recommendations. Please try again.');
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <header className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Sparkles className="text-blue-500" size={48} />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              AI Fashion Stylist
            </h1>
          </div>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Upload a photo of your clothing and get personalized style recommendations powered by AI
          </p>
        </header>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Upload Your Clothing</h2>
              <ImageUploader
                onImageSelect={handleImageSelect}
                previewUrl={previewUrl}
                onClear={handleClearImage}
              />
            </div>

            {selectedImage && (
              <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Customize Your Style</h2>

                <GenderSelector selected={gender} onChange={setGender} />

                <ClothingTypeSelector selected={clothingType} onChange={setClothingType} />

                <CategorySelector
                  selected={selectedCategories}
                  onChange={setSelectedCategories}
                />

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    {error}
                  </div>
                )}

                <button
                  onClick={handleGetRecommendations}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-bold py-4 px-6 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl flex items-center justify-center gap-3"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" size={24} />
                      Analyzing Your Style...
                    </>
                  ) : (
                    <>
                      <Sparkles size={24} />
                      Get Fashion Recommendations
                    </>
                  )}
                </button>
              </div>
            )}
          </div>

          <div>
            {loading && (
              <div className="bg-white rounded-xl shadow-lg p-12 text-center">
                <Loader2 className="animate-spin mx-auto mb-4 text-blue-500" size={64} />
                <p className="text-xl font-semibold text-gray-700 mb-2">
                  Analyzing Your Fashion...
                </p>
                <p className="text-gray-500">
                  Our AI is creating personalized style recommendations for you
                </p>
              </div>
            )}

            {!loading && recommendation && (
              <RecommendationDisplay recommendation={recommendation} />
            )}

            {!loading && !recommendation && !selectedImage && (
              <div className="bg-white rounded-xl shadow-lg p-12 text-center">
                <Sparkles className="mx-auto mb-4 text-gray-300" size={64} />
                <p className="text-xl font-semibold text-gray-700 mb-2">
                  Ready to Transform Your Style?
                </p>
                <p className="text-gray-500">
                  Upload a photo of your clothing to get started
                </p>
              </div>
            )}
          </div>
        </div>

        <footer className="text-center text-gray-500 text-sm mt-12 pb-8">
          <p>Powered by AI Vision Technology</p>
          <p className="mt-2">
            Get personalized fashion recommendations based on color theory, current trends, and
            style matching
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
