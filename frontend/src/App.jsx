import { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(console.error);
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>AI Compliance Assistant</h1>
      <h2>{message}</h2>
    </div>
  );
}

export default App;