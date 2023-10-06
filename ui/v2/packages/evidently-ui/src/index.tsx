import { useState } from 'react'

export function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Evidently UI Package</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>count is {count}</button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">Click on the Vite and React logos to learn more</p>
    </>
  )
}
