function Dashboard() {
  return (
    <div className="container mt-5">

      <div className="row">

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h5>Total Products</h5>
              <h2>25</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h5>Total Customers</h5>
              <h2>12</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h5>Total Orders</h5>
              <h2>30</h2>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;