import { useState, useEffect, Suspense } from "react";
import "./StockContainer.css";
import React from "react";

interface Props {
  ticker: string;
}

const StockContainer: React.FC<Props> = ({ ticker }) => {
  const hostname = "http://192.168.2.210:5000";
  const url = `${hostname}/predict/${ticker}`;
  const [price, setPrice] = useState<number>(0);

  useEffect(() => {
    async function getData() {
      const headers = {
        "Content-Type": "application/json",
        Accept: "application/json",
      };
      const result = await fetch(url, { headers });
      console.log(result.body);
      const json = await result.json();
      const fname = json["name"];
      const fprice = json["price"];
      setPrice(fprice);
    }
    getData();
  }, []);

  return (
    <div className="stock-container">
      <h2 className="stock-name">{ticker}</h2>
      <Suspense fallback={"Loading..."}>
        <h3 className="stock-info">Yesterdays Close Price: 146.50</h3>
        <h3 className="stock-price">{price}</h3>
      </Suspense>
    </div>
  );
};

export default StockContainer;
