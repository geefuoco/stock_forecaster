import { useState, useEffect, Suspense } from "react";
import "./StockContainer.css";
import React from "react";

interface Props {
  ticker: string;
}

const StockContainer: React.FC<Props> = ({ ticker }) => {
  const url = `${window.location.hostname}/prediction/${ticker}`;
  const [name, setName] = useState<string>("Loading");
  const [price, setPrice] = useState<number>(0);

  useEffect(() => {
    async function getData() {
      const result = await fetch(url);
      const json = await result.json();
      const fname = json["name"];
      const fprice = json["price"];
      setName(fname);
      setPrice(fprice);
    }
    getData();
  }, []);

  return (
    <div className="stock-container">
      <Suspense fallback={"Loading..."}>
        <h2 className="stock-name">{name}</h2>
        <h3 className="stock-price">{price}</h3>
      </Suspense>
    </div>
  );
};

export default StockContainer;
