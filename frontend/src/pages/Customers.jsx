import { useEffect, useState } from "react";

import {
  getCustomers,
  createCustomer,
} from "../services/customerService";

function Customers() {
  const [customers, setCustomers] = useState([]);

  const [form, setForm] = useState({
    name: "",
    email: "",
  });

  const fetchCustomers = async () => {
    const res = await getCustomers();
    setCustomers(res.data);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    await createCustomer(form);

    fetchCustomers();

    setForm({
      name: "",
      email: "",
    });
  };

  return (
    <div>
      <h2>Customers</h2>

      <form onSubmit={handleSubmit}>
        <input
          placeholder="Name"
          value={form.name}
          onChange={(e) =>
            setForm({
              ...form,
              name: e.target.value,
            })
          }
        />

        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) =>
            setForm({
              ...form,
              email: e.target.value,
            })
          }
        />

        <button>Add Customer</button>
      </form>

      <hr />

      {customers.map((customer) => (
        <div key={customer.id}>
          {customer.name}
          {" | "}
          {customer.email}
        </div>
      ))}
    </div>
  );
}

export default Customers;