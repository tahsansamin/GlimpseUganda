import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import apiClient from './api';
import CityMarker from './components/citymarker';
import Map from './components/map.jsx';


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
    <>
      
      
      
      <Map 
  mapSrc="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/World_map_-_low_resolution.svg/960px-World_map_-_low_resolution.svg.png" 
  originalWidth={640} 
  originalHeight={418}
  cities={[
    { name: "New York", x: 150, y: 150, size: 50, pinColor: "#dc3545" },
    { name: "London", x: 320, y: 120, size: 60, pinColor: "#0d6efd" },
    { name: "Tokyo", x: 550, y: 160, size: 55, pinColor: "#198754" },
  ]}
/>
      
    </>
  )
}

export default App
