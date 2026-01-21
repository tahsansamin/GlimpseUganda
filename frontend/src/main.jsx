import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import AnimatedText from './components/animatedtext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <AnimatedText 
      text="Welcome to the Animated Text Demo!" 
      animationType="letter" 
      delay={100} 
      className="mt-4 text-lg font-mono text-center" 
    />
    
  </StrictMode>,
)
