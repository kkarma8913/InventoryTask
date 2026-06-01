import { useEffect, useState } from "react";
import {
  getProducts,
  createProduct,
  deleteProduct,
} from "../services/productService";

function Products() {
  const [products, setProducts] = useState([]);

  const [form, setForm] = useState({
    name: "",
    sku: "",
    price: "",
    stock: "",
  });

  const fetchProducts = async () => {
    const res = await getProducts();
    setProducts(res.data);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    await createProduct({
      ...form,
      price: Number(form.price),
      stock: Number(form.stock),
    });

    setForm({
      name: "",
      sku: "",
      price: "",
      stock: "",
    });

    fetchProducts();
  };

  const handleDelete = async (id) => {
  try {
    await deleteProduct(id);

    fetchProducts();

    alert("Product deleted successfully");
  } catch (error) {
    alert(
      error.response?.data?.detail ||
      "Unable to delete product"
    );
  }
};

  return (
    <div className="container mt-4">

      <div className="card shadow">

        <div className="card-header bg-primary text-white">
          Product Management
        </div>

        <div className="card-body">

          <form className="row g-3" onSubmit={handleSubmit}>

            <div className="col-md-3">
              <input
                className="form-control"
                placeholder="Product Name"
                value={form.name}
                onChange={(e) =>
                  setForm({
                    ...form,
                    name: e.target.value,
                  })
                }
              />
            </div>

            <div className="col-md-2">
              <input
                className="form-control"
                placeholder="SKU"
                value={form.sku}
                onChange={(e) =>
                  setForm({
                    ...form,
                    sku: e.target.value,
                  })
                }
              />
            </div>

            <div className="col-md-2">
              <input
                className="form-control"
                placeholder="Price"
                value={form.price}
                onChange={(e) =>
                  setForm({
                    ...form,
                    price: e.target.value,
                  })
                }
              />
            </div>

            <div className="col-md-2">
              <input
                className="form-control"
                placeholder="Stock"
                value={form.stock}
                onChange={(e) =>
                  setForm({
                    ...form,
                    stock: e.target.value,
                  })
                }
              />
            </div>

            <div className="col-md-3">
              <button
                type="submit"
                className="btn btn-success w-100"
              >
                Add Product
              </button>
            </div>

          </form>

        </div>

      </div>

      <div className="card shadow mt-4">

        <div className="card-body">

          <table className="table table-striped">

            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>SKU</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>

              {products.map((product) => (
                <tr key={product.id}>

                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>{product.sku}</td>
                  <td>₹{product.price}</td>
                  <td>{product.stock}</td>

                  <td>
                    <button
                      className="btn btn-danger btn-sm"
                      onClick={() =>
                        handleDelete(product.id)
                      }
                    >
                      Delete
                    </button>
                  </td>

                </tr>
              ))}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}

export default Products;