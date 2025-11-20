import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import Home from './pages/Home'
import CoinsList from './pages/CoinsList'
import AddCoin from './pages/AddCoin'
import './App.css'

function App() {
    return (
        <BrowserRouter>
            <Navigation />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/coins" element={<CoinsList />} />
                <Route path="/coins/add" element={<AddCoin />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
