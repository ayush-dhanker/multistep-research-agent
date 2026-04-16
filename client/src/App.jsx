import { useState } from "react"
import SearchBar from "./components/SearchBar"
import ResultCard from "./components/ResultCard"
import Loader from "./components/Loader"
import axios from "axios"
import "./index.css"

export default function App() {
  const [topic, setTopic] = useState("")
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSearch() {
    if (!topic.trim()) return
    setLoading(true)
    setResult(null)
    setError(null)

    try {
      // const response = await axios.post("http://localhost:8000/research", {
      //   topic
      // })
      const response = await axios.post(
        `${import.meta.env.VITE_API_URL}/research`,
        { topic }
      )
      setResult(response.data)
    } catch (err) {
      setError("Something went wrong. Make sure the backend is running.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Research Agent</h1>
      <p className="subtitle">Powered by LangGraph — searches, evaluates, refines.</p>

      <SearchBar
        topic={topic}
        setTopic={setTopic}
        onSearch={handleSearch}
        loading={loading}
      />

      {error && <p className="error">{error}</p>}
      {loading && <Loader />}
      {result && <ResultCard result={result} />}
    </div>
  )
}