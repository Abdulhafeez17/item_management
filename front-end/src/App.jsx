import { Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Login from "./pages/Login";
import Signup from "./pages/singup";

import ItemListPage from "./pages/ItemListpage";
import ItemDetailPage from "./pages/ItemDetailPage";
import CreateItemPage from "./pages/CreateItemPage";
import EditItemPage from "./pages/EditItemPage";

function App() {
  return (
    <Routes>
      <Route
        path="/"
        element={
         
            <Login />
          
        }
      />

      {/* SIGNUP PAGE */}
      <Route
        path="/signup"
        element={
      
            <Signup />
        
        }
      />

      {/* ITEM LIST */}
      <Route
        path="/items"
        element={
          <Layout>
            <ItemListPage />
          </Layout>
        }
      />

      {/* ITEM DETAIL */}
      <Route
        path="/items/:id"
        element={
          <Layout>
            <ItemDetailPage />
          </Layout>
        }
      />

      {/* CREATE ITEM */}
      <Route
        path="/create"
        element={
          <Layout>
            <CreateItemPage />
          </Layout>
        }
      />

      {/* EDIT ITEM */}
      <Route
        path="/edit/:id"
        element={
          <Layout>
            <EditItemPage />
          </Layout>
        }
      />

    </Routes>
  );
}

export default App;