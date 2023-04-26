import router from "@/router";
import Textbook from "@/types/Textbook";
import Lesson from "@/types/Lesson";
import Section from "@/types/Section";
import User from "@/types/User";
import UserProgress from "@/types/UserProgress";
import { getToken, getRequest, postRequest } from "@/utils/api";
import { createStore } from "vuex";
import SlideImage from "@/types/SlideImage";
import Alert from "@/types/Alert";
import { Tip, TipResponse } from "@/types/Tip";

type State = {
  authToken: string | null;
  isAuthenticated: boolean;
  user: User | null;
  userProgress: UserProgress | null;
  textbook: Textbook | null;
  currentLesson: Lesson | null;
  currentSection: Section | null;
  currentSlide: string | null;
  currentImage: SlideImage | null;
  currentTips: Tip[];
  alerts: Alert[];
};

export default createStore({
  state: {
    authToken: null,
    isAuthenticated: false,
    user: null,
    userProgress: null,
    textbook: null,
    currentLesson: null,
    currentSection: null,
    currentSlide: null,
    currentImage: null,
    currentTips: [],
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

    setUserProgress(state, userProgress) {
      state.userProgress = userProgress;
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

    setCurrentSlide(state, slide) {
      state.currentSlide = slide;
    },

    setCurrentImage(state, image) {
      state.currentImage = image;
    },

    setCurrentTips(state, tipResponse) {
      state.currentTips = tipResponse.items;
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
    async getUser(context) {
      if (context.state.authToken) {
        const result = await getRequest<User>(
          "whoami",
          context.state.authToken
        );
        context.commit("setUser", result);
      }
    },

    // TODO add loading and error handling
    async getUserProgress(context) {
      if (context.state.authToken) {
        const result = await getRequest<UserProgress>(
          "home",
          context.state.authToken
        );
        context.commit("setUserProgress", result);
      }
    },

    // TODO once there are other courses/textbooks, this should become more generic in order to get any book
    async getDigitalStewardTextbook(context) {
      if (context.state.authToken) {
        const result = await getRequest<Textbook>(
          "textbooks/4/",
          context.state.authToken
        );
        context.commit("setTextbook", result);
      }
    },

    async getCurrentLesson(context, id) {
      if (context.state.authToken) {
        const result = await getRequest<Lesson>(
          `lessons/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentLesson", result);
      }
    },

    async getCurrentSection(context, id) {
      if (context.state.authToken) {
        const result = await getRequest<Section>(
          `sections/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentSection", result);
      }
    },

    async getCurrentImage(context, id) {
      if (context.state.authToken) {
        const result = await getRequest<SlideImage>(
          `images/${id}/`,
          context.state.authToken
        );
        context.commit("setCurrentImage", result);
      }
    },

    async getCurrentTips(context, id) {
      if (context.state.authToken) {
        const result = await getRequest<TipResponse>(
          `tips/?slide_id=${id}`,
          context.state.authToken
        );
        context.commit("setCurrentTips", result);
        context.commit("setCurrentSlide", id);
      }
    },

    // TODO add way to handle errors from the server
    async updateTips(context, body) {
      if (context.state.authToken) {
        await postRequest<Record<string, unknown>>(
          `tips/`,
          {
            ...body,
            slide_id: context.state.currentSlide,
            section: context.state.currentSection?.id,
          },
          context.state.authToken
        );
      }
    },

    // TODO error handling
    async markSectionComplete(context) {
      if (context.state.authToken) {
        await postRequest<Record<string, unknown>>(
          `grades/`,
          {
            section: context.state.currentSection?.id,
            student: context.state.user?.id,
          },
          context.state.authToken
        );
      }
    },
  },

  modules: {},
});
