import { Sparkles, ShoppingBag, Info } from 'lucide-react';
import { FashionRecommendation } from '../types/fashion';
import { ColorGradient } from './ColorGradient';

interface RecommendationDisplayProps {
  recommendation: FashionRecommendation;
}

export function RecommendationDisplay({ recommendation }: RecommendationDisplayProps) {
  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-[#800020] to-[#4A0012] text-white p-6 rounded-xl shadow-lg">
        <div className="flex items-center gap-3 mb-3">
          <Sparkles size={28} className="text-[#FFD700]" />
          <h2 className="text-2xl font-bold">Your Style Recommendations</h2>
        </div>
        <p className="text-[#FFE4E1]">{recommendation.analysis}</p>
      </div>

      <div className="grid gap-6">
        {recommendation.recommendations.map((category, idx) => (
          <div key={idx} className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b">
              <h3 className="text-xl font-bold text-gray-800 capitalize flex items-center gap-2">
                <ShoppingBag size={22} className="text-[#800020]" />
                {category.category}
              </h3>
            </div>
            <div className="p-6 space-y-4">
              {category.items.map((item, itemIdx) => (
                <div
                  key={itemIdx}
                  className="p-4 bg-gray-50 rounded-lg border border-gray-200 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h4 className="font-bold text-lg text-gray-800">{item.name}</h4>
                      <div className="flex gap-3 mt-1">
                        <div className="flex flex-col gap-2">
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-[#FFF0F5] text-[#800020]">
                            {item.color}
                          </span>
                          <div className="w-32">
                            <ColorGradient color={item.color} />
                          </div>
                        </div>
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-[#F0FFF0] text-[#2E8B57]">
                          {item.style}
                        </span>
                      </div>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-2">{item.description}</p>
                  <div className="flex items-start gap-2 mt-3 p-3 bg-blue-50 rounded-lg">
                    <Info size={16} className="text-blue-600 mt-0.5 flex-shrink-0" />
                    <p className="text-xs text-blue-900">
                      <span className="font-semibold">Why it matches:</span> {item.matchReason}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
