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
    { name: "Kampala", x: 485, y: 850, size: 50, pinColor: "#dc3545" },
    { name: "Entebbe", x: 330, y: 900, size: 45, pinColor: "#0d6efd" },
    { name: "Jinja", x: 550, y: 500, size: 55, pinColor: "#198754" },
    { name: "Murchison Falls National Park", x: 500, y: 350, size: 45 },
    { name: "Bwindi Forest", x: 200, y: 965, size: 45 },
    { name: "Mbarara", x: 250, y: 830, size: 45 },
    { name: "Queen Elizabeth National Park", x: 330, y: 720, size: 45 },
    { name: "Gulu", x: 470, y: 280, size: 45 },
    { name: "Kidepo Valley National Park", x: 650, y: 175, size: 45 },
    { name: "Kibale National Park", x: 400, y: 650, size: 45 },
    { name: "Rwenzori Mountains", x: 320, y: 590, size: 45 },
    { name: "Lake Bunyonyi", x: 230, y: 950, size: 45 },
    { name: "Sipi Falls", x: 680, y: 425, size: 45 },
    { name: "Lake Mburo National Park", x: 350, y: 840, size: 45 },
    { name: "Kabale", x: 250, y: 970, size: 45 }
  ]}
      />
    
      

    </div>
    
  )
}

export default App
