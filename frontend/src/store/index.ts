import router from "@/router";
import Textbook from "@/types/Textbook";
import Lesson from "@/types/Lesson";
import Section from "@/types/Section";
import User from "@/types/User";
import { getToken, makeRequest } from "@/utils/api";
import { createStore } from "vuex";
import SlideImage from "@/types/SlideImage";
import Alert from "@/types/Alert";

type State = {
  authToken: string | null;
  isAuthenticated: boolean;
  user: User | null;
  textbook: Textbook | null;
  currentLesson: Lesson | null;
  currentSection: Section | null;
  currentImage: SlideImage | null;
  alerts: Alert[];
};

export default createStore({
  state: {
    authToken: null,
    isAuthenticated: false,
    user: null,
    textbook: null,
    currentLesson: null,
    currentSection: null,
    currentImage: null,
    alerts: [],
  } as State,
  mutations: {
    setToken(state, token) {
      state.authToken = token;
      state.isAuthenticated = true;
    },

    removeToken(state) {
      state.authToken = null;
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

    setCurrentImage(state, image) {
      state.currentImage = image;
    },

    addAlert(state, alert) {
      state.alerts.push(alert);
    },

    removeAlert(state, alertType) {
      // set alerts state to everything that isn't of the indicated alertType
      state.alerts = state.alerts.filter(
        (alert) => alert.alertType !== alertType
      );
    },
  },
  actions: {
    async logIn(context, { username, password }) {
      const response = await getToken(username, password);

      if (response.token) {
        context.commit("setToken", response.token);
        localStorage.setItem("token", response.token);
        context.commit("removeAlert", "login");
        router.push({ name: "Home" });
      } else {
        context.commit("addAlert", {
          alert: "Sorry, could not log in",
          alertType: "login",
        });
        throw new Error("bad login");
      }
    },

    async logInWithToken(context, token) {
      if (token) {
        context.commit("setToken", token);
        router.push({ name: "Home" });
      } else {
        throw new Error("bad login"); // TODO should replace this with something else to tell user login failed
      }
    },

    async logOut(context) {
      context.commit("removeToken");
      localStorage.removeItem("token");
      router.push({ name: "Login" });
    },

    // TODO add loading and error handling
    async getUserData(context) {
      if (context.state.authToken) {
        const result = await makeRequest<User>("home", context.state.authToken);
        context.commit("setUser", result);
      }
    },

    // TODO once there are other courses/textbooks, this should become more generic in order to get any book
    async getDigitalStewardTextbook(context) {
      if (context.state.authToken) {
        const result = await makeRequest<Textbook>(
          "textbooks/4/",
          context.state.authToken
        );
        context.commit("setTextbook", result);
      }
    },

    async getCurrentLesson(context, id) {
      if (context.state.authToken) {
        const result = await makeRequest<Lesson>(
          `lessons/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentLesson", result);
      }
    },

    async getCurrentSection(context, id) {
      if (context.state.authToken) {
        const result = await makeRequest<Section>(
          `sections/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentSection", result);
      }
    },

    async getCurrentImage(context, id) {
      if (context.state.authToken) {
        const result = await makeRequest<SlideImage>(
          `images/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentImage", result);
      }
    },
  },
  modules: {},
});
