import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";

export const Login_form = () => {
  const { actions, store } = useContext(Context);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="container">
      <div className="row">
        <div className="col-5 mx-auto">
          <input
            onChange={(e) => {
              setEmail(e.target.value);
              actions.changeMessage({ message: "Tic.tac.tic.tac..." });
            }}
            className="form-control"
            type="mail"
            id="email"
            name="email"
            placeholder="email"
          />
          <input
            onChange={(e) => {
              setPassword(e.target.value);
              actions.changeMessage({ message: "Tic.tac.tic.tac..." });
            }}
            className="form-control"
            type="password"
            id="password"
            name="password"
            placeholder="password"
          />
          <Link to="/signup">
            <p className="text-end">Never here?, Sign Up!</p>
          </Link>
          <button
            onClick={() => {
              actions.generate_token(email, password);
            }}
            className="btn btn-primary mt-3"
            type="submit"
          >
            Go in !
          </button>
        </div>
      </div>
    </div>
  );
};
