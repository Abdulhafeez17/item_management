import { Link, useNavigate } from "react-router-dom";
import { logoutUser } from "../api/itemsApi";


function Navbar() {

  const navigate = useNavigate();

  const handleLogout = async () => {

    try {

      const token = localStorage.getItem("token");

      await logoutUser(token);

    } catch (err) {

      console.log(err);

    }

    localStorage.removeItem("token");

    alert("Logged out successfully");

    navigate("/");
  };

  return (

    <nav className="navbar">

      <h2>Item Manager</h2>

      <div className="nav-links">

        <Link to="/items">Items</Link>

        <Link to="/create">Create</Link>

        <button
          className="logout-btn"
          onClick={handleLogout}
        >
          Logout
        </button>

      </div>

    </nav>
  );
}

export default Navbar;