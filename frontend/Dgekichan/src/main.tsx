import "@fontsource/inter/index.css";

import "./design/themes/theme.css";
import "./app/styles/global.css";

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
