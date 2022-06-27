const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      message: null,
      msg: { show: false, text: "" },
      token: null,
      user_email: "",
      demo: [
        {
          title: "FIRST",
          background: "white",
          initial: "white",
        },
        {
          title: "SECOND",
          background: "white",
          initial: "white",
        },
      ],
    },
    actions: {
      //ChangeMessage
      changeMessage: () => {
        setStore({ message: "Tic,tac,tic,tac...." });
      },
      //log out
      logOut: () => {
        setStore({ token: null });
      },
      // Use getActions to call a function within a fuction
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },

      getMessage: () => {
        // fetching data from the backend
        fetch(process.env.BACKEND_URL + "/hello")
          .then((resp) => resp.json())
          .then((data) => setStore({ message: data.message }))
          .catch((error) =>
            console.log("Error loading message from backend", error)
          );
      },
      changeColor: (index, color) => {
        //get the store
        const store = getStore();

        //we have to loop the entire demo array to look for the respective index
        //and change its color
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });

        //reset the global store
        setStore({ demo: demo });
      },

      // generate TOKEN
      generate_token: async (email_recieved, password_recieved) => {
        const store = getStore();

        const resp = await fetch(process.env.BACKEND_URL + "/token", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: email_recieved,
            password: password_recieved,
          }),
        });

        if (!resp.ok)
          throw setStore({ message: "Invalid email or Password !" });

        if (resp.status === 401) {
          throw "Invalid credentials";
        } else if (resp.status === 400) {
          throw "Invalid email or password format";
        }
        const data = await resp.json();
        // save your token in the localStorage
        //also you should set your user into the store using the setStore function
        localStorage.setItem("token", data.token);
        setStore({ token: data.token });
        setStore({ user_email: email_recieved });

        return data;
      },

      //CREATE NEW USER
      createUser: async (data) => {
        const actions = getActions();
        const store = getStore();

        const resp = await fetch(process.env.BACKEND_URL + "/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
        const data2 = await resp.json();
        const text_received = data2.text;
        setStore({ msg: { show: true, text: text_received } });
      },
    },
  };
};

export default getState;
