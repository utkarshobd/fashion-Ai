import { Shirt, Footprints, Glasses, PackageCheck } from 'lucide-react';

interface CategorySelectorProps {
  selected: string[];
  onChange: (categories: string[]) => void;
}

const categories = [
  { value: 'tops', label: 'Tops', icon: Shirt, description: 'Shirts, T-shirts, Jackets' },
  { value: 'bottoms', label: 'Bottoms', icon: PackageCheck, description: 'Pants, Jeans, Skirts' },
  { value: 'shoes', label: 'Shoes', icon: Footprints, description: 'Sneakers, Boots, Heels' },
  { value: 'accessories', label: 'Accessories', icon: Glasses, description: 'Caps, Jewelry, Bags' },
];

export function CategorySelector({ selected, onChange }: CategorySelectorProps) {
  const toggleCategory = (category: string) => {
    if (selected.includes(category)) {
      onChange(selected.filter((c) => c !== category));
    } else {
      onChange([...selected, category]);
    }
  };

  const selectAll = () => {
    onChange(categories.map((c) => c.value));
  };

  const clearAll = () => {
    onChange([]);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <label className="block text-sm font-semibold text-gray-700">
          What do you want recommendations for?
        </label>
        <div className="flex gap-2">
          <button
            onClick={selectAll}
            className="text-xs text-blue-600 hover:text-blue-700 font-medium"
          >
            Select All
          </button>
          <span className="text-gray-300">|</span>
          <button
            onClick={clearAll}
            className="text-xs text-gray-600 hover:text-gray-700 font-medium"
          >
            Clear
          </button>
        </div>
      </div>
      <p className="text-xs text-gray-500 mb-3">
        Leave empty for complete outfit recommendations
      </p>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {categories.map((category) => {
          const Icon = category.icon;
          const isSelected = selected.includes(category.value);
          return (
            <button
              key={category.value}
              onClick={() => toggleCategory(category.value)}
              className={`p-4 rounded-lg border-2 transition-all text-left ${
                isSelected
                  ? 'border-blue-500 bg-blue-50 shadow-md'
                  : 'border-gray-200 bg-white hover:border-blue-300 hover:bg-blue-50'
              }`}
            >
              <Icon
                className={`mb-2 ${isSelected ? 'text-blue-600' : 'text-gray-400'}`}
                size={24}
              />
              <div className={`font-medium text-sm ${isSelected ? 'text-blue-700' : 'text-gray-700'}`}>
                {category.label}
              </div>
              <div className="text-xs text-gray-500 mt-1">{category.description}</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
