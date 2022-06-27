import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Redirect } from "react-router-dom";

export const Dashboard = () => {
  const { store, actions } = useContext(Context);

  return (
    <div className="container-fluid">
      {store.token ? (
        <div className="row">
          <div className="col ml-auto">
            <p className="text-end text-success">Usuario: {store.user_email}</p>
          </div>
          <div className="row">
            <div className="col-auto mx-auto">
              <h1 className="text-warning">
                Welcome to the private dashboard !
              </h1>
            </div>
          </div>
        </div>
      ) : (
        <Redirect to={"/"} />
      )}
    </div>
  );
};
