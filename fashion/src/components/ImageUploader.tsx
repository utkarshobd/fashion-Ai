import { Upload, X } from 'lucide-react';
import { useRef, useState } from 'react';

interface ImageUploaderProps {
  onImageSelect: (file: File) => void;
  previewUrl: string | null;
  onClear: () => void;
}

export function ImageUploader({ onImageSelect, previewUrl, onClear }: ImageUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onImageSelect(file);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  if (previewUrl) {
    return (
      <div className="relative">
        <img
          src={previewUrl}
          alt="Uploaded clothing"
          className="w-full h-64 object-cover rounded-lg shadow-lg"
        />
        <button
          onClick={onClear}
          className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full hover:bg-red-600 transition-colors shadow-lg"
        >
          <X size={20} />
        </button>
      </div>
    );
  }

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={handleClick}
      className={`border-3 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all ${
        isDragging
          ? 'border-blue-500 bg-blue-50 scale-105'
          : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
      }`}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="hidden"
      />
      <Upload className="mx-auto mb-4 text-gray-400" size={48} />
      <p className="text-lg font-medium text-gray-700 mb-2">
        Upload Your Clothing Image
      </p>
      <p className="text-sm text-gray-500">
        Drag and drop or click to browse
      </p>
      <p className="text-xs text-gray-400 mt-2">
        Supports: JPG, PNG, WEBP
      </p>
    </div>
  );
}
