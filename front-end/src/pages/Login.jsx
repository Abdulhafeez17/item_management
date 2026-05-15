import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { loginUser } from "../api/itemsApi";

function Login() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      const response = await loginUser(form);

      localStorage.setItem(
        "token",
        response.data.token
      );

      alert("Login successful");

      navigate("/items");

    } catch (err) {

      alert("Invalid credentials");
    }
  };

  return (

  <div>

    {/* Top Black Header */}
    <div
      style={{
        backgroundColor: "black",
        color: "white",
        padding: "15px 20px",
      }}
    >
      <h1
        style={{
          margin: 0,
          fontWeight: "bold",
        }}
      >
        Item Manager
      </h1>
    </div>

    {/* Login Section */}
    <div style={{ padding: "20px" }}>

      <h2>Login</h2>

      <form onSubmit={handleSubmit}>

        <input
          placeholder="Username"
          value={form.username}
          onChange={(e) =>
            setForm({
              ...form,
              username: e.target.value,
            })
          }
        />

        <br /><br />

        <input
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={(e) =>
            setForm({
              ...form,
              password: e.target.value,
            })
          }
        />

        <br /><br />

        <button type="submit">
          Login
        </button>

      </form>

      <br />

      <p>
        Don't have an account?
        <Link to="/signup">
          {" "}Signup
        </Link>
      </p>

    </div>

  </div>
);
}

export default Login;