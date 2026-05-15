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

      alert("Signup successful");

      navigate("/items");

    } catch (err) {

      alert(err.response.data.error);
    }
  };

  return (

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
  );
}

export default Signup;