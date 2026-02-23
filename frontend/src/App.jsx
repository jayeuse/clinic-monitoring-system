import React, {useEffect} from "react";
import api from "./services/api"

const checkHealth = async () => {
  try {
    const response = await api.get("/health");
    console.log("Backend Status: ", response.data);
  } catch (error) {
    console.error("Coonection Failed: ", error);
  }
};

function App() {
  
  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3x1 font-bold">Clinic Monitoring System</h1>
      <p className="mt-4 text-gray-600">Starting fresh UI Implementation</p>
    </div>
  );
}

export default App;
