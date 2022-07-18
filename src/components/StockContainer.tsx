import { useState, useEffect, Suspense } from "react";
import "./StockContainer.css";
import React from "react";

interface Props {
  ticker: string;
}

const StockContainer: React.FC<Props> = ({ ticker }) => {
  const server_uri = "http://192.168.2.210:5000";
  const url = `${server_uri}/predict/${ticker}`;
  const [price, setPrice] = useState<string>();
  const [date, setDate] = useState<Date>(new Date());

  const today = new Date();
  const marketClose = new Date(today.toLocaleDateString() + " 4:00:00 PM");

  useEffect(() => {
    async function getData() {
      const headers = {
        "Content-Type": "application/json",
        Accept: "application/json",
      };
      const result = await fetch(url, { headers });
      const json = await result.json();
      const fprice = json["price"];
      setPrice(fprice);
    }
    getData();
    if (today.getUTCHours() < marketClose.getUTCHours()) {
      setDate(today);
    } else {
      const tomorrow = new Date(today);
      tomorrow.setDate(today.getDate() + 1);
      if (tomorrow.getDay() == 0) {
        tomorrow.setDate(today.getDate() + 2);
      } else if (tomorrow.getDay() == 6) {
        tomorrow.setDate(today.getDate() + 3);
      }
      setDate(tomorrow);
    }
  }, []);

  return (
    <div className="stock-container">
      <h2 className="stock-name">{ticker}</h2>
      <h3 className="stock-date">Prediction for {date.toLocaleDateString()}</h3>
      <Suspense fallback={"Loading..."}>
        {price ? (
          <span className="stock-price">${price}</span>
        ) : (
          <span className="stock-price">Loading...</span>
        )}
      </Suspense>
    </div>
  );
};

export default StockContainer;
