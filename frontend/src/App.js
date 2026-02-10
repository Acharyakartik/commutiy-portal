import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("https://testapi.devtoolsdaily.com/users")
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <ul>
      {data.map(item => (
        <li key={item.id}>{item.firstName}</li>
      ))}
    </ul>
  );
}

export default App;
