import { Shirt, Footprints, Package } from 'lucide-react';
import { ClothingType } from '../types/fashion';

interface ClothingTypeSelectorProps {
  selected: ClothingType;
  onChange: (type: ClothingType) => void;
}

const clothingTypes: { value: ClothingType; label: string }[] = [
  { value: 't-shirt', label: 'T-Shirt' },
  { value: 'shirt', label: 'Shirt' },
  { value: 'pants', label: 'Pants' },
  { value: 'jeans', label: 'Jeans' },
  { value: 'shoes', label: 'Shoes' },
  { value: 'jacket', label: 'Jacket' },
  { value: 'dress', label: 'Dress' },
  { value: 'skirt', label: 'Skirt' },
  { value: 'shorts', label: 'Shorts' },
  { value: 'sweater', label: 'Sweater' },
  { value: 'hoodie', label: 'Hoodie' },
  { value: 'other', label: 'Other' },
];

export function ClothingTypeSelector({ selected, onChange }: ClothingTypeSelectorProps) {
  return (
    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-3">
        What type of clothing is this?
      </label>
      <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-2">
        {clothingTypes.map((type) => (
          <button
            key={type.value}
            onClick={() => onChange(type.value)}
            className={`px-3 py-2 rounded-lg border-2 transition-all text-sm font-medium ${
              selected === type.value
                ? 'border-blue-500 bg-blue-50 text-blue-700 shadow-md'
                : 'border-gray-200 bg-white text-gray-700 hover:border-blue-300 hover:bg-blue-50'
            }`}
          >
            {type.label}
          </button>
        ))}
      </div>
    </div>
  );
}
