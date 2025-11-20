import { useState, useEffect } from 'react'
import { getAllCoins } from '../services/api'

function CoinsList() {
    const [allCoins, setAllCoins] = useState([])  // All coins for filtering
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [page, setPage] = useState(1)
    const [pageSize, setPageSize] = useState(25)   // default
    const [searchTerm, setSearchTerm] = useState('')
    const [filterCountry, setFilterCountry] = useState('')
    const [filterCondition, setFilterCondition] = useState('')

    // Fetch all coins once when component loads
    useEffect(() => {
        const fetchCoins = async () => {
            try {
                setLoading(true)
                const coins = await getAllCoins()  // Fetch ALL coins
                setAllCoins(coins)
                setError(null)
            } catch (err) {
                setError('Failed to load coins')
                console.error(err)
            } finally {
                setLoading(false)
            }
        }

        fetchCoins()
    }, [])  // Only run once on mount

    // Filter all coins based on search and filters
    const filteredCoins = allCoins.filter(coin => {
        // Search filter - check multiple fields
        const matchesSearch = searchTerm === '' ||
            coin.coin_type_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            coin.year?.toString().includes(searchTerm) ||
            coin.denomination?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            coin.country_name?.toLowerCase().includes(searchTerm.toLowerCase())

        // Country filter
        const matchesCountry = filterCountry === '' || coin.country_name === filterCountry

        // Condition filter
        const matchesCondition = filterCondition === '' || coin.condition_name === filterCondition

        return matchesSearch && matchesCountry && matchesCondition
    })

    // Paginate the filtered results
    const startIndex = (page - 1) * pageSize
    const endIndex = startIndex + pageSize
    const paginatedCoins = filteredCoins.slice(startIndex, endIndex)
    const totalFilteredCount = filteredCoins.length

    // Reset to page 1 when filters change
    useEffect(() => {
        setPage(1)
    }, [searchTerm, filterCountry, filterCondition])

    return (
        <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
            <h1>My Coin Collection</h1>

            {/* Search and Filter Section */}
            {!loading && !error && allCoins.length > 0 && (
                <div style={{ marginBottom: '2rem', padding: '1rem', color: '#333', backgroundColor: '#f9f9f9', borderRadius: '8px' }}>
                    <div style={{ marginBottom: '1rem' }}>
                        <label style={{ textAlign: 'left', display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                            Search:
                        </label>
                        <input
                            type="text"
                            placeholder="Search by coin type, year, denomination, or country..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            style={{
                                width: '100%',
                                padding: '0.5rem',
                                fontSize: '1rem',
                                border: '1px solid #ccc',
                                borderRadius: '4px'
                            }}
                        />
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label style={{ textAlign: 'left', display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                                Filter by Country:
                            </label>
                            <select
                                value={filterCountry}
                                onChange={(e) => setFilterCountry(e.target.value)}
                                style={{
                                    width: '100%',
                                    padding: '0.5rem',
                                    fontSize: '1rem',
                                    border: '1px solid #ccc',
                                    borderRadius: '4px'
                                }}
                            >
                                <option value="">All Countries</option>
                                {[...new Set(allCoins.map(coin => coin.country_name))].sort().map(country => (
                                    <option key={country} value={country}>{country}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label style={{ textAlign: 'left', display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                                Filter by Condition:
                            </label>
                            <select
                                value={filterCondition}
                                onChange={(e) => setFilterCondition(e.target.value)}
                                style={{
                                    width: '100%',
                                    padding: '0.5rem',
                                    fontSize: '1rem',
                                    border: '1px solid #ccc',
                                    borderRadius: '4px'
                                }}
                            >
                                <option value="">All Conditions</option>
                                {Array.from(
                                    new Map(
                                        allCoins.map(coin => [coin.condition, { id: coin.condition, name: coin.condition_name }])
                                    ).values()
                                )
                                    .sort((a, b) => a.id - b.id)
                                    .map(condition => (
                                        <option key={condition.id} value={condition.name}>{condition.name}</option>
                                    ))}
                            </select>
                        </div>
                    </div>

                    {filteredCoins.length !== allCoins.length && (
                        <div style={{ marginTop: '1rem', color: '#666' }}>
                            Showing {filteredCoins.length} of {allCoins.length} coins
                        </div>
                    )}
                </div>
            )}

            {/* Pagination Controls */}
            {!loading && !error && filteredCoins.length > 0 && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', margin: '1rem 0' }}>
                    <div>
                        <label style={{ marginRight: '0.5rem' }}>Rows per page:</label>
                        <select
                            value={pageSize}
                            onChange={(e) => { setPage(1); setPageSize(Number(e.target.value)) }}
                        >
                            <option value={5}>5</option>
                            <option value={10}>10</option>
                            <option value={25}>25</option>
                            <option value={50}>50</option>
                            <option value={100}>100</option>
                            <option value={filteredCoins.length}>ALL ({filteredCoins.length})</option>
                        </select>
                    </div>

                    <div style={{ marginLeft: 'auto' }}>
                        <button
                            onClick={() => setPage((p) => Math.max(1, p - 1))}
                            disabled={page === 1}
                            style={{ marginRight: '0.5rem' }}
                        >
                            Prev
                        </button>
                        <button
                            onClick={() => {
                                const maxPage = Math.max(1, Math.ceil(totalFilteredCount / pageSize))
                                setPage((p) => Math.min(maxPage, p + 1))
                            }}
                            disabled={page >= Math.ceil(totalFilteredCount / pageSize)}
                        >
                            Next
                        </button>
                        <span style={{ marginLeft: '0.75rem' }}>
                            Page {page} of {Math.max(1, Math.ceil(totalFilteredCount / pageSize))}
                            ({totalFilteredCount} {totalFilteredCount === 1 ? 'coin' : 'coins'})
                        </span>
                    </div>
                </div>
            )}

            {loading && <p>Loading coins...</p>}

            {error && <p style={{ color: 'red' }}>Error: {error}</p>}

            {!loading && !error && (
                <div>
                    {allCoins.length === 0 ? (
                        <p>No coins in your collection yet.</p>
                    ) : filteredCoins.length === 0 ? (
                        <p>No coins match your search/filter criteria.</p>
                    ) : (
                        <div style={{
                            display: 'grid',
                            gridTemplateColumns: '1fr 2fr 0.8fr 1.2fr 1fr 1.2fr 0.8fr 1.2fr',
                            gap: '0.5rem',
                            marginTop: '1rem'
                        }}>

                            {/* Header Row */}
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Ref #</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Coin Type</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Year</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Country</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Denomination</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Condition</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Qty</div>
                            <div style={{ fontWeight: 'bold', padding: '0.75rem', color: '#333', backgroundColor: '#f4f4f4', borderBottom: '2px solid #333' }}>Est. Value</div>

                            {/* Data Rows - Display paginated filtered coins */}
                            {paginatedCoins.map(coin => (
                                <>
                                    <div key={`${coin.id}-reference_number`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.reference_number}</div>
                                    <div key={`${coin.id}-type`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.coin_type_name}</div>
                                    <div key={`${coin.id}-year`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.year}</div>
                                    <div key={`${coin.id}-country`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.country_name}</div>
                                    <div key={`${coin.id}-denomination`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.denomination}</div>
                                    <div key={`${coin.id}-condition`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.condition_name}</div>
                                    <div key={`${coin.id}-quantity`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd' }}>{coin.quantity}</div>
                                    <div key={`${coin.id}-value`} style={{ padding: '0.75rem', borderBottom: '1px solid #ddd', textAlign: 'right' }}>
                                        ${coin.value_estimate ? parseFloat(coin.value_estimate).toFixed(2) : '0.00'}
                                    </div>
                                </>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default CoinsList

