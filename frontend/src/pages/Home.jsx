import { useState, useEffect } from 'react'
import { getStats } from '../services/api'

function Home() {
    const [stats, setStats] = useState(null)  // Stats is an object, not an array
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        // This function runs when the component first loads
        const fetchStats = async () => {
            try {
                setLoading(true)  // Start loading
                const data = await getStats()  // Fetch coin stats from API
                // Stats endpoint returns an object directly (not paginated)
                setStats(data)  // Store the stats in state
                setError(null)  // Clear any previous errors
            } catch (err) {
                setError('Failed to load coin stats')  // Set error message
                console.error(err)
            } finally {
                setLoading(false)  // Stop loading (runs whether success or error)
            }
        }

        fetchStats()  // Call the function
    }, [])  // Empty array means "run once when component loads"

    return (
        <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
            <h1>Welcome to Coin Collection Tracker</h1>
            <p>Manage and track your coin collection with ease.</p>

            {loading && <p>Loading coins...</p>}

            {error && <p style={{ color: 'red' }}>Error: {error}</p>}

            {!loading && !error && stats && (
                <div style={{ marginTop: '2rem' }}>
                    <h2>Your Current Collection Statistics</h2>
                    <div style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                        gap: '1rem',
                        marginTop: '1rem'
                    }}>
                        <div style={{ padding: '1rem', color: '#333', backgroundColor: '#f4f4f4', borderRadius: '8px' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_coins}</div>
                            <div>Coin Records</div>
                        </div>
                        <div style={{ padding: '1rem', color: '#333', backgroundColor: '#f4f4f4', borderRadius: '8px' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_quantity}</div>
                            <div>Total Quantity</div>
                        </div>
                        <div style={{ padding: '1rem', color: '#333', backgroundColor: '#f4f4f4', borderRadius: '8px' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                                ${stats.total_estimated_value ? parseFloat(stats.total_estimated_value).toFixed(2) : '0.00'}
                            </div>
                            <div>Est. Value</div>
                        </div>
                        <div style={{ padding: '1rem', color: '#333', backgroundColor: '#f4f4f4', borderRadius: '8px' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.coin_types_count}</div>
                            <div>Coin Types</div>
                        </div>
                        <div style={{ padding: '1rem', color: '#333', backgroundColor: '#f4f4f4', borderRadius: '8px' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.countries_count}</div>
                            <div>Countries</div>
                        </div>
                        <div style={{ padding: '1rem', color: '#333', backgroundColor: '#f4f4f4', borderRadius: '8px' }}>
                            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.conditions_count}</div>
                            <div>Conditions</div>
                        </div>
                    </div>
                </div>
            )}

        </div>
    )
}

export default Home

