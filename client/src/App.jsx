import axios from "axios";
import { useState } from "react";

function StockForm() {
  const [stockCode, setStockCode] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(stockCode);

    try {
      const response = await axios.post(
        "http://localhost:3001/submit_stock_code",
        { stockCode } // Send as an object
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <h1>Enter Stock Code</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="stockCode">Stock Code:</label>
        <input
          type="text"
          id="stockCode"
          value={stockCode}
          onChange={(e) => setStockCode(e.target.value)}
          required
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default StockForm;
