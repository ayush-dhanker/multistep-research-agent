export default function ResultCard({ result }) {
    return (
        <div className="result-card">

            <div className="meta-row">
                <span className="badge">Score: {result.quality_score}</span>
                <span className="badge">Iterations: {result.iteration_count}</span>
            </div>

            <h2>Summary</h2>
            <p className="output">{result.output}</p>

            <h3>Sub-queries searched</h3>
            <ul>
                {result.steps.map((step, i) => (
                    <li key={i}>{step}</li>
                ))}
            </ul>

        </div>
    )
}