import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import PlacesPage from './pages/PlacesPage'
import PlaceDetailPage from './pages/PlaceDetailPage'
import AIChatPage from './pages/AIChatPage'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<PlacesPage />} />
        <Route path="/places/:id" element={<PlaceDetailPage />} />
        <Route path="/ai" element={<AIChatPage />} />
      </Routes>
    </Layout>
  )
}
