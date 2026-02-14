import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import apiClient from './api';
import CityMarker from './components/citymarker';
import Map from './components/map.jsx';
import InputBox from './components/inputbox.jsx';



function App() {
  const [count, setCount] = useState(0)
  const fetchData = async () => {
        try {
            const response = await apiClient.post('/prompts',
              { prompt: "what are the namugongo shrines?" } 
            );
            console.log(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

  return (
    <div className="App" style={{ padding: '20px' ,width: '100%' , height: '100%' }}>
        
      
      
      <Map 
  mapSrc="https://static.vecteezy.com/system/resources/thumbnails/017/745/284/small/doodle-freehand-drawing-of-uganda-map-free-png.png" 
  originalWidth={1000} 
  originalHeight={1000} 
  cities={[
    { name: "Kampala", x: 470, y: 850, size: 50, pinColor: "#dc3545" },
    { name: "Entebbe", x: 300, y: 1000, size: 60, pinColor: "#0d6efd" },
    { name: "Jinja", x: 550, y: 500, size: 55, pinColor: "#198754" },
  ]}
      />
    
      

    </div>
    
  )
}

export default App
