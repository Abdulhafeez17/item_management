import Navbar from "./Navbar";

function Layout({ children }) {
  return (
    <div>
      <Navbar />

      <div className="container">
        {children}
      </div>
    </div>
  );
}

export default Layout;