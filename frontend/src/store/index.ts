import router from "@/router";
import Textbook from "@/types/Textbook";
import Lesson from "@/types/Lesson";
import Section from "@/types/Section";
import User from "@/types/User";
import { getToken, makeRequest } from "@/utils/api";
import { createStore } from "vuex";

type State = {
  authToken: string | null;
  isAuthenticated: boolean;
  user: User | null;
  textbook: Textbook | null;
  currentLesson: Lesson | null;
  currentSection: Section | null;
};

export default createStore({
  state: {
    authToken: null,
    isAuthenticated: false,
    user: null,
    textbook: null,
    currentLesson: null,
    currentSection: null,
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

    setCurrentLesson(state, lesson) {
      state.currentLesson = lesson;
    },

    setCurrentSection(state, section) {
      state.currentSection = section;
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

    async getCurrentLesson(context, id) {
      if (context.state.authToken) {
        const result = await makeRequest(
          `lessons/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentLesson", result);
      }
    },

    async getCurrentSection(context, id) {
      if (context.state.authToken) {
        const result = await makeRequest(
          `sections/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentSection", result);
      }
    },
  },
  modules: {},
});
