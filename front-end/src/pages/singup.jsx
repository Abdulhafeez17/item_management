import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { signupUser } from "../api/itemsApi";

function Signup() {

  const navigate = useNavigate();

  const [form, setForm] = useState({
    username: "",
    password: "",
  });

  const handleSubmit = async (e) => {

    e.preventDefault();

    try {

      await signupUser(form);
      localStorage.setItem(
        "token",
        form.username
      );


      alert("Signup successful");


      navigate("/items");

    } catch (err) {

      alert(err.response.data.error);
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

    {/* Signup Form */}
    <div style={{ padding: "20px" }}>

      <h2>Signup</h2>

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
          Signup
        </button>

      </form>

    </div>

  </div>
);
}

export default Signup;