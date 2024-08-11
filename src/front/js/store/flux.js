const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			token: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			]
		},
		actions: {
			// Use getActions to call a function within a function
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello");
					const data = await resp.json();
					setStore({ message: data.message });
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error);
				}
			},
			changeColor: (index, color) => {
				// get the store
				const store = getStore();

				// we have to loop the entire demo array to look for the respective index
				// and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				// reset the global store
				setStore({ demo: demo });
			},
			// Login function to authenticate the user and set the token in the store and sessionStorage
			login: async (email, password) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + "/api/login", {
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify({ email, password }),
					});
					
					if (response.ok) {
						const { token } = await response.json();
						sessionStorage.setItem("token", token); 
						setStore({ token }); 
						return true;
					} else {
						const errorData = await response.json();
						alert(errorData.message || "Invalid credentials");
						return false;
					}
				} catch (error) {
					console.error("Error during login:", error);
					alert("Error during login. Please try again.");
					return false;
				}
			},
			// Logout function to clear the token from the store and sessionStorage
			logout: () => {
				sessionStorage.removeItem("token");
				setStore({ token: null }); // Limpia el token del estado global
				navigate('/login');
			},
			// Function to sync the token from sessionStorage to the store when the app loads
			syncTokenFromSessionStorage: () => {
				const token = sessionStorage.getItem("token");
				if (token) {
					setStore({ token });
				}
			},
		},
	};
};

export default getState;
