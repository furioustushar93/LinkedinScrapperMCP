# LinkedIn Scraper AI - Frontend

React 18 + Vite frontend for the LinkedIn Scraper AI chatbot.

## 🛠️ Tech Stack

- **React 18** - UI library with hooks
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization (ready for analytics)
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons

## 🚀 Quick Start

### Install Dependencies
```bash
npm install
```

### Development
```bash
npm run dev
```

Opens at: http://localhost:3000

### Build for Production
```bash
npm run build
```

Output: `dist/` directory

### Preview Production Build
```bash
npm run preview
```

## 📁 Project Structure

```
src/
├── components/           # React components
│   ├── Header.jsx       # Top navigation
│   ├── Sidebar.jsx      # Left sidebar
│   ├── ChatMessage.jsx  # Message component
│   ├── ChatInput.jsx    # Input area
│   └── WelcomeScreen.jsx # Welcome screen
├── App.jsx              # Main app
├── main.jsx             # Entry point
└── index.css            # Tailwind styles

public/                  # Static assets
├── vite.svg

index.html              # HTML template
vite.config.js          # Vite config
tailwind.config.js      # Tailwind config
postcss.config.js       # PostCSS config
```

## 🎨 Customization

### Colors
Edit `tailwind.config.js`:
```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your color palette
      }
    }
  }
}
```

### Components
All components are in `src/components/`. Each is fully customizable.

### Styling
Uses Tailwind CSS. Edit classes in JSX files directly.

## 🔌 API Integration

Backend URL configured in `vite.config.js`:
```js
server: {
  proxy: {
    '/api': 'http://localhost:8000',
    '/ws': {
      target: 'ws://localhost:8000',
      ws: true
    }
  }
}
```

## 📦 Dependencies

### Production
- `react`: ^18.3.1
- `react-dom`: ^18.3.1
- `axios`: ^1.6.2
- `recharts`: ^2.10.3

### Development
- `@vitejs/plugin-react`: ^4.3.0
- `tailwindcss`: ^3.4.0
- `vite`: ^5.1.0

## 🎯 Features

- **Real-time Chat**: WebSocket connection
- **Beautiful UI**: Modern, responsive design
- **Job Cards**: Rich job listing display
- **Profile Cards**: Professional profile cards
- **Company Info**: Detailed company cards
- **Context Aware**: Follow-up questions supported
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages

## 🐛 Debugging

### Browser Console
```javascript
// Check WebSocket connection
console.log('WebSocket status:', ws.readyState);

// Check state
console.log('Messages:', messages);
```

### React DevTools
Install React DevTools browser extension for component inspection.

## 📱 Responsive Design

Fully responsive using Tailwind's breakpoints:
- Mobile: `<768px`
- Tablet: `768px - 1024px`
- Desktop: `>1024px`

## ♿ Accessibility

- Semantic HTML
- ARIA labels
- Keyboard navigation
- Screen reader friendly

## 🚀 Performance

- Code splitting with React lazy loading
- Vite's fast HMR
- Optimized production builds
- Tree shaking enabled

## 📄 License

MIT License - See LICENSE file

