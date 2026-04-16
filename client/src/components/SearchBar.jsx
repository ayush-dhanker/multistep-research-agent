export default function SearchBar({ topic, setTopic, onSearch, loading }) {
    function handleKeyDown(e) {
        if (e.key === "Enter") onSearch()
    }

    return (
        <div className="search-bar">
            <input
                type="text"
                placeholder="Enter a research topic..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
            />
            <button onClick={onSearch} disabled={loading}>
                {loading ? "Researching..." : "Research"}
            </button>
        </div>
    )
}