import './App.css'
import Map from './components/map.jsx'
import { Routes, Route, Link } from 'react-router-dom'
import DocumentUpload from './components/DocumentUpload.jsx'

/* Pin + label colors: forest, maroon, water, gold, sage tones — safari map palette */
const CITY_MARKERS = [
  { name: 'Kampala', x: 540, y: 700, size: 50, pinColor: '#8b4545' },
  { name: 'Entebbe', x: 480, y: 770, size: 45, pinColor: '#5a8fb2' },
  { name: 'Jinja', x: 550, y: 500, size: 55, pinColor: '#3d5238' },
  { name: 'Murchison Falls National Park', x: 500, y: 350, size: 45, pinColor: '#6b8e5e' },
  { name: 'Bwindi Forest', x: 25, y: 965, size: 45, pinColor: '#2d4a2a' },
  { name: 'Mbarara', x: 250, y: 830, size: 45, pinColor: '#c49133' },
  { name: 'Queen Elizabeth National Park', x: 330, y: 700, size: 45, pinColor: '#8db67d' },
  { name: 'Gulu', x: 400, y: 280, size: 45, pinColor: '#5a7d8f' },
  { name: 'Kidepo Valley National Park', x: 650, y: 175, size: 45, pinColor: '#8b4545' },
  { name: 'Kibale National Park', x: 450, y: 650, size: 45, pinColor: '#3d5238' },
  { name: 'Rwenzori Mountains', x: 320, y: 530, size: 45, pinColor: '#5a8fb2' },
  { name: 'Lake Bunyonyi', x: 200, y: 935, size: 45, pinColor: '#6b8e5e' },
  { name: 'Sipi Falls', x: 680, y: 425, size: 45, pinColor: '#c49133' },
  { name: 'Lake Mburo National Park', x: 385, y: 860, size: 45, pinColor: '#8db67d' },
  { name: 'Kabale', x: 95, y: 990, size: 45, pinColor: '#8b4545' },
]

function App() {
  return (
    <div className="app-shell">
      <nav
        className="theme-nav fixed top-4 left-1/2 z-50 flex -translate-x-1/2 gap-1 px-2 py-2 sm:left-auto sm:right-6 sm:translate-x-0"
        aria-label="Main"
      >
        <Link to="/" className="theme-nav-link px-4 py-2 no-underline">
          Map
        </Link>
        <Link to="/upload" className="theme-nav-link px-4 py-2 no-underline">
          Contribute!
        </Link>
      </nav>

      <main className="app-main">
        <Routes>
          <Route
            path="/"
            element={
              <Map
                mapSrc="https://static.vecteezy.com/system/resources/thumbnails/017/745/284/small/doodle-freehand-drawing-of-uganda-map-free-png.png"
                originalWidth={1000}
                originalHeight={1000}
                cities={CITY_MARKERS}
              />
            }
          />
          <Route path="/upload" element={<DocumentUpload />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
