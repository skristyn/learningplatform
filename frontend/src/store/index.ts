import router from "@/router";
import Textbook from "@/types/Textbook";
import { User } from "@/types/User";
import { getToken, makeRequest } from "@/utils/api";
import { createStore } from "vuex";

type State = {
  authToken: string | null;
  isAuthenticated: boolean;
  user: User | null;
  textbook: Textbook | null;
};

export default createStore({
  state: {
    authToken: null,
    isAuthenticated: false,
    user: null,
    textbook: null,
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

    setTextbook(state, textbook) {
      state.textbook = textbook;
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

    // TODO add loading and error handling
    async getUserData(context) {
      if (context.state.authToken) {
        const result = await makeRequest("home", context.state.authToken);
        context.commit("setUser", result);
      }
    },

    async getDigitalStewardTextbook(context) {
      if (context.state.authToken) {
        const result = await makeRequest(
          "textbooks/4/",
          context.state.authToken
        );
        context.commit("setTextbook", result);
      }
    },
  },
  modules: {},
});
