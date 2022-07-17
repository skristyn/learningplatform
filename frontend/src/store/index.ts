import { createStore } from "vuex";

export default createStore({
  state: {
    isAuthenticated: false, // TODO: this state and its mutations should hook up to auth system
  },
  mutations: {
    logOut(state) {
      state.isAuthenticated = false;
    },

    logIn(state) {
      state.isAuthenticated = true;
    },
  },
  actions: {},
  modules: {},
});
