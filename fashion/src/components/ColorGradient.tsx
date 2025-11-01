import React from 'react';

interface ColorGradientProps {
  color: string;
}

export function ColorGradient({ color }: ColorGradientProps) {
  // Function to convert RGB to HSL
  const rgbToHsl = (r: number, g: number, b: number) => {
    r /= 255;
    g /= 255;
    b /= 255;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h = 0, s, l = (max + min) / 2;

    if (max === min) {
      h = s = 0;
    } else {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = (g - b) / d + (g < b ? 6 : 0); break;
        case g: h = (b - r) / d + 2; break;
        case b: h = (r - g) / d + 4; break;
      }
      h /= 6;
    }
    return { h: h * 360, s: s * 100, l: l * 100 };
  };

  // Function to convert hex to RGB
  const hexToRgb = (hex: string) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
      r: parseInt(result[1], 16),
      g: parseInt(result[2], 16),
      b: parseInt(result[3], 16)
    } : null;
  };

  // Function to convert color names to hex codes
  const getColorHex = (colorName: string): string => {
    const colorMap: { [key: string]: string } = {
      // Basic Colors
      red: '#FF0000',
      blue: '#0000FF',
      green: '#008000',
      yellow: '#FFFF00',
      purple: '#800080',
      pink: '#FFC0CB',
      orange: '#FFA500',
      brown: '#A52A2A',
      black: '#000000',
      white: '#FFFFFF',
      gray: '#808080',
      navy: '#000080',
      
      // Fashion-specific Colors
      burgundy: '#800020',
      mauve: '#E0B0FF',
      rust: '#B7410E',
      sage: '#BCB88A',
      taupe: '#483C32',
      ivory: '#FFFFF0',
      cream: '#FFFDD0',
      khaki: '#C3B091',
      charcoal: '#36454F',
      maroon: '#800000',
      olive: '#808000',
      teal: '#008080',
      violet: '#EE82EE',
      indigo: '#4B0082',
      turquoise: '#40E0D0',
      beige: '#F5F5DC',
      coral: '#FF7F50',
      crimson: '#DC143C',
      gold: '#FFD700',
      lavender: '#E6E6FA',
      magenta: '#FF00FF',
      salmon: '#FA8072',
      tan: '#D2B48C',
      plum: '#DDA0DD',
      slate: '#708090',
      
      // Color variations
      'light blue': '#ADD8E6',
      'dark blue': '#00008B',
      'navy blue': '#000080',
      'royal blue': '#4169E1',
      'sky blue': '#87CEEB',
      'light green': '#90EE90',
      'dark green': '#006400',
      'forest green': '#228B22',
      'mint green': '#98FF98',
      'olive green': '#556B2F',
      'light pink': '#FFB6C1',
      'hot pink': '#FF69B4',
      'deep pink': '#FF1493',
      'light brown': '#B5651D',
      'dark brown': '#5C4033',
      'chocolate brown': '#7B3F00',
      'golden brown': '#996515',
      'light gray': '#D3D3D3',
      'dark gray': '#A9A9A9',
      'charcoal gray': '#36454F',
    };

    return colorMap[colorName.toLowerCase()] || colorName;
  };

  const hexColor = getColorHex(color);
  const rgb = hexToRgb(hexColor);
  
  if (!rgb) {
    return null;
  }

  const hsl = rgbToHsl(rgb.r, rgb.g, rgb.b);
  
  // Generate lighter and darker versions by adjusting lightness
  const lighterColor = `hsl(${hsl.h}, ${hsl.s}%, ${Math.min(hsl.l + 30, 100)}%)`;
  const darkerColor = `hsl(${hsl.h}, ${hsl.s}%, ${Math.max(hsl.l - 30, 0)}%)`;

  return (
    <div className="color-gradient-container">
      <div
        className="h-8 w-full rounded-lg shadow-inner"
        style={{
          background: `linear-gradient(to right, ${lighterColor}, ${hexColor}, ${darkerColor})`,
        }}
      />
      <p className="text-xs text-center mt-1 text-gray-600">{color}</p>
    </div>
  );
}