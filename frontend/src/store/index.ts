import router from "@/router";
import { User } from "@/types/User";
import { getToken, makeRequest } from "@/utils/api";
import { createStore } from "vuex";

type State = {
  authToken: string | null;
  isAuthenticated: boolean;
  user: User | null;
};

export default createStore({
  state: {
    authToken: null,
    isAuthenticated: false,
    user: null,
  } as State,
  mutations: {
    setToken(state, token) {
      state.authToken = token;
      state.isAuthenticated = true;
    },

    // TODO make this into an action instead of a mutation
    logOut(state) {
      state.isAuthenticated = false;
    },

    setUser(state, user) {
      state.user = user;
    },
  },
  actions: {
    async logIn(context) {
      const response = await getToken();

      if (response.token) {
        context.commit("setToken", response.token);
        router.push({ name: "Home" });
      } else {
        throw new Error("bad login"); // TODO should replace this with something else to tell user login failed
      }
    },

    async getUserData(context) {
      if (context.state.authToken) {
        const result = await makeRequest("home", context.state.authToken);
        context.commit("setUser", result);
      }
    },
  },
  modules: {},
});
