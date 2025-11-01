# Fashion Recommendation App

A React-based fashion recommendation application that uses AI to suggest clothing combinations.

## Quick Setup

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Supabase CLI (optional for local development)

### Installation & Running

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

The app will run on `http://localhost:5173`

## Supabase Setup (Optional)

If you want to use the full Supabase functionality:

1. **Install Supabase CLI:**
   ```bash
   npm install -g supabase
   ```

2. **Start Supabase locally:**
   ```bash
   npm run supabase:start
   ```

3. **Deploy the function:**
   ```bash
   npm run supabase:deploy
   ```

## Troubleshooting

### "Failed to fetch" Error
The app includes a fallback system that provides local recommendations when the Supabase function is unavailable. This ensures the app works even without a backend connection.

### Environment Variables
Make sure your `.env` file contains:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run supabase:start` - Start local Supabase
- `npm run supabase:stop` - Stop local Supabase
- `npm run supabase:deploy` - Deploy functions to Supabase

## Features

- Image upload and analysis
- Gender-specific recommendations
- Category selection (tops, bottoms, shoes, accessories)
- Fallback recommendations when offline
- Responsive design with Tailwind CSS