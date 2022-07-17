import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import { Dropdown } from "floating-vue";
import "floating-vue/dist/style.css";

createApp(App)
  .use(store)
  .use(router)
  .component("VDropdown", Dropdown)
  .mount("#app");
