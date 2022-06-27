import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { Context } from "../store/appContext";

export const Navbar = () => {
  const { store, actions } = useContext(Context);

  return (
    <nav className="navbar navbar-light bg-light">
      <div className="container">
        <Link to="/">
          <span className="navbar-brand mb-0 h1">INICIO</span>
        </Link>

        {store.token ? (
          <div className="ml-auto">
            <Link to="/demo">
              <button className="btn btn-primary">
                Check the Context in action
              </button>
            </Link>
            <span>
              <button
                className="btn btn-primary m-2"
                onClick={() => {
                  actions.logOut();
                }}
              >
                LOG OUT!
              </button>
            </span>
          </div>
        ) : (
          ""
        )}
      </div>
    </nav>
  );
};
