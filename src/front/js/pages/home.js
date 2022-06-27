import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Login_form } from "../component/login-form";
import { Redirect } from "react-router-dom";

export const Home = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className="mx-auto text-center mt-5">
      <h1 className="text-primary">Welcome to Our Web !</h1>

      {store.token ? (
        <Redirect to={"/dashboard"} />
      ) : (
        <div>
          <Login_form />
          {store.message == "Invalid email or Password !" ? (
            <div className="alert alert-danger mt-3 col-5 mx-auto" role="alert">
              {store.message}
            </div>
          ) : (
            <div className="alert alert-info mt-3 col-5 mx-auto" role="alert">
              {store.message}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
