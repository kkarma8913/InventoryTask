import { useState } from "react";
import { createOrder } from "../services/orderService";

function Orders() {
  const [customerId, setCustomerId] =
    useState("");

  const [productId, setProductId] =
    useState("");

  const [quantity, setQuantity] =
    useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    await createOrder({
      customer_id: Number(customerId),
      items: [
        {
          product_id: Number(productId),
          quantity: Number(quantity),
        },
      ],
    });

    alert("Order Created");
  };

  return (
    <div>
      <h2>Create Order</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Customer ID"
          value={customerId}
          onChange={(e) =>
            setCustomerId(e.target.value)
          }
        />

        <input
          placeholder="Product ID"
          value={productId}
          onChange={(e) =>
            setProductId(e.target.value)
          }
        />

        <input
          placeholder="Quantity"
          value={quantity}
          onChange={(e) =>
            setQuantity(e.target.value)
          }
        />

        <button>Create Order</button>
      </form>
    </div>
  );
}

export default Orders;