import { Gender } from '../types/fashion';

interface GenderSelectorProps {
  selected: Gender;
  onChange: (gender: Gender) => void;
}

export function GenderSelector({ selected, onChange }: GenderSelectorProps) {
  const options: { value: Gender; label: string; emoji: string }[] = [
    { value: 'male', label: 'Male', emoji: '👨' },
    { value: 'female', label: 'Female', emoji: '👩' },
    { value: 'unisex', label: 'Unisex', emoji: '🧑' },
  ];

  return (
    <div>
      <label className="block text-sm font-semibold text-gray-700 mb-3">
        Gender <span className="text-red-500">*</span>
      </label>
      <div className="grid grid-cols-3 gap-3">
        {options.map((option) => (
          <button
            key={option.value}
            onClick={() => onChange(option.value)}
            className={`px-4 py-3 rounded-lg border-2 transition-all font-medium ${
              selected === option.value
                ? 'border-blue-500 bg-blue-50 text-blue-700 shadow-md'
                : 'border-gray-200 bg-white text-gray-700 hover:border-blue-300 hover:bg-blue-50'
            }`}
          >
            <div className="text-2xl mb-1">{option.emoji}</div>
            <div className="text-sm">{option.label}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
