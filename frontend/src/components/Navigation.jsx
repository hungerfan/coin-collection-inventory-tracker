import { Link } from 'react-router-dom'

function Navigation() {
    return (
        <nav style={{
            backgroundColor: '#333',
            padding: '1rem',
            marginBottom: '2rem'
        }}>
            <div style={{
                maxWidth: '1200px',
                margin: '0 auto',
                display: 'flex',
                gap: '2rem',
                alignItems: 'center'
            }}>
                <Link
                    to="/"
                    style={{
                        color: 'white',
                        textDecoration: 'none',
                        fontSize: '1.5rem',
                        fontWeight: 'bold'
                    }}
                >
                    Coin Collection
                </Link>
                <div style={{ display: 'flex', gap: '1.5rem' }}>
                    <Link
                        to="/"
                        style={{ color: 'white', textDecoration: 'none' }}
                    >
                        Home
                    </Link>
                    <Link
                        to="/coins"
                        style={{ color: 'white', textDecoration: 'none' }}
                    >
                        Coins
                    </Link>
                    <Link
                        to="/coins/add"
                        style={{ color: 'white', textDecoration: 'none' }}
                    >
                        Add Coin
                    </Link>
                </div>
            </div>
        </nav>
    )
}

export default Navigation

